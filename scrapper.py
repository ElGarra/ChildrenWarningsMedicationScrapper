import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import re
import csv
import json

# Class to scrapp https://www.medicinesforchildren.org.uk/ webpage and cathc the data
class Scrapper():

    def __init__(self):
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.letter = self.alphabet[0]
        self.page_count = 1
        self.alphabet_index = 0
        self.letter = ""
        self.url = ""
        self.html = None
        self.urls = []
        self.data = None
        self.my_data = []
        self.all_scrapped_data = []
        self.all_data = []
        self.run_letter_counter = 0
        self.translator = Translator()
        self.file_name = "medicines_for_children.csv"
        self.file = open(self.file_name, "w")
        self.writer = csv.writer(self.file, delimiter = ";")
        self.dict_list = []

# Method to scrapp each medication and store the name and warnings on a list
    def scrapCurrentURL(self, url):
        data = requests.get(url)
        medication_name = url[50:len(url) - 1]
        aux_list = []
        my_data = []
        for char in medication_name:
            if char != "-":
                aux_list.append(char)
            else:
                aux_list.append(" ")
        medication = "".join(aux_list)
        medication_translated = self.translator.translate(medication, src='en', dest='es')
        my_data.append(medication_translated.text)

        html = BeautifulSoup(data.text, "html.parser")
        try:
            articles = html.find("h3", {"id": "urgent-side-effects"}).find_next_sibling()
            while articles is not None:
                article_data = re.sub("<[^>]*>", "", str(articles.p)) 
                article_data_translated = self.translator.translate(article_data, src='en', dest='es')
                my_data.append(article_data_translated.text.replace("\n", " "))
                articles = articles.find_next_sibling() 
        
            return my_data

        except AttributeError:
            return None
    

# Method to get the URL for each medication
    def getURLForScrapping(self):

        self.html = BeautifulSoup(self.data.text, "html.parser")

        for a in self.html.find_all("a", href=True):
            if f"https://www.medicinesforchildren.org.uk/medicines/{self.letter.lower()}" in a["href"] and "page" not in a["href"]:
                self.urls.append(a["href"])
        return self.urls

# Method to set the parameters for the scrapper and run the functions that get the url and scrap the url
    def setScrapperParameters(self, i):
        self.alphabet_index = i
        self.letter = self.alphabet[self.alphabet_index]
        self.page_count = 1
        self.all_scrapped_data =[]
        self.url = f"https://www.medicinesforchildren.org.uk/medicines/page/{self.page_count}/?starts-with={self.letter}"
        self.data = requests.get(self.url)
        while self.data.status_code == 200:

            self.urls = self.getURLForScrapping()
            for urlscrapping in self.urls:
                self.my_data = self.scrapCurrentURL(urlscrapping)
                print(f" Page count {self.page_count} and URL {urlscrapping}")
                self.all_scrapped_data.append(self.my_data)
            
            self.page_count += 1
            self.url = f"https://www.medicinesforchildren.org.uk/medicines/page/{self.page_count}/?starts-with={self.letter}"
            self.data = requests.get(self.url)
            
            if self.data.status_code == 404:
                break
        self.data = None
        self.urls = []
        return self.all_scrapped_data

# Method to run the scrapper and store all the medication data in a list
    def runScrapper(self):
        for i in range(len(self.alphabet)):
            scrapped_data = self.setScrapperParameters(i)
            #print(scrapped_data)
            self.all_data.append(scrapped_data)
        #print(self.all_data)


# Method to write the data in a csv file
    def writeData(self):    
        for data in self.all_data:
            print("LARGO DE LETRA: " + str(len(data)))
            if len(data) > 10:
                data = data[12:]
            for data_list in data:
                if data_list is not None:
                    concat = ""
                    for i in range(1, len(data_list)):
                        concat += data_list[i]
                        concat += " "
                    data_dict = {"name": data_list[0], "BabyAlert": concat}
                    self.dict_list.append(data_dict)
                    self.json_list = json.dumps(self.dict_list, ensure_ascii=False, indent=4).encode('utf8')
                    self.writer.writerow(data_list)
                    #for i in range(0, len(data_list)):
                        #self.writer.writerow(data_list[i])
        with open("BabyAlertScrapper.json", "w", encoding="utf8") as file:
            file.write(self.json_list.decode())



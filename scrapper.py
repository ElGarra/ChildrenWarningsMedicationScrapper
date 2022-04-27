import requests
from bs4 import BeautifulSoup


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

# Method to scrapp each medication and store the name and warnings on a list
    def scrapCurrentURL(self, url):

        data = requests.get(url)
        medication_name = url[50:len(url) - 1]
        my_data = []
        my_data.append(medication_name)
        html = BeautifulSoup(data.text, "html.parser")
        try:
            articles = html.find("h3", {"id": "urgent-side-effects"}).find_next_sibling()
            while articles is not None:
                article_data = str(articles.p).replace("<p>", "").replace("</p>", "") # Try later with regex
                my_data.append(article_data)
                articles = articles.find_next_sibling() 
        
            return my_data

        except AttributeError as e:
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
            self.all_data.append(scrapped_data)





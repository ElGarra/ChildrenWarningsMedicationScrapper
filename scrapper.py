"""Module to write the scrapper class"""

import re
import json
import requests
from bs4 import BeautifulSoup
from googletrans import Translator

class Scrapper():
    """Class to scrapp https://www.medicinesforchildren.org.uk/ webpage and cathc the data"""

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
        self.dict_list = []

    def scrap_current_url(self, url):
        """Method to scrap each medication and store the name and warnings on a list"""
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
        medication_translated = self.translator.translate(
            medication, src='en', dest='es')
        my_data.append(medication_translated.text)

        html = BeautifulSoup(data.text, "html.parser")
        try:
            articles = html.find(
                "h3", {"id": "urgent-side-effects"}).find_next_sibling()
            while articles is not None:
                article_data = re.sub("<[^>]*>", "", str(articles.p))
                article_data_translated = self.translator.translate(
                    article_data, src='en', dest='es')
                my_data.append(article_data_translated.text.replace("\n", " "))
                articles = articles.find_next_sibling()

            return my_data

        except AttributeError:
            return None

    def get_url_for_scrapping(self):
        """Method to get the URL for each medication"""

        self.html = BeautifulSoup(self.data.text, "html.parser")

        for link in self.html.find_all("a", href=True):
            if f"https://www.medicinesforchildren.org.uk/medicines/{self.letter.lower()}" \
                in link["href"] and "page" not in link["href"]:
                self.urls.append(link["href"])
        return self.urls

    def set_scrapper_parameters(self, i):
        """Method to set the parameters for the scrapper and run the functions to scrap the url"""

        self.alphabet_index = i
        self.letter = self.alphabet[self.alphabet_index]
        self.page_count = 1
        self.all_scrapped_data = []
        self.url = "https://www.medicinesforchildren.org.uk/medicines/page/" \
            f"{self.page_count}/?starts-with={self.letter}"
        self.data = requests.get(self.url)
        while self.data.status_code == 200:

            self.urls = self.get_url_for_scrapping()
            for urlscrapping in self.urls:
                self.my_data = self.scrap_current_url(urlscrapping)
                print(f" Page count {self.page_count} and URL {urlscrapping}")
                self.all_scrapped_data.append(self.my_data)

            self.page_count += 1
            self.url = "https://www.medicinesforchildren.org.uk/medicines/page/" \
                f"{self.page_count}/?starts-with={self.letter}"
            self.data = requests.get(self.url)

            if self.data.status_code == 404:
                break
        self.data = None
        self.urls = []
        return self.all_scrapped_data

    def run_scrapper(self):
        """Method to run the scrapper and store all the medication data in a list"""

        for i in range(len(self.alphabet)):
            scrapped_data = self.set_scrapper_parameters(i)
            self.all_data.append(scrapped_data)



    def write_data(self):
        """Method to write the data in a csv file"""
        for data in self.all_data:
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
                    json_list = json.dumps(
                        self.dict_list, ensure_ascii=False, indent=4).encode('utf8')

        with open("Coaching.json", "w", encoding="utf8") as file:
            file.write(json_list.decode())

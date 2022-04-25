from calendar import c
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re

#from webscrapping import actualWebScrapping

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

    def scrapCurrentURL(self, url):

        data = requests.get(url)

        my_data = []

        html = BeautifulSoup(data.text, "html.parser")
        try:
            articles = html.find("h3", {"id": "urgent-side-effects"}).find_next_sibling()
            while articles is not None:
                article_data = str(articles.p).replace("<p>", "").replace("</p>", "") # Try later with re
                my_data.append(article_data)
                articles = articles.find_next_sibling() 
        
            return my_data

        except AttributeError as e:
            return None
    

    def getURLForScrapping(self):

        self.html = BeautifulSoup(self.data.text, "html.parser")

        for a in self.html.find_all("a", href=True):
            if f"https://www.medicinesforchildren.org.uk/medicines/{self.letter.lower()}" in a["href"] and "page" not in a["href"]:
                self.urls.append(a["href"])
        return self.urls

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

    def runScrapper(self):
        for i in range(len(self.alphabet)):
            scrapped_data = self.setScrapperParameters(i)
            self.all_data.append(scrapped_data)

#print(all_scrapped_data)

scrapper = Scrapper()
scrapper.runScrapper()
for letra in scrapper.all_data:
    print(letra)
    print("------------------------------------------------")


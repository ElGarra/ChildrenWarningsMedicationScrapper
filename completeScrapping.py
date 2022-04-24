from calendar import c
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re

from webscrapping import actualWebScrapping

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def getURLForScrapping(data, letter):
    html = BeautifulSoup(data.text, "html.parser")
    urls = []
    for a in html.find_all("a", href=True):
        if f"https://www.medicinesforchildren.org.uk/medicines/{letter.lower()}" in a["href"]:
            urls.append(a["href"])
    return urls

def setParameters(alphabet_index):
    letter = alphabet[alphabet_index]
    page_count = 1
    url = f"https://www.medicinesforchildren.org.uk/medicines/page/{page_count}/?starts-with={letter}"
    data = requests.get(url)
    
    all_scrapped_data = []
    while data.status_code == 200:

        urls = getURLForScrapping(data, letter)
        for urlscrapping in urls:
            my_data = actualWebScrapping(urlscrapping)
            print(f" Page count {page_count} and URL {urlscrapping}")
            all_scrapped_data.append(my_data)
        
        page_count += 1
        url = f"https://www.medicinesforchildren.org.uk/medicines/page/{page_count}/?starts-with={letter}"
        data = requests.get(url)
        
        if data.status_code == 404:
            break
    return all_scrapped_data

all_scrapped_data = []
for i in range(len(alphabet)):
    scrapped_data = setParameters(i)
    all_scrapped_data.append(scrapped_data)

print(all_scrapped_data)



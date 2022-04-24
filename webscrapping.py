import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
letter = alphabet[0]

url = f"https://www.medicinesforchildren.org.uk/medicines/allopurinol-for-hyperuricaemia/"
data = requests.get(url)

my_data = []

html = BeautifulSoup(data.text, "html.parser")
articles = html.find("h3", {"id": "urgent-side-effects"}).find_next_sibling()

while articles is not None:
    article_data = str(articles.p).replace("<p>", "").replace("</p>", "") # Try later with re
    my_data.append(article_data)
    articles = articles.find_next_sibling() 

pprint(my_data)

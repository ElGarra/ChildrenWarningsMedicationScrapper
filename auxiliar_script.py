import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
letter = alphabet[0]

def actualWebScrapping(url):

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
    
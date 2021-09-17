from bs4 import BeautifulSoup
import requests, ssl
from urllib.request import urlopen
ssl._create_default_https_context = ssl._create_unverified_context
import re

def crawler(url, depth):
    if depth == 0:
        return None

    html = urlopen(url)                        # You were missing 
    soup = BeautifulSoup(html, 'html.parser')  # these lines.

    links = soup.find("div",{"id" : "bodyContent"}).findAll("a", href=re.compile("(/wiki/)+([A-Za-z0-9_:()])+"))

    print("Level ", depth, url)
    for link in links:
        if ':' not in link['href']:
            crawler("https://en.wikipedia.org"+link['href'], depth - 1)

url = "https://en.wikipedia.org/wiki/Big_data"
crawler(url, 3)
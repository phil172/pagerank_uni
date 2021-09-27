from bs4 import BeautifulSoup
import ssl
from urllib.request import urlopen
import re, os
import json
base_url = "https://www.math.kit.edu/"
ssl._create_default_https_context = ssl._create_unverified_context

class HtmlImport():
    def __init__(self, path):
        self.path = path
        self.soup = self.get_soup()
        self.text = self.get_text()
        

    def get_soup(self):
        with open(self.path) as html_file:
            soup = BeautifulSoup(html_file, features="html.parser")
            return soup

    def get_text(self):
        soup = self.soup
        for script in self.soup(["script", "style"]):
            script.extract()    # rip it out
        # get text
        for script in soup(["script", "style"]):
            script.extract()    # rip it out
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text

def to_json(dct, file):
    with open(file, "w") as outfile:
        json.dump(dct, outfile)
    
all_pages = os.listdir("pages")


searchterm = input("Search something...")
searchterm = searchterm.lower()
search_dict = dict()

for page in all_pages:
    h = HtmlImport("pages/"+page)
    text: str = h.get_text()
    text = text.lower()
    pos = re.finditer(searchterm, text)
    spans = []
    for el in pos:
        spans.append(el.span())
        search_dict[page] = spans

to_json(search_dict, "searchdict.json")

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
        self.text = self.get_text_string()
        

    def get_soup(self):
        with open(self.path) as html_file:
            soup = BeautifulSoup(html_file, features="html.parser")
            return soup

    def get_text_string(self):
        soup = self.soup
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


if __name__ == "__main__":
    all_pages = os.listdir("pages") ## LISTE zb [9.html, 8.html, ...]

    ### import pagerank json
    ### {1: 1.2, 2: 1.4, ...}


    searchterm = input("Search something...")
    searchterm = searchterm.lower()
    search_dict = dict()

    for page in all_pages:
        h = HtmlImport("pages/"+page)
        text: str = h.get_text_string()
        text = text.lower()
        results = [m for m in re.finditer(searchterm, text)]
        spans = []
        if len(results) > 0:
            for el in results:
                spans.append(el.span())
                search_dict[page] = spans
            print(search_dict)
        elif len(results) == 0:
            print("nothing found")
            terms = searchterm.split(" ")
            for term in terms:
                print(f"trying again for {term}")
                results = [m for m in re.finditer(term, text)]
                if len(results) == 0:
                    print("not all terms found...")
                    break
                print(f"{term} found")
                # spans = []
                # for el in results:
                #     spans.append(el.span())

        #                 search_dict[page] = spans
        #         except StopIteration as e:dd
        #             print(f"{term} not in {page}")

    ### FALLS NICHTS GEFUNDEN
    ### 1x Suche für "Fakultät"
    ### 1x Suche für "für"
    ### 1x Suche für "Mathematik"


    to_json(search_dict, "searchdict.json")
    # print(search_dict["9.html"])
    # print(text[0:80])

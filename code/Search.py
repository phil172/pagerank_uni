from bs4 import BeautifulSoup
import ssl
from urllib.request import urlopen
import re, os, colorama, json, ssl
import random

''' COLORAMA MODULE '''
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW
BLUE = colorama.Fore.BLUE
RED = colorama.Fore.RED

''''URL SSL'''
base_url = "https://www.math.kit.edu/"
ssl._create_default_https_context = ssl._create_unverified_context



''' IMPORT HTML FILES FROM FOLDER'''
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
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text

''' SAVE SEARCH'''
class Save():
    def __init__(self, file, dct):
        self.file = file
        self.dct = dct
    def to_json(self):
        with open(self.file, "w") as outfile:
            json.dump(self.dct, outfile)

''' IMPORT PAGERANKING '''

class PageRank():
    def __init__(self):
        self.files = os.listdir("pages")
        self.pagerank: list() = [random.uniform(0.8,1.5) for x in range(len(self.files))]
        self.rank_dict: dict() = dict(zip(self.files, self.pagerank))
        self.sorted_dict: dict() = self.sort_dict()

    def sort_dict(self):
        s_dict = dict(sorted(self.rank_dict.items(), key=lambda item: item[1], reverse=True))
        return s_dict

''' NAVIGATE TERMINAL '''


class NavigateTerminal():
    def __init__(self):
        self.welcome = self.welcome()
        self.searchterm = self.check_searchterm()
    def welcome(self):
        print(f"{GREEN}\n")
        print("\n")
        print("\n")
        print(f"Welcome to Pagerank!{RESET} \n")
        print(f"{RED}**************************")
        print("\n")
        print(f"{RED} made by Philipp and Xander")
        print("\n")
        print(f"{RED}**************************{RESET}")
        print("\n")
        print("\n")

    def check_searchterm(self):
        while True:
            input_str = input(f"{GREEN}Please enter your search term...\n")
            print("\n")
            print("\n")
            if input_str.strip().isdigit():
                print(f"{GREEN}Not a string... Please try again{RESET}")
                continue
            else:
                print(f"{GREEN}You're searching for {input_str}")
                print("\n")
                print("\n")
                print(f"**************************{RESET}")
                print("\n")
                print("\n")
                return input_str.lower()
                

''' SEARCH '''

class Search():
    def __init__(self):
        n = NavigateTerminal()
        p = PageRank()
        self.searchterm = n.searchterm
        self.all_pages = list(p.sorted_dict.keys())
        self.searchdict = self.return_indexes()  

    def return_indexes(self):
        searchdict = dict()
        for page in self.all_pages:
            h = HtmlImport("pages/"+page)
            text: str = h.get_text_string()
            text = text.lower()
            results = [m for m in re.finditer(self.searchterm, text)]
            spans = []
            if len(results) > 0:
                for el in results:
                    spans.append(el.span())
                    searchdict[page] = spans
            elif len(results) == 0:
                terms = self.searchterm.split(" ")
                for term in terms:
                    print(f"trying again for {term}")
                    results = [m for m in re.finditer(term, text)]
                    if len(results) == 0:
                        print("not all terms found...")
                        break
                    print(f"{term} found")
        if len(list(searchdict.keys())) == 0:
            print("nothing found")
            return
        else:
            print("\n")
            print("\n")
            print(f"{YELLOW}**************************{RESET}")
            print("\n")
            print("\n")    
            print(f"{YELLOW}{self.searchterm} found on {len(list(searchdict.keys()))} pages{RESET}!")
            print("\n")
            print("\n")            
            Save("searchresults.json", searchdict).to_json()
            return searchdict


''' SHOW RESULTS '''

class ShowResults():
    def __init__(self):
        s = Search()
        self.results = list(s.searchdict.keys())
        self.first_page: str = self.results[0]
        self.first_values = list(s.searchdict[self.first_page])
        self.second_page = self.results[1]
        self.second_values = list(s.searchdict[self.second_page])
        self.third_page = self.results[2]
        self.third_values = list(s.searchdict[self.third_page])
        self.inv_id_dict = self.get_id_dict()
        #self.testing = self.test()

    def get_id_dict(self):
        with open('id_dict.json') as json_file:
            id_dict = json.load(json_file)
        inv_id_dict = {v: k for k, v in id_dict.items()}
        return inv_id_dict
                
    def test(self):
        print("Testing resuts")
        print(self.results)
        print(self.first_page)
        print(self.first_values)

    def find_link(self, page):
        id = page.replace(".html","")
        link = self.inv_id_dict[int(id)]
        return link
        
    def print_out(self):
        #Import the html file
        h = HtmlImport("pages/"+self.first_page)         
        text = h.text
        found_string = self.first_values[0]
        output: str = text[found_string[0]:found_string[1]+300]
        output = output.replace("\n", " ")
        first_link = self.find_link(self.first_page)
        print(f"{RED}{output} ...")
        print("\n")
        print("\n")
        print(f"{BLUE}Link: {first_link}")
        print("\n")
        print("\n")
        inp = input(f"{BLUE}Type next if you want to see the next result")
        if inp == "next":
            h = HtmlImport("pages/"+self.second_page)         
            text = h.text
            found_string = self.first_values[0]
            output: str = text[found_string[0]:found_string[1]+300]
            output = output.replace("\n", " ")
            link = self.find_link(self.second_page)
            print(f"{RED}{output} ...")
            print("\n")
            print("\n")
            print(f"{BLUE}Link: {link}")
            print("\n")
            print("\n")   
        else:
            print("Thank you")         

if __name__ == "__main__":
    s = ShowResults()
    s.print_out()


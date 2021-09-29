import ssl, json, itertools, urllib, colorama
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urlparse, urljoin
from urllib.error import HTTPError
from urllib.request import urlparse, urljoin
from ToGraph import Graph

'''COlORAMA MODULE'''

colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW
BLUE = colorama.Fore.BLUE
RED = colorama.Fore.RED

'''BASEURL AND SSL'''

base_url = "https://www.math.kit.edu/"
ssl._create_default_https_context = ssl._create_unverified_context

'''Initinalize Dicts'''
internal_urls = set()
urls_visited = set()
url_dict = dict()
id_dict = dict()
idpath = 'id_dict.json'
datapath = 'links_to_pages.json'

'''ID CLASS'''

class ID_spooler():

    id_iter = itertools.count(start=1)

    def __init__(self):
        self.id = next(self.id_iter)


'''SCRAPER CLASS'''
class Scraper():
    documents = [".jpg", ".xlsx", "doc", "png", "mp4", "zip", "pdf"]

    def __init__(self):
        pass

    def depht_crawler(self, input_url):
        all_href = []
        temp_urls = set()
        ### Curent URL
        current_url_domain = urlparse(input_url).netloc
        html_page = urllib.request.urlopen(input_url)
        soup = BeautifulSoup(html_page, "lxml")
        for a_tag in soup.findAll('a'):
            href = a_tag.attrs.get("href")
            if(href != "" and href != None):
                href = href.replace(" ", "")
                if current_url_domain not in href:
                    continue
                if any(ext in href for ext in self.documents):
                    continue
                if current_url_domain not in href:
                    continue
                href = urljoin(input_url, href)
                href_parsed = urlparse(href)
                href = href_parsed.scheme
                href += "://"
                href = href.replace(" ", "")
                href += href_parsed.netloc
                href += href_parsed.path
                final_parsed_href = urlparse(href)
                is_valid = bool(final_parsed_href.scheme) and bool(
                    final_parsed_href.netloc)
                if is_valid:
                    if current_url_domain in href and href not in internal_urls:
                        internal_urls.add(href)
                        temp_urls.add(href)
            all_href.append(href)
        internal_urls.remove(input_url)    
        url_dict[input_url] = list(set(all_href))
        return temp_urls


    def save_html(self, url, id):
        html_page = urllib.request.urlopen(url)
        soup = BeautifulSoup(html_page, "lxml")
        with open(str('pages/'+ str(id)+'.html'), 'w', encoding='utf-8') as f_out:
            f_out.write(soup.prettify()) 

    def to_json(self, dict, file):
        with open(file, "w") as outfile:
            json.dump(dict, outfile)

'''CRAWL AND SAFE'''
class Crawl(Scraper):
    def __init__(self, url, depth=3, urls_to_visit=200):
        self.crawl(url, depth, urls_to_visit)


    def crawl(self, url_, depth, urls_to_visit=200):
        try:
            if(depth == 0):
                print("Intern - {}".format(url_))
            elif(depth == 1):
                self.depht_crawler(url_)
            else:
                queue = []
                queue.append(url_)
                for j in range(depth):
                    print(f"DEPTH: {j}")
                    for count in range(len(queue)):
                        id_ = ID_spooler()
                        url = queue.pop(0)
                        url.replace(" ", "")
                        if url in urls_visited:
                            print(f"{RED}{url} visited")
                            continue
                        print(f"{GREEN}Scraping... {url}{RESET}")
                        print(f"{RED}URLS VISITED: {len(urls_visited)}{RESET}")
                        if len(urls_visited) > urls_to_visit:
                            self.to_json(url_dict, "links_to_pages.json")
                            self.to_json(id_dict, "id_dict.json") 
                            return
                        print(f"{YELLOW}URLS in QUEUE: {len(queue)}{RESET}")
                        urls_visited.add(url)
                        id_dict[url] = id_.id
                        urls = self.depht_crawler(url)
                        print(f"{BLUE}Url: {url} \nPage_ID:  {id_.id} \nNumberOfNewLinks: {len(urls)}{RESET}")
                        print(f"{GREEN}Done.{RESET}")
                        self.save_html(url, id_.id)
                        for i in urls:
                            if i not in urls_visited:
                                queue.append(i)
            self.to_json(url_dict, "links_to_pages.json")
            self.to_json(id_dict, "id_dict.json")                
        except KeyboardInterrupt:
            self.to_json(url_dict, "links_to_pages.json")
            self.to_json(id_dict, "id_dict.json")

'''SCRAPE'''
if __name__ == '__main__':
    Crawl(base_url, depth=3, urls_to_visit=30)

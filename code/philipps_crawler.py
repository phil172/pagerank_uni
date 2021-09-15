import itertools
from bs4 import BeautifulSoup
import requests, ssl
from urllib.request import Request, urlopen
import urllib, colorama
from urllib.parse import urlparse, urljoin
from urllib.error import HTTPError
import json
import itertools

# class resource_cl():
#     newid = itertools.count().next
#     def __init__(self):
#         self.id = resource_cl.newid()

colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW
BLUE = colorama.Fore.BLUE
RED = colorama.Fore.RED

url = "https://www.math.kit.edu/"
ssl._create_default_https_context = ssl._create_unverified_context
### Class to save Page objects
class IdSpooler:
    '''
    constructor
    '''
    def __init__(self, start=1):
        self.nextid = start

    '''
    Get the next id
    '''
    def getNext(self):
        toReturn = self.nextid
        self.nextid += 1
        return toReturn

    '''
    Get the largest returned
    '''
    def getLargest(self):
        return self.nextid

class Page:
    '''
    Constructor
    '''
    id_counter = itertools.count(start=1)
    def __init__(self, id, url, title, no_links, content, link_urls):
        self.id = next(Page.id_counter)
        self.url = url
        self.title = title
        self.no_links = no_links
        self.link_urls = link_urls
        self.page_rank = 0.0
        self.content = content

    '''
    Save Content
    '''
    def save_content(self):
        filename = "pages/" + str(self.id) + '.html'
        clean_content = str(self.content)
        clean_content = clean_content.replace('\n', '')
        with open(filename, 'w') as f:
            f.write(clean_content)
            print('page', self.id, 'saved as', filename)

    def addLink(self, url):
        if url not in self.link_urls:
            self.link_urls.append(url)


### Crawls a given Url and saves the data
class Crawler:
    def __init__(self, url):
        self.url = url
        self.spooler = IdSpooler()

    def is_valid(self, url):
        pass

    def get_id(self):
        return self.spooler.getNext()
     
    def replace(self):
        str(self).replace()
    
    def get_page(self):
        ### IF URL IN SET -> CONTINUE (Seiten nicht doppelt herunterladen)
        url = self.url
        urls = set()
        title = ""
        no_links = ""

        #print(id)
        domain_name = urlparse(url).netloc
        html_page = urllib.request.urlopen(url)
        soup = BeautifulSoup(html_page, "lxml")
        content = soup.contents
        content = soup.prettify("utf-8")
        for a_tag in soup.findAll('a'):
            href = a_tag.attrs.get("href")
            # already in the set
            if href in urls:
                continue
            ### Check if pdf link
            if "pdf" in str(href):
                continue
            if "doc" in str(href):
                continue
            if ".jpg" in str(href) or ".png" in str(href):
                continue
            if href == "" or href is None:
                continue
            # if not self.is_valid(href):
            #     print("NOT VALID")
            #     # not a valid URL
            #     continue
            if domain_name not in href:
                # external link
                continue
            urls.add(href)
        no_links = len(urls)
        title = soup.title.string
        toReturn = Page(id, url, title,  no_links, content, urls)
        return toReturn


def save_json(new_dict, filename):
    with open(filename, 'w') as fp:
        json.dump(new_dict, fp)
def add_if_key_not_exist(dict_obj, key, value):
    if key not in dict_obj:
        dict_obj.update({key: value})
    
def crawl(url):
    cr = Crawler(url)
    page = cr.get_page()
    print(f"{RED}[*] Crawling: {page.url}[*][*][*][*]{RESET}")
    print(f"{BLUE}CR: {cr.url} \nPAGE URL: {page.url} \nID:  {page.id}{RESET}")
    new_dict = dict()
    id_dict = dict()
    new_dict[page.url] = list(page.link_urls)
    id_dict[page.id] = [page.url]
    for link in page.link_urls:
        cr = Crawler(link)
        page = cr.get_page()
        #new_dict[page.url] = list(page.link_urls)
        add_if_key_not_exist(id_dict, page.id, page.url)
        add_if_key_not_exist(new_dict, page.id, page.link_urls)
        print(f"{YELLOW}[*][*][*][*]-- Crawling: {page.url} --[*][*][*][*]{RESET}")
        lenght = len(page.link_urls)
        print(f"{BLUE}Url: {page.url} \nPage_ID:  {page.id} \nNumberOfLinks: {lenght}{RESET}")
    save_json(id_dict, "IDs.json")
    save_json(new_dict, "ID_LINKS.json")
    print(f"{GREEN}Webscarping Done!")

    





crawl(url)
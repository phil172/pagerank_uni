import itertools
from bs4 import BeautifulSoup
import requests, ssl
from urllib.request import Request, urlopen
import urllib, colorama
from urllib.parse import urlparse, urljoin
from urllib.error import HTTPError
import json
from lxml import html
import itertools
from http.client import InvalidURL
import pandas as pd
from tqdm import tqdm
import config
from collections import deque

base_url = "https://www.math.kit.edu/"
ssl._create_default_https_context = ssl._create_unverified_context

i = 0

colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW
BLUE = colorama.Fore.BLUE
RED = colorama.Fore.RED


class Page:
    '''
    Constructor
    '''
    id_counter = itertools.count(start=1)
    def __init__(self, url, title, no_links, content, link_urls):
        self.id = next(Page.id_counter)
        self.url = url
        self.title = title
        self.no_links = no_links
        self.link_urls: list = link_urls
        self.page_rank = 0.0
        self.content = content


class Scraper():
    def __init__(self, url):
        self.url = url
        self.soup = self.get_page(url)
        self.page = self.crawl_links(url)
        self.new_urls = deque([url])

    def get_page(self, url):
        url = self.url
        domain_name = urlparse(url).netloc
        html_page = urllib.request.urlopen(url)
        soup = BeautifulSoup(html_page, "lxml")
        return soup

    def crawl_links(self, url):
        url = self.url
        urls = set()
        domain_name = urlparse(url).netloc
        soup = self.get_page(url)
        content = str(soup)
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
            if domain_name not in href:
                continue
            urls.add(href)
        no_links = len(urls)
        if soup.title == None:
            title = "No Title"
        title = soup.title.string
        toReturn = Page(url, title,  no_links, content, urls)
        return toReturn


class Crawler():
    def __init__(self, start_url, i=0, it=2):
        self.visited_url = set()
        self.start_url = start_url
        self.url_dict = dict()
        self.i = i
        self.it = it

    def crawl_page(self, url):
        sc = Scraper(url)
        sc.new_urls.popleft(url)
        self.visited_url.add(url)
        #links_to_crawl = sc.page.link_urls
        #print(type(links_to_crawl))
        print(self.visited_url)
        for link in sc.new_urls:
            if len(links_to_crawl) == len(self.visited_url):
                break
            if link in self.visited_url:
                print(link, " already scraped")
                continue
            sc = Scraper(link)
            self.visited_url.add(link)
            links_to_crawl = links_to_crawl | sc.page.link_urls
            print(len(links_to_crawl))
            print(self.visited_url)
            self.url_dict[link] = sc.page.link_urls
            self.crawl_page(link)            
        print("depth 2 crawled")

    def crawl(self, url):
        try:
            sc = Scraper(url)
            self.visited_url[sc.page.url] = sc.page.link_urls
            while self.i <= self.it:
                for link in sc.page.link_urls:
                    if link not in list(self.visited_url.keys()):
                        sc = Scraper(link)
                        print(f"{RED}[*] Crawling: {link}[*][*][*][*]{RESET}")
                        #print(len(sc.page.link_urls))
                        self.visited_url[sc.page.url] = sc.page.link_urls
                    else:
                        continue
                self.i +=1
        except:
            return self.visited_url
        return self.visited_url

    def safe_page(self, url):
        sc = Scraper(url)
        content = sc.page.content
        with open("output1.html", "w") as file:
            file.write(str(content))

cr = Crawler(base_url, i=0, it=2)
cr.crawl_page(base_url)




def save_json(new_dict, filename):
    with open(filename, 'w') as fp:
        json.dump(new_dict, fp)


# dct: dict = cr.crawl(cr.start_url)
# cr.safe_page(cr.start_url)

# for el in list(dct.keys()):
#     new_dct = cr.crawl(el)
#     dct.update(new_dct)

# print(len(dct))
# save_json(dct, "first_.json")


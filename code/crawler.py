from bs4 import BeautifulSoup
import requests, ssl
from urllib.request import Request, urlopen
import urllib, colorama
from urllib.parse import urlparse, urljoin
from urllib.error import HTTPError
import json

###
"https://www.thepythoncode.com/article/extract-all-website-links-python"
###


# init the colorama module
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW
BLUE = colorama.Fore.BLUE

url = "https://www.math.kit.edu/"
ssl._create_default_https_context = ssl._create_unverified_context

# initialize the set of links (unique links)
internal_urls = set()
external_urls = set()
urls_pdf = set()
urls_doc = set()
img_doc = set()
all_urls = dict()
### Validate URLs
def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

### Get all links from Website
def get_links(url: str):
    ### IF URL IN SET -> CONTINUE (Seiten nicht doppelt herunterladen)
    urls = set()
    domain_name = urlparse(url).netloc
    url.replace("#", "")
    url.replace(" ", "")
    html_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_page, "lxml")
    for a_tag in soup.findAll('a'):
        href = a_tag.attrs.get("href")
        ### Check if pdf link
        if "pdf" in str(href):
            continue
        if "zip" in str(href):
            continue
        if "xlsx" in str(href):
            continue
        if "doc" in str(href):
            continue
        if ".jpg" in str(href) or ".png" in str(href):
            continue
        if href == "" or href is None:
            continue
        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            # if href not in external_urls:
            #     print(f"{GRAY}[!] External link: {href}{RESET}")
            #     external_urls.add(href)
            continue
        #print(f"{GREEN}[*] Internal link: {href}{RESET}")
        all_urls[url] = internal_urls
        urls.add(href)
        internal_urls.add(href)
    return urls
    
def get_html_every_url(urls):
    for url in urls:
        html_page = urllib.request.urlopen(url)
        soup = BeautifulSoup(html_page, "lxml")       

urls_visited = 0
urls_visited_set = set()
url_pairs = dict()

def crawl(url, max_urls=30):
    global urls_visited, urls_visited_set
    urls_visited += 1
    print("URLS VISITED", urls_visited)
    print(f"{YELLOW}[*] Crawling: {url}{RESET}")
    links = get_links(url)
    try:
        url_pairs[url] = links
    except TypeError as e:
        print(e)
        pass
    for link in links:
        try:
            if urls_visited > max_urls:
                break
            if link in list(url_pairs.keys()):
                continue
            crawl(link, max_urls=max_urls)
        except HTTPError as e:
            print(e)
            continue

def to_json(dict, file):
    with open(file, "w") as outfile:
        json.dump(dict, outfile)

if __name__ == "__main__":
    try:
        crawl(url, max_urls=1000)
    except Exception as e:
        print(e)
    print(len(list(url_pairs.keys())))
    to_json(url_pairs, "url_pairs.json")

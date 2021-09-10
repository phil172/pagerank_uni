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

### URL and SSL
url = "https://www.math.kit.edu/"
ssl._create_default_https_context = ssl._create_unverified_context

# initialize the set of links (unique links)
internal_urls = set()
external_urls = set()
urls_pdf = set()
urls_doc = set()
img_doc = set()

### Validate URLs
def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

### Get all links from Website
def get_links(url):
    ### IF URL IN SET -> CONTINUE (Seiten nicht doppelt herunterladen)
    urls = set()
    domain_name = urlparse(url).netloc
    html_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_page, "lxml")
    for a_tag in soup.findAll('a'):
        href = a_tag.attrs.get("href")
        ### Check if pdf link
        if "pdf" in str(href):
            print(f"{BLUE}[!] PDF link: {href}{BLUE}")
            urls_pdf.add(href)
            continue
        if "doc" in str(href):
            print(f"{BLUE}[!] DOC link: {href}{BLUE}")
            urls_doc.add(href)
            continue
        if ".jpg" in str(href) or ".png" in str(href):
            print(f"{BLUE}[!] IMG link: {href}{BLUE}")
            urls_doc.add(href)
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
            if href not in external_urls:
                print(f"{GRAY}[!] External link: {href}{RESET}")
                external_urls.add(href)
            continue
        print(f"{GREEN}[*] Internal link: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)
    return urls
    
def get_html_every_url(urls):
    for url in urls:
        html_page = urllib.request.urlopen(url)
        soup = BeautifulSoup(html_page, "lxml")       

urls_visited = 0
def crawl(url, max_urls=30):
    global urls_visited
    urls_visited += 1
    print(f"{YELLOW}[*] Crawling: {url}{RESET}")
    links = get_links(url) ## Hinterlegen, auf welcher Seite gecrawlet wurde
    ### DICT
    ###["www.math.kit.edu" : {"https://www.math.kit.edu/#KITsecTermine", "link3", "linkx"}]
    ###["https://www.math.kit.edu/#KITsecTermine" : {"link2", "link34", "linkx"}]
    for link in links:
        try:
            if urls_visited > max_urls:
                break
            crawl(link, max_urls=max_urls)
        except HTTPError as e:
            print(e)
            continue


if __name__ == "__main__":
    crawl(url, max_urls=40)
    print(internal_urls)
    print("[+] Total Internal links:", len(internal_urls))
    print("[+] Total PDF links:", len(urls_pdf))
    print("[+] Total DOC links:", len(urls_doc))
    print("[+] Total External links:", len(external_urls))
    print("[+] Total URLs:", len(external_urls) + len(internal_urls))
    print("[+] Total crawled URLs:", urls_visited)
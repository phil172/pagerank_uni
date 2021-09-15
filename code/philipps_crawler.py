import itertools
from bs4 import BeautifulSoup
import requests, ssl
from urllib.request import Request, urlopen
import urllib, colorama
from urllib.parse import urlparse, urljoin
from urllib.error import HTTPError

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
    def __init__(self, id, url, title, no_links, content, link_urls):
        self.id = id
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
        urls = set()
        title = ""
        no_links = ""
        id = self.get_id()
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
            #print(f"{GREEN}[*] Internal link: {href}{RESET}")
            urls.add(href)
        no_links = len(urls)
        title = soup.title.string
        toReturn = Page(id, url, title,  no_links, content, urls)
        return toReturn

def Run():
    cr = Crawler(url)
    print(cr.url)
    page = cr.get_page()
    links = page.link_urls
    print(links)
    for link in links:
        cr = Crawler(link)
        print(cr.url)
        page = cr.get_page()
        print(page.url)
        print(page.id)

cr = Crawler(url)
print(cr)
print("1", cr.url)
page = cr.get_page()
print("1 page.url: ", page.url)
dr = Crawler("https://www.math.kit.edu/vvz/seite/vvzzukunft/de")
print("2", dr.url)
page2 = dr.get_page()
print("2 page.url: ", page2.url)
cr = Crawler("https://www.math.kit.edu/vvz/seite/vvzzukunft/de")
print("2 ", cr.url)
page3 = cr.get_page()
print("3 page.url: ", page3.url)






# new_dict = dict()
# new_dict[page.url]=list(page.link_urls)
# for i in range(0, 5):#page.no_links):
#     next_url = new_dict[page.url][i]
#     dr = Crawler(next_url)
#     print(next_url)
#     page = dr.get_page()
#     print(page.url)
#     new_dict[page.url] = list(page.link_urls)

#print(new_dict)
# spoler = IdSpooler()
# lst = []
# for i in range(0,4):
#     i +=1
#     page = cr.get_page()
#     print(page.url)
#     lst.append(page)
# print(lst[0].url)
# print(lst[1].url)
# print(lst[2].url)
# print(lst[3].url)


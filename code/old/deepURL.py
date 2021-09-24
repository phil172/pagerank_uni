import requests, ssl
import pandas as pd
from lxml import html
from urllib.parse import urljoin
import itertools, urllib
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
url = "https://www.math.kit.edu/"

ssl._create_default_https_context = ssl._create_unverified_context

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

class DeepCrawler:
    def __init__(self, start_page):
        self.visited_url = {}
        self.queue_url = [start_page]

    def get_page(self):
        ### IF URL IN SET -> CONTINUE (Seiten nicht doppelt herunterladen)
        url = self.url
        urls = list()
        title = ""
        no_links = ""

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
            urls.append(href)
        no_links = len(urls)
        title = soup.title.string
        toReturn = Page(id, url, title,  no_links, content, urls)
        return toReturn

    def get_url_list(self, url):
        print('crawling: %s'%(url))
        
        try:
            url = url.lower()
            response = requests.get(url, timeout=10.0)
            raw_html = response.text
            parsed_html = self.page.content()
        except:
            return
        
        url_title_item = parsed_html.xpath('//title')
        url_title = '(NO TITLE)'
        try:
            url_title = url_title_item[0].text
        except:
            url_title = '(ERROR TITLE)'
        self.visited_url[url] = url_title
    
        for a in parsed_html.xpath('//a'):
            raw_url = a.get('href')
            if raw_url is None:
                continue
            
            parsed_url = urljoin(url, raw_url)
            if parsed_url not in list(self.visited_url.keys()) and parsed_url not in self.queue_url:
                self.queue_url.append(parsed_url)
    
    def output_result(self):
        result = pd.DataFrame()
        urls = list(self.visited_url.keys())
        titles = list(self.visited_url.values())
        
        result['TITLE'] = titles
        result['URL'] = urls
        
        result.to_csv('result.csv', encoding='utf-8-sig')
        
    def start_crawling(self, threshold=-1):
        while threshold is not 0:
            this_url = self.queue_url[0]
            self.get_url_list(this_url)
            
            if len(self.queue_url) == 1:
                break
            else:
                self.queue_url = self.queue_url[1:]
                
            threshold -= 1
        
        self.output_result()
        print('DONE!')
        
        
        
myCrawler = DeepCrawler(url)
myCrawler.start_crawling(threshold=25)
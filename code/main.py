### PageRanke Algorithm ###
## https://towardsdatascience.com/pagerank-3c568a7d2332 ##

from __future__ import division
from io import StringIO
from bs4 import BeautifulSoup
import requests, ssl
from urllib.request import Request, urlopen
import urllib, colorama
from urllib.parse import urlparse, urljoin
from urllib.error import HTTPError
import json
#from cgi import escape
import sys
import os
import math
import string
import operator 
import codecs
import copy
import re

__version__ = "0.1"

STOPWORDS = ["und", "ist"]
DEBUG_FLG = True
AGENT = AGENT = "%s/%s" % (__name__, __version__)
ssl._create_default_https_context = ssl._create_unverified_context

# init the colorama module
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW
BLUE = colorama.Fore.BLUE

### Page ID
class Uid():
    ### Constructor
    def __init__(self, start=0):
        self.nextid = start

    ### Next ID
    def getNext(self):
        idToReturn = self.nextid
        self.nextid += 1
        return idToReturn

    ### Get largest (last) ID
    def getLargest(self):
        return self.nextid

class Page():
    def __init__(self, uid, url, nr_links="", title=""):
        # Unique ID
        self.uid = uid
        # url
        self.url = url
        # title
        self.title = title
        # number of links
        self.nr_links = ""
        # page content
        self.content = ""
        # pages this links to
        self.linkUrls = set([])
        # (url, anchor) pairs this links to
        self.links = []
        # PageRank of this page
        self.pageRank = 0.0
        # Terms of anchors pointing to this page
        self.incomingTerms = []


    ### Get Item

    def __getitem__(self, x):
        return self.urls[x]

    # add a link (which is url and anchor)
    def addLink(self, url, anchor):
        if url not in self.linkUrls:
            self.links.append((url, anchor))
            self.linkUrls.add(url)
    ### ?????
    def addIncomingTerms(self, termList):

        termList = map(lambda x: x.lower(), termList)
        print("first ")
        termList = filter(lambda x: (x not in STOPWORDS), termList)
        print("second")
        self.incomingTerms.extend(termList)
        print("extend")

    def isDeadend(self):
        if len(self.links) == 0:
            return True
        elif (len(self.links) == 1) and (self.links[0][0] == self.url):
            return True
        else:
            return False

    def getTitle(self):
        if not self.title:
            return '<No Title>'
        else:
            return self.title
    # def getIndexRecord(self):
    #     return PageIndexRecord(self.title, self.incomingTerms)

    def savePage(self):
        filename = "pages/" + str(self.uid) + '.html'
        clean_content = str(self.content)
        clean_content = clean_content.replace('\n', '')
        with open(filename, 'w') as f:
            f.write(clean_content)
            if DEBUG_FLG:
                print('page', self.uid, 'saved as', filename)

class WebCrawler():
    def __init__(self, seeldUrls = []):
        self.pages = {}
        self.urls = set()
        self.spooler = Uid()

    def is_valid(url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)


    def right_link(self, href):
        url = href
        if url[:25] != "https://www.math.kit.edu/":
            return False
        if "pdf" in str(url):
            return False
        if "doc" in str(url):
            return False
        if "jpg" in str(url) or ".png" in str(url):

            return False
        else:
            return True

    def openRequest(self, url):
        try:
            request = urllib.request.Request(url)
            handle = urllib.request.build_opener()
        except IOError:
            return None
        return request, handle

    def addHeaders(self, request):
        request.add_header("User-Agent", AGENT)

    def fetchPage(self, url):
        if url in self.pages:
            return self.pages[url]
        uid = self.spooler.getNext()
        toReturn = Page(uid, url)
        request, handle = self.openRequest(url)
        self.addHeaders(request)
        if handle:
            try:
                toReturn.content = handle.open(request).read()
                soup = BeautifulSoup(toReturn.content, features="lxml")
                toReturn.title = str(soup.html.head.title)
                links = soup('a')   
                if DEBUG_FLG:
                    print("page has ", len(links), " links.")    
            except HTTPError as e:
                print(e)

        ### process links
            for link in links:
                if not link:
                    continue
                href = link.attrs.get("href")
                anchor = str(link)
                if not anchor:
                    anchor = " "
                if not href:
                    continue
                ###Check if pdf, dod, img or external link
                fullHref = str(urljoin(url, href)) #escape(href)
                fullHref = fullHref.replace('\n', '')
                if self.right_link(fullHref):# and fullHref in self.urls:
                    toReturn.addLink(fullHref, anchor)
                    #print(anchor, "----->", fullHref)
            return toReturn


    def savePages(self):
        for page in self.pages.values():
            page.savePage()

    def crawl(self, urllist=None):
        if urllist:
            self.urls = set(urllist)
        else:
            print("NOT URLLIST")
        for url in self.urls:
            self.pages[url] = self.fetchPage(url)
            if DEBUG_FLG:
                print('Successfully fetched', url)
            self.pages[url].savePage()
        print("''''''''''###########''''''''''''''")
        print(self.pages[url].linkUrls)
        print(type(self.pages[url].linkUrls))
        print(len(self.pages[url].linkUrls))
        print("''''''''''###########''''''''''''''")
        if DEBUG_FLG:
            print("*****************")
            print("Finished Fetching!")
        print(self.pages.items())
        print(type(self.pages))   
        for url, page in self.pages.items():
            for (href, anchor) in page.links:
                if href and anchor:
                    terms = anchor.lower().split()
                    print("terms")
                    print(type(self.pages[href]))
                    self.pages[href].addIncomingTerms(terms)
                    print("addincomingtermns")

class PageIndexRecord:
    def __init__(self, title, anchors=None):
        self.title = title
        self.anchors = anchors

    def addAnchor(self, anchorString):
        self.anchors.append(anchorString)

    def setTitle(self, title):
        self.title = title


def Run():
    lst = ["https://www.math.kit.edu/"]
    crawler = WebCrawler()
    crawler.crawl(lst)

Run()
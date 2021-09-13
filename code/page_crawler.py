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

###
"https://www.thepythoncode.com/article/extract-all-website-links-python"
###

### STOPWORDS (Words that aren't specific enough)
STOPWORDS = set(['and', 'is', 'it', 'an', 'as', 'at', 'have', 'in', 'its', 'are', 
	'said', 'from', 'for', 'to', 'been', 'than', 'also', 'other', 'which', 'new', 
	'has', 'was', 'more', 'be', 'we', 'that', 'of', 'but', 'they', 'not', 'with', 
	'by', 'a', 'on', 'this', 'could', 'their', 'these', 'can', 'the', 'or', 'first'])

DEBUG_FLG = True
VERBOSE_FLG = False
alpha = 0.15
CONVERGE_ERROR = 0.00001

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

    ### Get largest (last) ID
    def getLargest(self):
        return self.nextid

### URL and SSL
class Page():
    def __init__(self, uid, url, title=""):
        # Unique ID
        self.uid = uid

        # url
        self.url = url

        # title
        self.title = title

        # page content
        self.content = ""

        # pages this links to
        self.linkURls = set([])

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
        termList = filter(lambda x: (x not in STOPWORDS), termList)
        self.incomingTerms.extend(termList)

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
    def getIndexRecord(self):
        return PageIndexRecord(self.title, self.incomingTerms)

    def savePage(self):
        filename = "pages/" + str(self.uid) + '.html'
        with open(filename, 'w') as f:
            f.write(self.content)
            if DEBUG_FLG:
                print('page', self.uid, 'saved as', filename)


class Crawler:
    def __init__(self, seedUrls=[]):
        self.pages = {}
        self.urls = set(seedUrls)
        self.spooler = Uid()

    def validateUrl(self, url):
        return url in self.urls

    ### excluding docs, pdfs, img and external urls
    def standardLink(self, href):
        test = href
        if test[:26] != "https://www.math.kit.edu/":
            return False
        elif string.find(href, "pdf") > -1:
            return False
        elif string.find(href, "doc") > -1:
            return False
        elif string.find(href, "img") > -1:
            return False
        else:
         return True

    ### clean an url:
    def sanitizeUrl(self, url):
        url = str(url)
        if url[-10:] == "index.html":
            return url[:-10]

        hashIndex = string.find(url, "#")
        if hashIndex > -1:
            realUrl = url[0:hashIndex]
            return realUrl
        return url

    def is_valid(self, url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def right_link(self):
        if "pdf" in str(self):
            print(f"{BLUE}[!] PDF link: {self}{BLUE}")
            return False
        if "doc" in str(self):
            print(f"{BLUE}[!] DOC link: {self}{BLUE}")
            return False
        if ".jpg" in str(self) or ".png" in str(self):
            print(f"{BLUE}[!] IMG link: {self}{BLUE}")
            return False
        else:
            return True

    def requestPage(self, url):
        try:
            request = urllib.request.urlopen(url)
            handle = urllib.request.build_opener()
        except IOError:
            return None
        print("HANDLE", handle)
        return (request, handle)

    def fetchPage(self, url):
        if url in self.pages:
            return self.pages[url]
        uid = self.spooler.getNext()
        toReturn = Page(uid, url)
        request, handle = self.requestPage(url)
        self.addHeaders(request)
        if handle:
            try:
                toReturn.content = handle.open(request).read()
                soup = BeautifulSoup(toReturn.content)
                toReturn.title = soup.html.head.title.string
                links = soup("a")
                print("Page has ", len(links), " links!")
            except HTTPError as e:
                print(e)


        ## processing links
            for link in links:
                if not link.right_link():
                    print("notright link")
                    continue
                if not link:
                    continue
                href = link.get("href")
                anchor = link.string
                if not anchor:
                    anchor = " "
                if not href:
                    continue

                href = self.sanitizeUrl(href)
                fullHref = str(urlparse.urljoin(url, href))
                fullHref = string.replace(fullHref, '\n', '')
                if self.standardLink(fullHref) and fullHref in self.urls:
                    toReturn.addLink(fullHref, anchor)
                    if DEBUG_FLG and VERBOSE_FLG:
                        print("---> linked to ", fullHref)
            return toReturn

        ### save pages
    def savePages(self):
        for page in self.pages.itervalues():
            page.savePage()

    def crawl(self, urllist=None):
        if urllist:
            self.urls = set(urllist)
        print(self.urls)
        for url in self.urls:
            self.pages[url] = self.fetchPage(url)
            if DEBUG_FLG:
                print("successfully fetched ", url)
            self.pages[url].savePage()
        if DEBUG_FLG:
            print("************")
            print("finished fetching!")

        for url, page in self.pages.items():
            for (href, anchor) in page.links:
                if href and anchor:
                    terms = anchor.lower().split()
                    self.pages[href].addIncomingTerms(terms)

class PageIndexRecord:
    pass

def openUrlFile(filename="url.txt"):
    if DEBUG_FLG:
        print('opening', filename)
    urls = []
    with open(filename, 'r') as f:
        for line in f:
            urls.append(str.replace(line, '\n', ''))
        return urls

crawler = Crawler(openUrlFile())
crawler.crawl()
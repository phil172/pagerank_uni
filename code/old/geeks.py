from bs4 import BeautifulSoup
import requests, ssl, urllib
from urllib.parse import urlparse

site="https://www.math.kit.edu/"
ssl._create_default_https_context = ssl._create_unverified_context
# lists
urls=[]
queue=["https://www.math.kit.edu/"]

# function created
def scrape(queue: list):
    # getting the request from url
    site = queue[0]
    print("SCRAPING: ", site)
    domain_name = urlparse(site).netloc
    html_page = urllib.request.urlopen(site)
    s = BeautifulSoup(html_page, "lxml")       
       
    for i in s.find_all("a"):
        href = i.attrs.get("href")
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
            # external link
            continue
        # if href.startswith("/"):
        #     site = site+href
        if href not in  urls:
            queue.append(href)
    print(len(queue))
    queue = queue[1:]
    if queue[0] not in urls:     
        urls.append(queue[0])   
    # calling it self
    scrape(queue)
   
# main function

   
# website to be scrape


# calling function
scrape(queue)
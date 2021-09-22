from tqdm import tqdm
from time import sleep
import urllib
import requests, ssl
from urllib.request import urlopen
from urllib.parse import urljoin
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import requests
import colorama
from functools import cached_property
import config


'''Colorama Module'''
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW
BLUE = colorama.Fore.BLUE
RED = colorama.Fore.RED

'''Base Url'''
base_url = "https://www.math.kit.edu/"
ssl._create_default_https_context = ssl._create_unverified_context
new_links = []
links_visited: list = ["https://www.math.kit.edu/"]
url_dict = {}

'''First Iteration'''

def first_it(base_url):
    print(f"{BLUE}[*][*][*][*]-- Crawling: {base_url} --[*][*][*][*]{RESET}")
    domain_name = urlparse(base_url).netloc
    html_page = urllib.request.urlopen(base_url)
    soup = BeautifulSoup(html_page, "lxml")
    body = soup.find('body')
    href_tags = body.find_all(href=True)   
    all_links = list(set([tag.get('href') for tag in href_tags]))
    all_internal_links = [x for x in all_links if domain_name in x]
    url_dict[base_url] = all_internal_links
    for link in all_internal_links:
        if link in links_visited:
            continue
        new_links.append(link)
    config.cache[base_url] = all_internal_links
    return all_links, new_links

i = 0
all_links, new_links = first_it(base_url)
for link in tqdm(new_links, ncols = 100):
    if link in links_visited:
        continue
    while i < 20:
        i += 1
        first_it(link)

print(url_dict)
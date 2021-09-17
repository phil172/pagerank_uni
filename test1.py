class Page:
    '''
    Constructor
    '''
    anzahl = 10
    def __init__(self, url, title, no_links, content, link_urls):
        self.url = url
        self.title = title
        self.no_links = no_links
        self.link_urls = link_urls
        self.page_rank = 0.0
        self.content = content


seite = Page("www.url.de", "test", 2, "sasdasd", "wasdasdasd")

print(seite)
seite.anzahl = 20
print(seite.anzahl)
from bs4 import BeautifulSoup
import ssl
from urllib.request import urlopen
base_url = "https://www.math.kit.edu/"
ssl._create_default_https_context = ssl._create_unverified_context

class HtmlImport():
    def __inti__(self):
        self.text = self.getText()
        self.soup = self.getSoup()

    def getSoup(self):
        with open("pages/1.html") as html_file:
            soup = BeautifulSoup(html_file, features="html.parser")
            return soup
    # url = base_url
    # html = urlopen(url).read()
    # soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
        
    def getText(self):
        soup = self.soup
        # get text
        for script in soup(["script", "style"]):
            script.extract()    # rip it out
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text
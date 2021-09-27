from bs4 import BeautifulSoup
import ssl
base_url = "https://www.math.kit.edu/"
ssl._create_default_https_context = ssl._create_unverified_context

### Nur Text importieren

from urllib.request import urlopen
from bs4 import BeautifulSoup

url = base_url
html = urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

# get text
text = soup.get_text()

# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)

a = text.find("Mathematik")
print(text[a:])
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import *
from searchhtml import HtmlImport
import os, re

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PageRank for math.kit.edu'
        self.left = 50  
        self.top = 50   
        self.width = 500
        self.height = 1000
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(460,20)
        
        # Create a button in the window
        self.button = QPushButton('Search', self)
        self.button.move(200,100)

        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show() 

    @pyqtSlot()
    def on_click(self):
        searchterm = self.textbox.text()
        h = HtmlImport("pages/9.html")
        text: str = h.get_text_string()
        text = text.lower()
        results = [m for m in re.finditer(searchterm, text)]
        spans = []
        if len(results) > 0:
            for el in results:
                spans.append(el.span())
        self.results_window.setText(spans)
        self.textbox.setText("")

def render(url):
    """Fully render HTML, JavaScript and all."""

    import sys
    from PyQt5.QtCore import QEventLoop,QUrl
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtWebEngineWidgets import QWebEngineView

    class Render(QWebEngineView):
        def __init__(self, url):
            self.html = None
            self.app = QApplication(sys.argv)
            QWebEngineView.__init__(self)
            self.loadFinished.connect(self._loadFinished)
            self.load(QUrl(url))
            while self.html is None:
                self.app.processEvents(QEventLoop.ExcludeUserInputEvents | QEventLoop.ExcludeSocketNotifiers | QEventLoop.WaitForMoreEvents)
            self.app.quit()

        def _callable(self, data):
            self.html = data

        def _loadFinished(self, result):
            self.page().toHtml(self._callable)

    return Render(url).html


print(render("https://www.math.kit.edu/"))

all_pages = os.listdir("pages")




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
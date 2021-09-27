# main.py
import sys
import os
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, pyqtSlot

from bs4 import BeautifulSoup


class Browser(QtWebEngineWidgets.QWebEngineView):

    def __init__(self):
        super().__init__()
        self.soup = self.get_soup()
        self.text = self.get_text_string()
        html = self.get_result()

        here = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
        base_path = os.path.join(os.path.dirname(here), 'dummy').replace('\\', '/')
        self.url = QtCore.QUrl('file:///' + base_path)
        self.page().setHtml(html, baseUrl=self.url)

    def get_soup(self):
        with open("pages/1.html") as html_file:
            soup = BeautifulSoup(html_file, features="html.parser")
            result = soup.find_all("div")
            return soup

    def get_result(self):
        with open("pages/1.html") as html_file:
            soup = BeautifulSoup(html_file, features="html.parser")
            result = str(soup)
            return result

    def get_text_string(self):
        soup = self.soup
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

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_widgets()
        self.init_layout()

    def init_widgets(self):
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(460,20)
        self.browser = Browser()
        self.browser.move(100, 100)
        self.browser.loadFinished.connect(self.load_finished)


    def init_layout(self):
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.browser)

        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def load_finished(self, status):
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setWindowTitle('Load Status')
        self.msg.setText(f"It is {str(status)} that the page loaded.")
        self.msg.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
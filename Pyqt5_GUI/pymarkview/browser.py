import webbrowser
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *
import os

class WebEnginePage(QWebEnginePage):
    def acceptNavigationRequest(self, url, navtype, mainframe):
        return False


class Browser(QWebEngineView):
    PMV_LINK_PREFIX = "pmv://"

    pmv_link_clicked = pyqtSignal(str)

    def __init__(self):
        self.view = QWebEngineView.__init__(self)
        self.setPage(WebEnginePage(self))
        self.page().acceptNavigationRequest = self.handle_link_click
        self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.FocusOnNavigationEnabled, False)
        self.loadStarted.connect(self.handle_load_started)
        self.loadFinished.connect(self.handle_load_finished)

    def load_html(self, html):
        self.setHtml(html, baseUrl=QUrl.fromLocalFile(os.getcwd()+os.path.sep))

    def load_url(self, url):
        self.setUrl(QUrl(url))

    def enable_javascript(self, state):
        self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, state)

    def handle_load_started(self):
        self.scroll_position = self.page().scrollPosition()

    def handle_load_finished(self):
        self.page().runJavaScript(
            f"window.scrollTo({self.scroll_position.x()}, {self.scroll_position.y()});"
        )

    def handle_link_click(self, url, navtype, mainframe):
        url = url.toString()

        if not url.startswith(self.PMV_LINK_PREFIX):
            webbrowser.open(url)
        else:
            self.pmv_link_clicked.emit(url[len(self.PMV_LINK_PREFIX):])

        return False

    @classmethod
    def demo(cls):

        class Example(QWidget):

            def __init__(self):
                super().__init__()
                use_my_md = False
                if use_my_md:
                    from Pyqt5_GUI.pymarkview.markdown import Markdown
                    md = Markdown()
                    self.md = md.parse
                else:
                    from markdown2 import Markdown
                    self.md = Markdown(extras=["fenced-code-blocks", "cuddled-lists", "code-friendly"]).convert
                self.initUI()

            def initUI(self):
                browser = Browser()

                hbox = QHBoxLayout()
                hbox.addStretch(1)
                hbox.addWidget(browser)

                self.setLayout(hbox)
                welcome_text = """ PyMarkView
===

Overview
---

Supports **bold**, *italic* and ***bold-italic***!
Inline `code` is possible, too!

Images can be inserted using drag and drop or the corresponding MD syntax.

```
#include<stdio.h>
int main() {
    printf("Hello world!\n");
}
```

> A famous quote!
> Multiline!

* Unordered
* foo

1. Ordered
2. bar

###### I am a tiny header!

Types of links: <https://github.com/> [GitHub](https://github.com/)

CLI usage
---

`$ pymarkview -i "input.md" -o "output.html"`

Show Image
---

![asd](https://pics5.baidu.com/feed/023b5bb5c9ea15ceaa1406dc8e9e8bfa3887b291.jpeg?token=fb36dc59a25964bcaf4f4866545f5504)
![asd](https://img.php.cn/upload/article/202103/09/2021030915055928798.jpg)
![asd](../../data/temp.png)
                 """
                stylesheet = '''<style>
                body {
                    font-family: sans-serif;
                }

                h1.alt, h2.alt {
                    border-bottom: 1px solid #eee;
                }

                hr {
                    border: 0;
                    border-top: 1px solid #eee;
                }

                blockquote {
                    margin-left: 0;
                    padding-left: 10px;
                    border-left: 4px solid #dfe2e5;
                }

                code {
                    background: #f6f8fa;
                    border-radius: 3px;
                    padding: 2px;
                }

                pre {
                    background: #f6f8fa;
                    padding: 16px;
                    border-radius: 3px;
                }

                img {
                  max-width: 50%;
                  vertical-align: middle;
                }
                </style>
                '''
                # a=QFileInfo('./temp.png')
                # print(a.absoluteFilePath())
                mathjax = '''<script async type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.2/MathJax.js?config=TeX-MML-AM_CHTML"></script>'''
                html_md = self.md(welcome_text)
                html_md += stylesheet
                html_md += mathjax
                # print(html_md)
                browser.load_html(html_md)

                a = QUrl.fromLocalFile(os.path.join(os.getcwd(),'temp.png'))
                # index_file = QFileInfo(r'E:\my_projects\coolbeam.github.io\docs\index.html').absoluteFilePath()

                # browser.load(a)
                # browser.load(QUrl(r'E:\my_projects\coolbeam.github.io\docs\index.html'))
                self.setGeometry(30, 30, 900, 900)
                self.setWindowTitle('browser')
                self.show()

        app = QApplication(sys.argv)
        ex = Example()
        sys.exit(app.exec_())


if __name__ == '__main__':
    import sys

    Browser.demo()

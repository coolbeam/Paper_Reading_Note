# -*- coding: utf-8 -*-

"""
这是一个极简图书管理（QTableWidget的使用）的例子！
文章链接：http://www.xdbcb8.com/archives/779.html
文章链接：http://www.xdbcb8.com/archives/784.html
文章链接：http://www.xdbcb8.com/archives/795.html
文章链接：http://www.xdbcb8.com/archives/814.html
"""

import requests
from PIL import Image
from io import BytesIO
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap
from Pyqt5_GUI.Library_manager_example.Ui__bookinfoUI import Ui_Dialog
from Pyqt5_GUI.Library_manager_example.getbookinfo import GetBookInfo
from Pyqt5_GUI.Library_manager_example.datamanagement import DataManagement

class CreateBook(QDialog, Ui_Dialog):
    """
    创建图书档案
    """ 
    def __init__(self, parent=None):
        """
        初始化图书信息以及设定一些界面参数
        """
        super(CreateBook, self).__init__(parent)
        self.setupUi(self)
        self.initUi()
        self.isbn = ""
        self.subtitle = ""
        self.author = ""
        self.pubdate = ""
        self.classification = ""
        self.publisher = ""
        self.price = ""
        self.pages = ""
        self.summary = ""
        self.img = ""
        self.country = ""
        self.header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36"
        }

    def initUi(self):
        '''
        一些基本设置
        '''
        classifications = ["", "马克思主义、列宁主义、毛泽东思想、邓小平理论", "哲学、宗教", "社会科学总论", 
                    "政治、法律", "军事", "经济", "文化、科学、教育、体育", "语言、文字", "文学", 
                    "艺术", "历史、地理", "自然科学总论", "数理科学和化学", "天文学、地球科学", "生物科学", 
                    "医药、卫生", "农业科学", "工业技术", "交通运输", "航空、航天", "环境科学、劳动保护科学（安全科学）", 
                    "综合性图书"]
        self.comboBox.addItems(classifications)
        #将comboBox增加图书类型

    @pyqtSlot()
    def on_pushButton_read_clicked(self):
        """
        读取图书信息
        """
        self.isbn = self.lineEdit_isbn.text()
        if self.isbn == "":
            QMessageBox.warning(self, "警告", "ISBN号为空")
            self.lineEdit_isbn.setFocus()
            # 读取ISBN号的时候，首先判断下是不是为空，要是为空则弹出警告对话框
        else:
            book = GetBookInfo(self.isbn)
            rstatus, bookinfo = book.getbookinfo()
            # 根据ISBN号去获取豆瓣API上的图书信息，rstatus和bookinfo分别表示返回是否成功和图书信息。
            if rstatus == "1":
                self.subtitle = bookinfo["subtitle"]
                self.author = bookinfo["author"]
                self.pubdate = bookinfo["pubdate"]
                self.classification = bookinfo["classification"]
                self.publisher = bookinfo["publisher"]
                self.price = bookinfo["price"]
                self.pages = bookinfo["pages"]
                self.summary = bookinfo["summary"]
                self.img = bookinfo["img"]
                self.country = bookinfo["country"]
                self.set_bookinfo(self.subtitle, self.author, self.pubdate, self.classification, self.publisher, self.price, self.pages, self.summary, self.img)
            else:
                QMessageBox.warning(self, "警告", "大兄dei貌似查不到哦")
                self.lineEdit_isbn.setFocus()

    @pyqtSlot()
    def on_pushButton_chioce_clicked(self):
        """
        图书封面选择
        """
        f = QFileDialog.getOpenFileName(self, "选择图书封面", "./res/book/", ("Images (*.png *.jpg)"))
        if f[0]:
            self.label_pic.setPixmap(QPixmap(f[0]))
            self.img = f[0]

    def accept(self):
        """
        点击确认后
        ISBN号、书名、作者不能为空。然后将取得的图书信息利用self.get_bookinfo()放入到book这个字典中
        """
        if self.lineEdit_isbn.text() == "":
            QMessageBox.information(self, "提示", "ISBN号为空！")
        elif self.lineEdit_bookname.text() == "":
            QMessageBox.information(self, "提示", "书名为空！")
        elif self.lineEdit_author.text() == "":
            QMessageBox.information(self, "提示", "作者为空！")
        else:
            isbn = self.lineEdit_isbn.text()
            subtitle = self.lineEdit_bookname.text()
            author = self.lineEdit_author.text()
            pubdate = self.lineEdit_pudate.text()
            classification = self.comboBox.currentText()
            publisher = self.lineEdit_publisher.text()
            price = self.lineEdit_price.text()
            pages = self.lineEdit_pages.text()
            summary = self.textEdit_content.toPlainText()
            img = self.img
            country = self.country
            book = self.get_bookinfo(isbn, subtitle, author, pubdate, classification, publisher, price, pages, summary, img, country)
            dm = DataManagement()
            r = dm.insert_db(book)
            if r > 0:
                self.done(1)
            else:
                QMessageBox.information(self, "提示", "新增图书失败，貌似已经有相同的ISBN图书存在了！")
            # 利用dm.insert_db(book)把图书信息存入“book.dat”中，同时返回1；要是存入不成功那么就提示有相同的ISBN号。
    
    def reject(self):
        """
        点击取消后
        """
        self.done(-1)
    
    def set_bookinfo(self, subtitle, author, pubdate, classification, publisher, price, pages, summary, img):
        """
        设置图书信息
        """
        self.lineEdit_bookname.setText(subtitle)
        self.lineEdit_author.setText(author)
        self.comboBox.setEditText(classification)
        self.lineEdit_publisher.setText(publisher)
        self.lineEdit_pudate.setText(pubdate)
        self.lineEdit_pages.setText(pages)
        self.lineEdit_price.setText(price)
        self.textEdit_content.setPlainText(summary)

        imgname = './res/book/' + img.split("/")[-1]
        response = requests.get(img, headers=self.header)
        #获取图书信息
        image1 = Image.open(BytesIO(response.content))
        image1.save(imgname)
        self.label_pic.setPixmap(QPixmap(imgname))
        #获取图书封面

    def get_bookinfo(self, isbn, subtitle, author, pubdate, classification, publisher, price, pages, summary, img, country):
        """
        返回图书信息
        """
        book = {"isbn" : isbn, "subtitle" : subtitle, "author" : author, "pubdate" : pubdate, "classification" : classification, 
                "publisher" : publisher, "price" : price, "pages" : pages, "summary" : summary, "img" : img, "country" : country
                }
        return book
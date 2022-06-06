# -*- coding: utf-8 -*-

"""
这是一个极简图书管理（QTableWidget的使用）的例子！
文章链接：http://www.xdbcb8.com/archives/779.html
文章链接：http://www.xdbcb8.com/archives/784.html
文章链接：http://www.xdbcb8.com/archives/795.html
文章链接：http://www.xdbcb8.com/archives/814.html
"""

import pickle
import codecs
import os

class DataManagement:
    """
    数据操作类
    """
    books = []

    def insert_db(self, bookinfo):
        """
        新增一条图书记录
        """
        self.books = self.load()
        for book in self.books:
            if book["isbn"] == bookinfo["isbn"]:
                return -1
        else:
            self.books.append(bookinfo)
            with codecs.open("book.dat", "wb") as f:
                pickle.dump(self.books, f)
            return 1

    def save_db(self, bookinfo):
        """
        保存所有图书档案
        """
        with codecs.open("book.dat", "wb") as f:
            pickle.dump(bookinfo, f)

    def query_db(self, isbn="", author="", bookname=""):
        """
        查找某本书
        """
        self.books = self.load()
        if isbn:
            # 按照isbn查找
            for i, book in enumerate(self.books):
                if book["isbn"] == isbn:
                    return i
            else:
                return -1
        if author:
            # 按照作者查找
            for i, book in enumerate(self.books):
                if book["author"] == author:
                    return i
            else:
                return -1
        if bookname:
            # 按照书名查找
            for i, book in enumerate(self.books):
                if book["subtitle"] == bookname:
                    return i
            else:
                return -1            

    def load(self):
        """
        载入数据
        """
        pathname = "book.dat"

        if not(os.path.exists(pathname) and os.path.isfile(pathname)):
            with codecs.open("book.dat", "wb") as f:
                pickle.dump(self.books, f)
            #要是没有book.dat我们就建一个

        with codecs.open("book.dat", "rb") as f:
            books = pickle.load(f)
        return books
        # 返回books对象
# -*- coding: utf-8 -*-

"""
这是一个极简图书管理（QTableWidget的使用）的例子！
文章链接：http://www.xdbcb8.com/archives/779.html
文章链接：http://www.xdbcb8.com/archives/784.html
文章链接：http://www.xdbcb8.com/archives/795.html
文章链接：http://www.xdbcb8.com/archives/814.html
"""

import sys
from Pyqt5_GUI.Library_manager_example.mbook import Mbook
from Pyqt5_GUI.Library_manager_example.createbook import CreateBook
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mb = Mbook()
    mb.show()
    sys.exit(app.exec_())
# -*- coding: utf-8 -*-

"""
这是一个关于TIM模拟（QTreeWidget）的例子！
文章链接：http://www.xdbcb8.com/archives/737.html
文章链接：http://www.xdbcb8.com/archives/740.html
文章链接：http://www.xdbcb8.com/archives/753.html
文章链接：http://www.xdbcb8.com/archives/757.html
文章链接：http://www.xdbcb8.com/archives/762.html
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMessageBox
from Pyqt5_GUI.TIM_like_list.Ui_additem_ui import Ui_Dialog

class Dialog_additem(QDialog, Ui_Dialog):
    """
    新增联系人对话框
    """
    def __init__(self, parent=None):
        """
        一些初始设置
        """
        super(Dialog_additem, self).__init__(parent)
        self.setupUi(self)
        self.flag = False# 判断返回的联系人图标是默认的还是自定义的
        self.iconpath = ''
    
    @pyqtSlot(bool)
    def on_radioButton_toggled(self, checked):
        """
        默认联系人图标
        """
        self.flag = False
        if self.pushButton.isEnabled() == True:
            self.pushButton.setEnabled(False)
    
    @pyqtSlot(bool)
    def on_radioButton_2_toggled(self, checked):
        """
        自定义联系人图标
        """
        self.flag = True
        if self.pushButton.isEnabled() == False:
            self.pushButton.setEnabled(True)
    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        选择图标
        """
        fname = QFileDialog.getOpenFileName(self, '打开文件', './res/user/', ("Images (*.png *.jpg)"))
        if fname[0]:
            self.iconpath = fname[0]
    
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        新增命令提交
        """
        if len(self.lineEdit.text()) == 0:
            QMessageBox.information(self, '提示', '好友姓名为空')
            self.lineEdit.setFocus()
        else:
            self.done(1)# 给主窗口的返回值
    
    @pyqtSlot()
    def on_buttonBox_rejected(self):
        """
        取消新增
        """
        self.done(-1)

    def geticonpath(self):
        '''
        获得图标路径
        '''
        if self.flag == True:
            return self.iconpath
        else:
            return "./res/user/default.jpg"
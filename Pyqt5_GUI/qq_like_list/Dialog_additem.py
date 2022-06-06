# -*- coding: utf-8 -*-

"""
新增联系人
文章链接：http://www.xdbcb8.com/archives/725.html
"""

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox
from Pyqt5_GUI.qq_like_list.Ui_ui import Ui_Dialog

class Dialog_additem(QDialog, Ui_Dialog):
    """
    Dialog_additem是用Qt设计师画的界面，然后生成对话框代码的。
    """
    def __init__(self, parent=None):
        """
        一些初始设置
        """
        super(Dialog_additem, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(300, 150)
        self.flag = False
        #判断返回的联系人图标是默认的还是自定义的

        self.iconpath = ''
        # 图标路径
    
    @pyqtSlot(bool)
    def on_radioButton_toggled(self, checked):
        """
        默认联系人图标
        """
        self.flag = False
        if self.pushButton.isEnabled() == True:
            self.pushButton.setEnabled(False)
            # 图标选择按钮不可用
    
    @pyqtSlot(bool)
    def on_radioButton_2_toggled(self, checked):
        """
        选择联系人图标
        """
        self.flag = True
        if self.pushButton.isEnabled() == False:
            self.pushButton.setEnabled(True)
            # 图标选择按钮可以用
    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        打开图标文件夹
        """
        fname = QFileDialog.getOpenFileName(self, '打开文件', './res/', ("Images (*.png *.jpg)"))
        if fname[0]:
            self.iconpath = fname[0]
    
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        提交新增联系人
        """
        if len(self.lineEdit.text()) == 0:
            QMessageBox.information(self,'提示','好友姓名为空')
            self.lineEdit.setFocus()
        else:
            self.done(1)#给主窗口的返回值

    
    @pyqtSlot()
    def on_buttonBox_rejected(self):   
        """
        取消新增联系人
        """
        self.done(-1)#给主窗口的返回值

    def geticonpath(self):
        '''
        返回图标路径
        '''
        if self.flag == True:
            return self.iconpath
        else:
            return "./res/default.ico"

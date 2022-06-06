#coding=utf-8

"""
这是一个关于QQ模拟（QListWidget）的例子！
文章链接：http://www.xdbcb8.com/archives/725.html
"""

import random
import Pyqt5_GUI.qq_like_list.Random_Name as Random_Name
from PyQt5.QtWidgets import QListWidget, QMenu, QAction, QMessageBox, QListWidgetItem, QAbstractItemView
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QFont, QBrush
from Pyqt5_GUI.qq_like_list.Dialog_additem import Dialog_additem

class ListWidget(QListWidget):

    '''
    QQ模拟
    '''

    map_listwidget = []
    # map_listwidget保存QListWidget对象和分组名称的对应关系

    def __init__(self):
        '''
        一些初始设置
        '''
        super().__init__()
        self.Data_init()
        self.Ui_init()

    def Data_init(self):
        '''
        数据初始化，随机生成会员红名等功能。
        '''
        randomnum = random.sample(range(26), 10)
        for i in randomnum:
            item = QListWidgetItem()
            randname = Random_Name.getname()
            randicon = "./res/"+ str(i) + ".jpg"
            font = QFont()
            font.setPointSize(16)
            item.setFont(font)
            item.setText(randname)
            flag = random.randint(0, 5)
            if flag == 1:
                item.setForeground(QBrush(Qt.red))
                item.setToolTip('会员红名尊享')
            # 实现随机会员

            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            # 设置联系人名称的对其方式：水平、垂直居中

            item.setIcon(QIcon(randicon))
            self.addItem(item)
            # 给每个联系人设置图标，然后新增到QListWidget当中
    
    def Ui_init(self):
        self.setIconSize(QSize(70, 70))
        self.setStyleSheet("QListWidget{border:1px solid gray; color:black; }"
                        "QListWidget::Item{padding-top:20px; padding-bottom:4px; }"
                        "QListWidget::Item:hover{background:skyblue; }"
                        "QListWidget::item:selected:!active{border-width:0px; background:lightgreen; }"
                        )
        # 界面上的设定

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # 项目选择方式，支持ctrl多选

        self.itemSelectionChanged.connect(self.getListitems)
        # 当选择的项目（联系人）改变时，发出此信号，这里我们返回被选中项目对象的列表
    
    def getListitems(self):
        '''
        返回被选中的项目对象的列表
        '''
        return self.selectedItems()

    def contextMenuEvent(self, event):
        '''
        上下文菜单的函数，与上期相同部分，不注释。
        '''
        hitIndex = self.indexAt(event.pos()).column()
        if hitIndex > -1:
            pmenu = QMenu(self)
            pDeleteAct = QAction("删除", pmenu)
            pmenu.addAction(pDeleteAct)
            pDeleteAct.triggered.connect(self.deleteItemSlot)
            if self is self.find('我的好友'):
                pAddItem = QAction("新增好友", pmenu)
                pmenu.addAction(pAddItem)     
                pAddItem.triggered.connect(self.addItemSlot)
            # 判断一下是否在“我的好友”这个分组单击右键的，否则不会产生新增好友的菜单。

            if len(self.map_listwidget) > 1:
                pSubMenu = QMenu("转移联系人至", pmenu)
                pmenu.addMenu(pSubMenu)
                for item_dic in self.map_listwidget:
                    if item_dic['listwidget'] is not self:
                        # 在遍历分组名称和QListWidget对象字典的时候，会判断下当前要转移的分组是否就是单击右键时分组。
                        pMoveAct = QAction(item_dic['groupname'], pmenu)
                        pSubMenu.addAction(pMoveAct)
                        pMoveAct.triggered.connect(self.move)
            pmenu.popup(self.mapToGlobal(event.pos()))
    
    def deleteItemSlot(self):
        '''
        在删除项目（联系人）的时候，我们根据选择的项目进行删除
        '''
        dellist = self.getListitems()
        for delitem in dellist:
            del_item = self.takeItem(self.row(delitem))
            del del_item

    def addItemSlot(self):
        '''
        新增联系人
        '''
        dg = Dialog_additem()
        r = dg.exec()
        # 这里是执行我们自定义的新增联系人对话框

        if r > 0:
            newitem = QListWidgetItem()
            newname = dg.lineEdit.text()
            newicon = dg.geticonpath()
            font = QFont()
            font.setPointSize(16)
            newitem.setFont(font)
            newitem.setText(newname)
            newitem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            newitem.setIcon(QIcon(newicon))
            self.addItem(newitem)
            #新增联系人

    def setListMap(self, listwidget):
        '''
        把一个分组对象加入到map_listwidget
        '''
        self.map_listwidget.append(listwidget)

    def move(self):
        '''
        获取已选的项目，删除后再增加。
        '''
        tolistwidget = self.find(self.sender().text())
        movelist = self.getListitems()
        for moveitem in movelist:
            pItem = self.takeItem(self.row(moveitem))
            tolistwidget.addItem(pItem)

    def find(self, pmenuname):
        '''
        找到分组对象
        '''
        for item_dic in self.map_listwidget:
            if item_dic['groupname'] == pmenuname:
                return item_dic['listwidget']
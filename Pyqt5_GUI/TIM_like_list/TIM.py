# -*- coding: utf-8 -*-

"""
这是一个关于TIM模拟（QTreeWidget）的例子！
文章链接：http://www.xdbcb8.com/archives/737.html
文章链接：http://www.xdbcb8.com/archives/740.html
文章链接：http://www.xdbcb8.com/archives/753.html
文章链接：http://www.xdbcb8.com/archives/757.html
文章链接：http://www.xdbcb8.com/archives/762.html
"""

import sys

import codecs
import random
from PyQt5.QtCore import Qt, QSize, pyqtSlot, QVariant
from PyQt5.QtGui import QIcon, QFont, QBrush, QStandardItemModel
from PyQt5.QtWidgets import QWidget, QApplication, QTreeWidgetItem, QMenu, QAction, QInputDialog, QMessageBox, \
    QAbstractItemView, QCompleter

import Pyqt5_GUI.TIM_like_list.Random_Name as Random_Name
from Pyqt5_GUI.TIM_like_list.Dialog_additem import Dialog_additem
from Pyqt5_GUI.TIM_like_list.Ui_ui import Ui_Form


class TIM(QWidget, Ui_Form):
    '''
    TIM模拟
    '''
    grouplist = []
    # 分组信息存储

    userslist = []
    # 用户信息存储

    tmpuseritem = []

    # 临时保存一下批量操作是我们选中的联系人对象

    def __init__(self, parent=None):
        '''
        一些初始设置
        '''
        super(TIM, self).__init__(parent)
        self.setupUi(self)
        self.Ui_init()

    def Ui_init(self):
        '''
        界面初始设置
        '''
        self.treeWidget.setColumnCount(1)
        self.treeWidget.setColumnWidth(0, 50)
        self.treeWidget.setHeaderLabels(["好友"])
        # 每个项目的标题中添加一列，并为每列设置标签

        self.treeWidget.setIconSize(QSize(70, 70))
        # 设置图标大小的

        self.treeWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # 同时设置多选的方式

        self.treeWidget.itemSelectionChanged.connect(self.getListitems)  # 项目选择发生变化时发出信号
        self.treeWidget.currentItemChanged.connect(self.restatistic)  # 当前项目发生变化时发出信号
        self.treeWidget.itemClicked.connect(self.isclick)  # 项目点击时发出信号

        with codecs.open('./res/treewidget.qss', 'r', 'utf-8') as f:
            styleSheet = f.readlines()
        style = '\r\n'.join(styleSheet)
        self.treeWidget.setStyleSheet(style)
        # 样式设置

        root = self.creategroup('我的好友')  # 默认用户组
        root.setExpanded(True)  # 默认是好友展开

        self.menuflag = 1
        # 是否出现批量操作菜单的标志

        self.m_model = QStandardItemModel(0, 1, self)
        m_completer = QCompleter(self.m_model, self)
        self.lineEdit.setCompleter(m_completer)
        m_completer.activated[str].connect(self.onUsernameChoosed)
        # 搜索时自动填充姓名

    def creategroup(self, groupname):
        hidernum = 0
        # 统计隐身联系人

        group = QTreeWidgetItem(self.treeWidget)
        # 新增一个分组（QTreeWidgetItem类型），这个分组是挂在self.treeWidget下的

        groupdic = {'group': group,
                    'groupname': groupname,
                    'childcount': 0,
                    'childishide': 0}
        # 分组信息字典

        icon = self.searchicon(groupname)
        group.setIcon(0, icon)
        # 根据分组名称设置图标的

        randomnum = random.sample(range(26), 10)
        for i in randomnum:
            child = QTreeWidgetItem()
            # 一个联系人
            randname, randicon, font, isvip, ishider = self.createusers(i)  # 随机创建一个用户
            userdic = {'user': child, 'username': randname, 'ishide': 0}
            self.userslist.append(userdic)
            child.setText(0, randname)
            child.setFont(0, font)
            child.setIcon(0, randicon)
            child.setTextAlignment(0, Qt.AlignHCenter | Qt.AlignVCenter)
            if isvip == 1:
                # VIP
                child.setForeground(0, QBrush(Qt.red))
                child.setToolTip(0, '会员红名尊享')
            if ishider == 1:
                # 是否隐身
                hidernum += 1
                userdic['ishide'] = 1
            group.addChild(child)
            # 将每个联系人增加先前创建的group分组当中

        childnum = group.childCount()
        # 统计每个分组下联系人的数量

        lastchildnum = childnum - hidernum
        # 减去隐身的数量就是在线联系人的数量了

        groupdic['childcount'] = childnum
        groupdic['childishide'] = hidernum
        # 更新groupdic中的数据

        groupname += ' ' + str(lastchildnum) + '/' + str(childnum)
        # 将当前groupname设置成类似：我的好友 8/10 的样式

        group.setText(0, groupname)
        # 将给定列中显示的文本设置为给定文本，如：我的好友 8/10

        self.grouplist.append(groupdic)
        # 把分组加入到分组列表中

        return group

    def createusers(self, num):
        '''
        创建一个联系人，属性随机
        '''
        randname = Random_Name.getname()
        randicon = QIcon("./res/user/" + str(num) + ".jpg")
        font = QFont()
        font.setPointSize(16)
        isvip = random.randint(0, 5)
        ishider = random.randint(0, 5)
        if ishider == 1:
            randicon = QIcon("./res/user/" + str(num) + "h.jpg")
        return randname, randicon, font, isvip, ishider

    def contextMenuEvent(self, event):
        '''
        上下文菜单
        '''
        hititem = self.treeWidget.currentItem()
        # 返回树小部件中的当前项目，这里可以是分组也可以是联系人

        if hititem:
            root = hititem.parent()
            # 看看这个项目是否有上一节点

            if root is None:
                pgroupmenu = QMenu(self)
                pAddgroupAct = QAction('添加分组', self.treeWidget)
                pRenameAct = QAction('重命名', self.treeWidget)
                pDeleteAct = QAction('删除该组', self.treeWidget)
                pgroupmenu.addAction(pAddgroupAct)
                pgroupmenu.addAction(pRenameAct)
                pgroupmenu.addAction(pDeleteAct)
                pAddgroupAct.triggered.connect(self.addgroup)
                pRenameAct.triggered.connect(self.renamegroup)

                if self.treeWidget.itemAbove(hititem) is None:
                    pDeleteAct.setEnabled(False)
                else:
                    pDeleteAct.triggered.connect(self.deletegroup)
                # 这里表示最顶端的分组（它的上面是有没分组的），pDeleteAct设置为禁用。否则是可以执行的。

                pgroupmenu.popup(self.mapToGlobal(event.pos()))
                # 弹出菜单
            elif root.childCount() > 0:
                # 下面有联系人的话
                pItemmenu = QMenu(self)
                pDeleteItemAct = QAction('删除联系人', pItemmenu)
                pItemmenu.addAction(pDeleteItemAct)
                pDeleteItemAct.triggered.connect(self.delete)
                if len(self.grouplist) > 1:
                    pSubMenu = QMenu('转移联系人至', pItemmenu)
                    pItemmenu.addMenu(pSubMenu)
                    for item_dic in self.grouplist:
                        if item_dic['group'] is not root:
                            pMoveAct = QAction(item_dic['groupname'], pItemmenu)
                            pSubMenu.addAction(pMoveAct)
                            pMoveAct.triggered.connect(self.moveItem)
                if len(self.getListitems(self.menuflag)) == 1:
                    pRenameItemAct = QAction('设定备注', pItemmenu)
                    pItemmenu.addAction(pRenameItemAct)
                    pRenameItemAct.triggered.connect(self.renameItem)
                    # 我们选定的联系人数量只能为1的时候，才能设定备注
                if self.menuflag > 0 and root.childCount() > 1:
                    pBatchAct = QAction('分组内批量操作', pItemmenu)
                    pItemmenu.addAction(pBatchAct)
                    pBatchAct.triggered.connect(self.Batchoperation)
                    # 如果批量操作标志大于0且该分组下面的联系人多余1人，菜单分组内批量操作出现，这个联系到Batchoperation()函数。
                elif self.menuflag < 0:
                    pCancelBatchAct = QAction('取消批量操作', pItemmenu)
                    pItemmenu.addAction(pCancelBatchAct)
                    pCancelBatchAct.triggered.connect(self.CancelBatchoperation)
                    # 否则批量操作标志小于0，我们就显示取消批量操作按钮，这个联系到CancelBatchoperation()函数。

                pItemmenu.popup(self.mapToGlobal(event.pos()))
                # 弹出菜单

    def addgroup(self):
        '''
        增加一个分组
        '''
        gname, ok = QInputDialog.getText(self, '提示信息', '请输入分组名称')
        if ok:
            if len(gname) == 0:
                QMessageBox.information(self, '提示', '分组名称不能为空哦')
            else:
                self.creategroup(gname)

    def renamegroup(self):
        '''
        重命名分组，之后相关数据更新一下
        '''
        hitgroup = self.treeWidget.currentItem()
        # 我们选中的分组

        gnewname, ok = QInputDialog.getText(self, '提示信息', '请输入分组的新名称')
        if ok:
            if len(gnewname) == 0:
                QMessageBox.information(self, '提示', '分组名称不能为空哦')
            else:
                hitgroup.setText(0, gnewname)
                newicon = self.searchicon(hitgroup.text(0))
                hitgroup.setIcon(0, newicon)
                gindex = self.searchgroup(hitgroup)
                self.grouplist[gindex]['groupname'] = gnewname
                self.treeWidget.setCurrentItem(hitgroup.child(0))
                # 设置当前的项目（这里表示分组中的第一个联系人）

    def deletegroup(self):
        '''
        删除分组
        '''
        hitgroup = self.treeWidget.currentItem()
        gindex = self.searchgroup(hitgroup)
        reply = QMessageBox.question(self, '警告', '确定要删除这个分组及其联系人吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.treeWidget.takeTopLevelItem(gindex)
            # 删除树中给定索引处的顶级项目并返回它，否则返回0

            del self.grouplist[gindex]
            # 也要把在self.grouplist的数据也要删除

    def moveItem(self):
        '''
        移动联系人
        '''
        movelist = self.getListitems(self.menuflag)
        togroupname = self.sender().text()
        mindex = self.searchgroup(togroupname)
        togroup = self.grouplist[mindex]['group']
        # 得到新的分组对象

        self.deleteItems(movelist, flag=0)
        self.add(togroup, movelist)
        self.tmpuseritem.clear()
        # 分组的联系人删除、增加

    def delete(self):
        '''
        删除联系人
        '''
        delitems = self.getListitems(self.menuflag)
        self.deleteItems(delitems)
        self.tmpuseritem.clear()

    def deleteItems(self, items, flag=1):
        '''
        删除联系人的具体操作
        '''
        for delitem in items:
            delitem.setData(0, Qt.CheckStateRole, QVariant())
            # 取消删除item的复选框，这句不写，批量操作时联系人转移过去后还是带复选框的。

            pindex = delitem.parent().indexOfChild(delitem)
            dindex = self.searchuser(delitem)
            ishide = self.userslist[dindex]['ishide']
            # 取得我们联系人在当前分组下的索引。找到这个联系人在userslist列表中的索引以及是否隐身信息

            if flag == 1:
                del self.userslist[dindex]
                # 若不是批量操作状态下，则直接删除这些存储在userslist的对象

            fathergroup = delitem.parent()  # 父节点
            findex = self.searchgroup(fathergroup)
            if ishide == 1:
                self.grouplist[findex]['childishide'] -= 1
                self.grouplist[findex]['childcount'] -= 1
                # 要是这个联系人状态是隐身的，我们把grouplist相应的group字典信息修改：总数 - 1，隐身数量 - 1
            else:
                self.grouplist[findex]['childcount'] -= 1
                # 否则只有：总数 - 1

            delitem.parent().takeChild(pindex)
            # 最后删除分组下的联系人

    def add(self, group, items):
        '''
        分组中增加联系人
        '''
        gindex = self.searchgroup(group)
        for item in items:
            aindex = self.searchuser(item)
            ishide = self.userslist[aindex]['ishide']
            if ishide == 1:
                self.grouplist[gindex]['childishide'] += 1
                self.grouplist[gindex]['childcount'] += 1
            else:
                self.grouplist[gindex]['childcount'] += 1
            group.addChild(item)
            # 更新grouplist中的相应信息和实际情况一致

            self.treeWidget.setCurrentItem(item)
            # 触发itemSelectionChanged信号，让分组上的数量再次更新一下

    def Batchoperation(self):
        '''
        遍历分组下的所有联系人，给它们加上checkState
        '''
        self.menuflag *= -1
        # 是否批量操作的标志

        group = self.getListitems()[0].parent()
        childnum = group.childCount()
        for c in range(childnum):
            child = group.child(c)
            child.setCheckState(0, Qt.Unchecked)

    def CancelBatchoperation(self):
        '''
        遍历函数然后把分组联系人的复选框信息全部清除
        '''
        self.menuflag *= -1
        group = self.getListitems()[0].parent()
        childnum = group.childCount()
        for c in range(childnum):
            child = group.child(c)
            child.setData(0, Qt.CheckStateRole, QVariant())

    def isclick(self, item):
        '''
        看看联系人是否被选中
        '''
        if item.checkState(0) == Qt.Checked:
            if self.tmpuseritem.count(item) == 0:
                self.tmpuseritem.append(item)
        # 若联系人的状态是Qt.Checked（被选中），我们一定要先在tmpuseritem列表查查我们点击的联系人对象是不是已经存在了。
        else:
            if len(self.tmpuseritem) > 0:
                if self.tmpuseritem.count(item) != 0:
                    i = self.tmpuseritem.index(item)
                    del self.tmpuseritem[i]
        # 如果tmpuseritem列表有联系人的话，取消选中的时候，我们要判断一下这个联系人存在的话，获取它的索引，然后将它从列表中删除。

    def renameItem(self):
        '''
        设定联系人备注
        '''
        hituser = self.treeWidget.currentItem()
        uindex = self.searchuser(hituser)  # 得到当前选定联系人的索引
        unewname, ok = QInputDialog.getText(self, '提示信息', '请输入备注名称')
        if ok:
            if len(unewname) == 0:
                QMessageBox.information(self, '提示', '备注名称不能为空哦')
            else:
                hituser.setText(0, unewname)
                self.userslist[uindex]['username'] = unewname

    def searchgroup(self, hitgroup):
        '''
        根据分组名称或对象返回其索引
        '''
        if isinstance(hitgroup, str):  # 是分组名称吗？
            for i, g in enumerate(self.grouplist):
                if g['groupname'] == hitgroup:
                    return i
        else:
            for i, g in enumerate(self.grouplist):  # 分组对象吗？
                if g['group'] == hitgroup:
                    return i

    def searchuser(self, hituser):
        '''
        返回联系人的索引
        '''
        if isinstance(hituser, str):  # 是联系人名称吗？
            for i, u in enumerate(self.userslist):
                if u['username'] == hituser:
                    return i
        else:
            for i, u in enumerate(self.userslist):
                if u['user'] == hituser:
                    return i

    def searchicon(self, gpname2):
        '''
        根据分组名查找图标，默认是buddy_default.ico
        '''
        if gpname2.find('好友') >= 0:
            return QIcon('./res/group/buddy.ico')
        elif gpname2.find('同事') >= 0:
            return QIcon('./res/group/partner.ico')
        elif gpname2.find('黑名单') >= 0:
            return QIcon('./res/group/blacklist.ico')
        return QIcon('./res/group/buddy_default.ico')

    def getListitems(self, flag=1):
        '''
        获得项目的数量
        '''
        if flag > 0:
            return self.treeWidget.selectedItems()
            # 当批量操作标志大于0的时候，即返回所有选定的非隐藏项目的列表
        return self.tmpuseritem
        # 要是批量操作标志小于0的时候，我们返回临时存储批量操作的联系人项目。

    def restatistic(self, item, preitem):
        '''
        针对分组的统计函数
        '''
        if item:
            # 首先判断当前项目究竟是分组还是联系人
            fathergroup = item.parent()
            if fathergroup:
                self.restatistic_op(fathergroup)
            else:
                self.restatistic_op(item)
        elif preitem.parent().childCount() == 1:
            lastgroupname = preitem.parent().text(0).split()[0] + ' 0/0'
            preitem.parent().setText(0, lastgroupname)
            self.menuflag = 1

    def restatistic_op(self, itemorgroup):
        '''
        根据分组对象我们在self.grouplist取到相应的联系人数量、隐身联系人的数量，然后再设置分组名称
        '''
        # 设置总人数和在线人数
        gindex = self.searchgroup(itemorgroup)
        totalcount = self.grouplist[gindex]['childcount']
        hidecount = self.grouplist[gindex]['childishide']
        fathergroupname = self.grouplist[gindex]['groupname']
        fathergroupname += ' ' + str(totalcount - hidecount) + '/' + str(totalcount)
        itemorgroup.setText(0, fathergroupname)

    def onUsernameChoosed(self, name):
        '''
        设置搜索的联系人
        '''
        self.lineEdit.setText(name)

    @pyqtSlot()
    def on_bt_search_clicked(self):
        '''
        查找联系人
        '''
        username = self.lineEdit.text()
        if len(username) > 0:
            useritemindex = self.searchuser(username)
            useritem = self.userslist[useritemindex]['user']
            self.treeWidget.setCurrentItem(useritem)

    @pyqtSlot()
    def on_bt_adduser_clicked(self):
        '''
        增加联系人
        '''
        print('增加联系人')
        adduser = Dialog_additem()  # 自定义增加联系人对话框
        for g in self.grouplist:
            adduser.comboBox.addItem(g['groupname'])
        r = adduser.exec_()
        if r > 0:
            newitem = QTreeWidgetItem()
            newname = adduser.lineEdit.text()
            newicon = adduser.geticonpath()
            font = QFont()
            font.setPointSize(16)
            newitem.setFont(0, font)
            newitem.setText(0, newname)
            newitem.setTextAlignment(0, Qt.AlignHCenter | Qt.AlignVCenter)
            newitem.setIcon(0, QIcon(newicon))
            comboxinfo = adduser.comboBox.currentText()
            # 新增的联系人在哪个分组呢，看这里

            cindex = self.searchgroup(comboxinfo)
            group = self.grouplist[cindex]['group']
            self.grouplist[cindex]['childcount'] += 1
            userdic = {'user': newitem, 'username': newname, 'ishide': 0}
            self.userslist.append(userdic)
            group.addChild(newitem)
            self.treeWidget.setCurrentItem(newitem)
            # 增加联系人之后相关数据要更新一下

    @pyqtSlot(str)
    def on_lineEdit_textChanged(self, text):
        '''
        联系人名称自动补全
        '''
        namelist = []

        for itm in self.userslist:
            username = itm['username']
            if username.find(text) >= 0:
                namelist.append(itm['username'])
        self.m_model.removeRows(0, self.m_model.rowCount())

        for i in range(0, len(namelist)):
            self.m_model.insertRow(0)
            self.m_model.setData(self.m_model.index(0, 0), namelist[i])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tim = TIM()
    tim.show()
    sys.exit(app.exec_())

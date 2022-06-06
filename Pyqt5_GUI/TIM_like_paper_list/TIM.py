# -*- coding: utf-8 -*-

"""
这是一个关于TIM模拟（QTreeWidget）的例子！
文章链接：http://www.xdbcb8.com/archives/737.html
文章链接：http://www.xdbcb8.com/archives/740.html
文章链接：http://www.xdbcb8.com/archives/753.html
文章链接：http://www.xdbcb8.com/archives/757.html
文章链接：http://www.xdbcb8.com/archives/762.html
"""
import os
import sys
from Pyqt5_GUI.utils.tools import tools
from Pyqt5_GUI.utils.settings import Settings
import codecs
import random
from PyQt5.QtCore import Qt, QSize, pyqtSlot, QVariant
from PyQt5.QtGui import QIcon, QFont, QBrush, QStandardItemModel, QImage
from PyQt5.QtWidgets import QWidget, QApplication, QTreeWidgetItem, QMenu, QAction, QInputDialog, QMessageBox, \
    QAbstractItemView, QCompleter

import Pyqt5_GUI.TIM_like_list.Random_Name as Random_Name
from Pyqt5_GUI.TIM_like_list.Dialog_additem import Dialog_additem
from Pyqt5_GUI.TIM_like_list.Ui_ui import Ui_Form


class TIM_list(QWidget, Ui_Form):
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
        super(TIM_list, self).__init__(parent)
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

        # self.treeWidget.itemSelectionChanged.connect(self.getListitems)  # 项目选择发生变化时发出信号
        # self.treeWidget.currentItemChanged.connect(self.restatistic)  # 当前项目发生变化时发出信号
        self.treeWidget.itemClicked.connect(self.isclick)  # 项目点击时发出信号
        #
        # with codecs.open('./res/treewidget.qss', 'r', 'utf-8') as f:
        #     styleSheet = f.readlines()
        # style = '\r\n'.join(styleSheet)
        # self.treeWidget.setStyleSheet(style)
        # # 样式设置
        #
        root = self.creategroup('我的好友')  # 默认用户组
        root.setExpanded(True)  # 默认是好友展开
        #
        # self.menuflag = 1
        # # 是否出现批量操作菜单的标志
        #
        # self.m_model = QStandardItemModel(0, 1, self)
        # m_completer = QCompleter(self.m_model, self)
        # self.lineEdit.setCompleter(m_completer)
        # m_completer.activated[str].connect(self.onUsernameChoosed)
        # # 搜索时自动填充姓名

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


class Paper_Sample(tools.abstract_config):
    def __init__(self, **kwargs):
        # ==== 笔记信息
        self.text = '笔记内容'  # 笔记内容
        self.image_ls = []  # 图片路径存储
        self.tags = {}  # 技术点标签，待定,或者主题标签，类似于光流，分割等
        self.reading_date = None  # 最开始阅读的时间
        self.modify_date = None  # 最近修改的时间

        # ===== 论文信息
        self.title = '无标题'
        self.years = ''  # 年份, int
        self.produce = ''  # 论文出处,str
        # self.auther_ls = []  # 作者，可能记录不太方便, 暂时不用
        # self.pdf_url = None,  # pdf 下载链接，str，后面可能使用自动下载
        # self.code_url = None  # 代码链接，有就str，无就none
        self.update(kwargs)


class Paper_Data():
    def __init__(self, settings: Settings):
        self.conf = settings
        self.data_ls = {'0': Paper_Sample()}

    def save(self):
        save_path = os.path.join(self.conf.main_data_dir, 'data.pkl')
        tools.pickle_saver.save_pickle(self, save_path)

    def load(self):
        save_path = os.path.join(self.conf.main_data_dir, 'data.pkl')
        if os.path.isfile(save_path):
            s = tools.pickle_saver.load_picke(save_path)
            self.data_ls = s.data_ls

    def get_all_list(self):
        res = [self.data_ls[i] for i in self.data_ls.keys()]
        return res

    def get_paper_widget_item(self, paper_sample: Paper_Sample):
        if len(paper_sample.image_ls) > 0:
            icon_image_name = paper_sample.image_ls[0]
            icon_image_path = os.path.join(self.conf.image_save_dir, icon_image_name)
        else:
            icon_image_path = os.path.join(self.conf.main_data_dir, 'res', 'defaut_paper_ico.jpg')

        sample_icon = QIcon(icon_image_path)  # size会自动处理

        font = QFont()
        font.setPointSize(self.conf.list_font_size)
        font.setBold(True)

        font2 = QFont()
        font2.setPointSize(self.conf.list_font_size-2)


        child = QTreeWidgetItem()

        child.setText(0, '[%s][%s]'%(paper_sample.years,paper_sample.produce)+paper_sample.title)
        child.setFont(0, font)

        child.setIcon(0, sample_icon)

        child.setTextAlignment(0, Qt.AlignHCenter | Qt.AlignVCenter)
        return child

    @classmethod
    def demo_data(cls):
        pdata = Paper_Data(Settings())
        p1 = Paper_Sample(image_ls=[os.path.join(pdata.conf.main_data_dir, 'temp.png')], tags={'main_tag': ['光流', ]},
                          reading_date=0, modify_date=0, title='论文1Paper_DataPaper_DataPaper_Data', years='2001', produce='CCTV')
        p2 = Paper_Sample(image_ls=[os.path.join(pdata.conf.main_data_dir, 'temp1.png')], tags={'main_tag': ['光流', ]},
                          reading_date=1, modify_date=1, title='论文2', years='2002', produce='CCTV')
        p3 = Paper_Sample(image_ls=[os.path.join(pdata.conf.main_data_dir, 'temp2.png')], tags={'main_tag': ['光流', ]},
                          reading_date=1, modify_date=1, title='论文3', years='2003', produce='CCTV')
        p4 = Paper_Sample(reading_date=1, modify_date=1, title='论文4', years='2004', produce='CCTV')
        pdata.data_ls = {'0': p1, '1': p2, '2': p3, '3': p4}
        return pdata


class TIM_Paper_list(QWidget, Ui_Form):
    '''
    TIM模拟
    '''
    grouplist = []
    # 分组信息存储

    userslist = []
    # 用户信息存储

    tmpuseritem = []  # 临时保存一下批量操作是我们选中的联系人对象

    def __init__(self, parent=None, conf=None, paper_data=None):
        '''
        一些初始设置
        '''
        super(TIM_Paper_list, self).__init__(parent)
        assert isinstance(conf, Settings)
        assert isinstance(paper_data, Paper_Data)
        self.conf = conf
        self.paper_data = paper_data
        self.setupUi(self)  # 初始化UI界面
        self.Ui_init()  # 初始化各种功能，列表等

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
        root = self.update_paper_group()  # 默认分组为所有笔记
        root.setExpanded(True)  # 默认是好友展开

        # self.treeWidget.itemSelectionChanged.connect(self.getListitems)  # 项目选择发生变化时发出信号
        # self.treeWidget.currentItemChanged.connect(self.restatistic)  # 当前项目发生变化时发出信号
        # self.treeWidget.itemClicked.connect(self.isclick)  # 项目点击时发出信号

        # item的样式设置
        with codecs.open('./res/treewidget.qss', 'r', 'utf-8') as f:
            styleSheet = f.readlines()
        style = '\r\n'.join(styleSheet)
        self.treeWidget.setStyleSheet(style)

        #
        # self.menuflag = 1
        # # 是否出现批量操作菜单的标志
        #
        # self.m_model = QStandardItemModel(0, 1, self)
        # m_completer = QCompleter(self.m_model, self)
        # self.lineEdit.setCompleter(m_completer)
        # m_completer.activated[str].connect(self.onUsernameChoosed)
        # # 搜索时自动填充姓名

    def update_paper_group(self):
        all_paper_ls = self.paper_data.get_all_list()

        # 建立所有笔记的分组
        group_name = '所有笔记'

        group_all_note = QTreeWidgetItem(self.treeWidget)  # 所有笔记的分组（QTreeWidgetItem类型），这个分组是挂在self.treeWidget下的
        groupdic = {'group': group_all_note,  # 分组信息字典,记录起来
                    'groupname': group_name,
                    'childcount': 0, }

        # 根据分组名称设置图标的
        icon = self.searchicon(group_name)
        group_all_note.setIcon(0, icon)

        # 对每个paper的笔记都加入这个组
        for paper_i in all_paper_ls:
            child = self.paper_data.get_paper_widget_item(paper_i)
            group_all_note.addChild(child)  # 加入分组

        childnum = group_all_note.childCount()  # 统计每个分组下的数量

        groupdic['childcount'] = childnum
        # 更新groupdic中的数据

        group_name += ' [%s]' % childnum
        # 将当前groupname设置成类似：我的好友 8/10 的样式

        group_all_note.setText(0, group_name)
        # 将给定列中显示的文本设置为给定文本，如：我的好友 8/10

        self.grouplist.append(groupdic)
        # 把分组加入到分组列表中
        return group_all_note

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

    def searchicon(self, gpname2):
        '''
        根据分组名查找图标，默认是buddy_default.ico
        '''
        if gpname2.find('所有笔记') >= 0:
            return QIcon('./res/group/buddy.ico')
        elif gpname2.find('同事') >= 0:
            return QIcon('./res/group/partner.ico')
        elif gpname2.find('黑名单') >= 0:
            return QIcon('./res/group/blacklist.ico')
        return QIcon('./res/group/buddy_default.ico')

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tim = TIM_Paper_list(conf=Settings(), paper_data=Paper_Data.demo_data())
    tim.show()
    sys.exit(app.exec_())

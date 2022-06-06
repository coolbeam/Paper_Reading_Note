import sys
import os

'''
https://github.com/5yutan5/PyQtDarkTheme
'''
from utils.tools import tools
from utils.settings import Settings, Paper_Sample, Paper_Data
# from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
# from PyQt5.QtCore import Qt
import qdarktheme
from qdarktheme.qtpy.QtCore import QDir, Qt, Slot, QSize, pyqtSlot
from qdarktheme.util import get_qdarktheme_root_path
from qdarktheme.qtpy.QtGui import QAction, QActionGroup, QFont, QIcon, QTextOption, QBrush
from qdarktheme.qtpy.QtWidgets import (QTreeView,
                                       QApplication, QColorDialog, QFileDialog, QVBoxLayout, QHBoxLayout, QLabel, QMainWindow, QMenuBar,
                                       QMessageBox, QSizePolicy, QStackedWidget, QStatusBar, QToolBar, QToolButton, QSplitter, QLineEdit,
                                       QWidget, QTextEdit, QTreeWidget, QTreeWidgetItem, QAbstractItemView, QHeaderView, QFrame, QPlainTextEdit, QComboBox
                                       )
from qdarktheme.widget_gallery.ui.dock_ui import DockUI
from qdarktheme.widget_gallery.ui.frame_ui import FrameUI
from qdarktheme.widget_gallery.ui.widgets_ui import WidgetsUI
import qtawesome as qta

icon_ls = ['folder_open_24dp', 'palette_24dp', 'font_download_24dp',
           'circle_24dp', 'clear_24dp', 'widgets_24dp', 'flip_to_front_24dp', 'crop_din_24dp', 'settings_24dp',
           'announcement_24dp', 'contrast_24dp']
''' 添加'''


class Note_list(QWidget):
    def __init__(self, conf=None, paper_data=None):
        super(Note_list, self).__init__()
        assert isinstance(conf, Settings)
        assert isinstance(paper_data, Paper_Data)
        self.conf = conf
        self.paper_data = paper_data
        self.tree_view_grouplist = {}  # 用来记录group
        self.tree_view_child_ls = {}  # 用来记录所有的paper笔记，key是他们在paper data里面的key
        self.current_child_key = ''  # 用于取出最后修改过的那个note作为初始化载入

        # ==== setup UI items
        self.paper_tree_view = QTreeWidget()
        self.search_text = QLineEdit()
        self.search_button = QToolButton()  # 搜索按钮点击搜索
        self.search_option = QComboBox()  # 搜索类别选择
        self.search_tag_edit_btn = QToolButton()  # 搜索标签的时候搜索哪些标签舍子
        self.bt_addnote = QToolButton()
        self.item_brush_dark = QBrush(Qt.white)
        self.item_brush_light = QBrush(Qt.black)
        self.item_brush_favorate = QBrush(Qt.red)
        # 阅读进度图标
        self.progress_1_icon_dict = {}

        # ==== setup UI actions
        self.setup_ui_actions()

        # ==== setup UI layout
        self.setup_ui_layout()

    def setup_ui_actions(self):
        self.paper_tree_view.setColumnCount(4)  # 一共三列
        self.paper_tree_view.setHeaderLabels(["年份", '出处', '标题', '修改时间'])
        self.paper_tree_view.setSortingEnabled(True)  # 可排序
        self.paper_tree_view.sortByColumn(3, Qt.SortOrder.DescendingOrder)  # 安装第三列排序,即修改时间
        # self.paper_tree_view.hideColumn(3)
        self.paper_tree_view.setAllColumnsShowFocus(True)  # 点击的时候标记出来current item
        self.paper_tree_view.setAutoScroll(False)  # 重要,打开这个的话点击就自动给你滚动了很讨厌

        self.paper_tree_view.setIndentation(5)  # https://zhuanlan.zhihu.com/p/58392806 树视图中项目的缩进
        # self.tree_view.setIconSize(QSize(70, 70))
        # self.tree_view.setTreePosition(0)
        self.paper_tree_view.setAnimated(True)  # 展开收缩的动画
        self.paper_tree_view.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)  # 设置宽度自适应
        self.paper_tree_view.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)  # 设置宽度自适应
        self.paper_tree_view.header().setSectionResizeMode(2, QHeaderView.ResizeToContents)  # 设置宽度自适应
        # self.paper_tree_view.header().setSectionResizeMode(3, QHeaderView.ResizeToContents)  # 设置宽度自适应
        self.paper_tree_view.header().setDragEnabled(True)  # 设置标题栏可以拖动
        self.paper_tree_view.currentItemChanged.connect(self.on_currentItemChanged)  # 当前项目发生变化时发出信号
        # self.paper_tree_view.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 同时设置多选的方式, 不设置多选和批量操作

        self.search_text.setPlaceholderText("搜索")
        self.search_button.setIcon(QIcon(os.path.join(self.conf.res_save_dir, 'search.ico')))
        self.search_option.addItems(("标题", "年份", "出处", "笔记", "标签"))
        self.search_tag_edit_btn.setIcon(qta.icon('ei.list', color='white', ))
        self.bt_addnote.setIcon(QIcon(os.path.join(self.conf.res_save_dir, 'add.ico')))
        self.bt_addnote.setAutoRaise(True)

        # 设置tips
        self.bt_addnote.setToolTip("添加笔记")
        self.search_text.setToolTip("搜索笔记")
        self.search_button.setToolTip("点击进行搜索")
        self.search_option.setToolTip("搜索选项")

        # 设置按钮事件
        self.paper_tree_view.itemClicked.connect(self.item_click)  # 项目点击时发出信号
        self.bt_addnote.clicked.connect(self.on_bt_addnote_clicked)
        self.search_button.clicked.connect(self.on_search_button_clicked)

    @classmethod
    def _make_h_layout(cls, widget_ls, space=0, margins=(0, 0, 0, 0)):
        temp_hbox = QHBoxLayout()
        temp_container = QWidget()
        temp_hbox.setSpacing(space)
        temp_hbox.setContentsMargins(margins[0], margins[1], margins[2], margins[3])
        for i_widget in widget_ls:
            temp_hbox.addWidget(i_widget)
        temp_container.setLayout(temp_hbox)
        return temp_container

    @classmethod
    def _make_v_layout(cls, widget_ls, space=0, margins=(0, 0, 0, 0)):
        temp_hbox = QVBoxLayout()
        temp_container = QWidget()
        temp_hbox.setSpacing(space)
        temp_hbox.setContentsMargins(margins[0], margins[1], margins[2], margins[3])
        for i_widget in widget_ls:
            temp_hbox.addWidget(i_widget)
        temp_container.setLayout(temp_hbox)
        return temp_container

    def setup_ui_layout(self):
        # 载入icon资源
        for i in [1, 20, 50, 80, 99]:
            self.progress_1_icon_dict['%s%%' % i] = QIcon(os.path.join(self.conf.res_save_dir, 'progress_ico_%s.svg' % i))

        # 初始化, 先把所有paper笔记弄成item，存起来
        self.paper_tree_view.setIconSize(QSize(20, 20))
        for p_key in self.paper_data.keys():
            paper_sample = self.paper_data.fetch(p_key)
            child = self.get_paper_widget_item(paper_sample)
            child.paper_sample = paper_sample  # todo 这里把该sample记录了
            child.paper_data_key = p_key  # todo key也记录了
            if '收藏' in child.paper_sample.tags:
                child.setToolTip(2, '收藏:' + child.paper_sample.title)
            else:
                child.setToolTip(2, child.paper_sample.title)
            self.tree_view_child_ls[p_key] = child
        child_ls = [self.tree_view_child_ls[i] for i in self.tree_view_child_ls.keys()]
        child_ls = sorted(child_ls, key=lambda x: x.paper_sample.modify_date, reverse=True)  # 按照最后修改顺序排序
        self.current_child_key = child_ls[0].paper_data_key

        # 初始group：所有笔记
        root = self.tree_view_create_paper_group(child_ls, group_name='所有笔记')  # 默认分组为所有笔记，这里需要加一个按最近阅读排序
        root.setExpanded(True)  # 所有笔记的分组默认是展开

        globale_vbox = QVBoxLayout(self)
        search_container = self._make_h_layout([self.bt_addnote, self.search_text, self.search_button, self.search_option, self.search_tag_edit_btn], space=5)
        globale_vbox.addWidget(search_container)
        globale_vbox.addWidget(self.paper_tree_view)

    # 这里初始化的时候没有载入确切的note给到editor那边
    def init_set_item(self):
        self.paper_tree_view.setCurrentItem(self.tree_view_child_ls[self.current_child_key])

    def tree_view_create_paper_group(self, paper_item_ls, group_name):
        group_item = QTreeWidgetItem(self.paper_tree_view)  # （QTreeWidgetItem类型），这个分组是挂在self.treeWidget下的
        # 对每个paper的笔记都加入这个组
        for paper_item in paper_item_ls:
            group_item.addChild(paper_item)  # 加入分组
        childnum = group_item.childCount()  # 统计分组下的数量
        group_item.setText(0, group_name + ' [%s]' % childnum)
        # 将给定列中显示的文本设置为给定文本，如：所有笔记 [10]
        self.tree_view_grouplist[group_name] = group_item  # 把分组加入到分组dict中记录下来
        return group_item

    # 给一个paper_sample,输出一个treeview的子节点
    def get_paper_widget_item(self, paper_sample: Paper_Sample):
        sample_icon = self.progress_1_icon_dict[paper_sample.readind_progress]  # size会自动处理

        font = QFont()
        font.setPointSize(self.conf.list_font_size)
        font.setBold(True)

        child = QTreeWidgetItem()
        # 0=年份, 1=出处, 2=标题, 3=修改时间

        child.setText(0, '%s' % paper_sample.years)
        child.setText(1, '%s' % paper_sample.produce)
        child.setText(2, '%s' % paper_sample.title)
        child.setText(3, '%s' % paper_sample.modify_date)

        child.setFont(0, font)
        child.setFont(1, font)
        child.setFont(2, font)
        child.setFont(3, font)

        child.setIcon(0, sample_icon)

        child.setTextAlignment(0, Qt.AlignHCenter | Qt.AlignVCenter)
        if '收藏' in paper_sample.tags:
            child.setForeground(0, self.item_brush_favorate)
            child.setForeground(1, self.item_brush_favorate)
            child.setForeground(2, self.item_brush_favorate)
            child.setForeground(3, self.item_brush_favorate)
        return child

    def update_item_icon(self, item):
        sample_icon = self.progress_1_icon_dict[item.paper_sample.readind_progress]  # size会自动处理
        item.setIcon(0, sample_icon)

    def item_update_favorate(self):
        item = self.paper_tree_view.currentItem()
        if item:
            # 首先判断当前项目究竟是分组还是联系人
            if hasattr(item, 'paper_sample'):  # 这样才能确认是note item，不然有可能是选中的group
                if isinstance(item.paper_sample, Paper_Sample):
                    if '收藏' in item.paper_sample.tags:
                        item.setForeground(0, self.item_brush_favorate)
                        item.setForeground(1, self.item_brush_favorate)
                        item.setForeground(2, self.item_brush_favorate)
                        item.setForeground(3, self.item_brush_favorate)
                        item.setToolTip(2, '收藏:' + item.paper_sample.title)
                    elif self.conf.theme == 'dark':
                        item.setForeground(0, self.item_brush_dark)
                        item.setForeground(1, self.item_brush_dark)
                        item.setForeground(2, self.item_brush_dark)
                        item.setForeground(3, self.item_brush_dark)
                        item.setToolTip(2, item.paper_sample.title)
                    elif self.conf.theme == 'light':
                        item.setForeground(0, self.item_brush_light)
                        item.setForeground(1, self.item_brush_light)
                        item.setForeground(2, self.item_brush_light)
                        item.setForeground(3, self.item_brush_light)
                        item.setToolTip(2, item.paper_sample.title)

    '''         事件相应函数            '''

    # 如果editor那边的信息变了item的相应信息也要变
    def on_year_text_change(self):
        item = self.paper_tree_view.currentItem()
        if item:
            # 首先判断当前项目究竟是分组还是联系人
            if hasattr(item, 'paper_sample'):  # 这样才能确认是note item，不然有可能是选中的group
                if isinstance(item.paper_sample, Paper_Sample):
                    item.setText(0, '%s' % item.paper_sample.years)
                    item.setText(3, '%s' % item.paper_sample.modify_date)

    # 如果editor那边的信息变了item的相应信息也要变
    def on_reading_progress_change(self):
        item = self.paper_tree_view.currentItem()
        if item:
            # 首先判断当前项目究竟是分组还是联系人
            if hasattr(item, 'paper_sample'):  # 这样才能确认是note item，不然有可能是选中的group
                if isinstance(item.paper_sample, Paper_Sample):
                    self.update_item_icon(item)

    # 论文出处修改了
    def on_produce_change(self):
        item = self.paper_tree_view.currentItem()
        if item:
            # 首先判断当前项目究竟是分组还是联系人
            if hasattr(item, 'paper_sample'):  # 这样才能确认是note item，不然有可能是选中的group
                if isinstance(item.paper_sample, Paper_Sample):
                    item.setText(1, '%s' % item.paper_sample.produce)
                    item.setText(3, '%s' % item.paper_sample.modify_date)

    # 论文标题修改了
    def on_title_change(self):
        item = self.paper_tree_view.currentItem()
        if item:
            # 首先判断当前项目究竟是分组还是联系人
            if hasattr(item, 'paper_sample'):  # 这样才能确认是note item，不然有可能是选中的group
                if isinstance(item.paper_sample, Paper_Sample):
                    item.setText(2, '%s' % item.paper_sample.title)
                    item.setText(3, '%s' % item.paper_sample.modify_date)
                    if '收藏' in item.paper_sample.tags:
                        item.setToolTip(2, '收藏:' + item.paper_sample.title)
                    else:
                        item.setToolTip(2, item.paper_sample.title)

    # 选中的item变了，需要重新统计group
    def on_currentItemChanged(self, item, preitem):
        '''
        针对分组的统计函数
        '''
        # print('*' * 10)
        if item:
            if hasattr(item, 'paper_sample'):  # 这样才能确认是note item，不然有可能是选中的group
                if isinstance(item.paper_sample, Paper_Sample):
                    pass
                    # print('当前选中的item是：')
                    # print(item.paper_sample.to_dict)
                    # print('')

        for grou_k in self.tree_view_grouplist.keys():
            groups = self.tree_view_grouplist[grou_k]
            childnum = groups.childCount()
            groups.setText(0, grou_k + ' [%s]' % childnum)
        # if item:
        #     # 首先判断当前项目究竟是分组还是联系人
        #     if hasattr(item, 'paper_sample'):  # 这样才能确认是note item，不然有可能是选中的group
        #         print(item.paper_sample.title, item.paper_sample.to_dict)  # 这种情况其实可以指导其父节点是谁
        #         if isinstance(item.paper_sample, Paper_Sample) and isinstance(self.note_editor, Paper_Note_Editor_preview):
        #             self.note_editor.load_paper_sample(item.paper_sample)
        #     # fathergroup = item.parent()
        #     # if fathergroup:  # 是group
        #     #     print('选中group:', fathergroup.text(0))
        #     # else:  # 是子节点
        #     #     pass
        if preitem:
            if hasattr(preitem, 'paper_sample'):  # 这样才能确认是note item，不然有可能是选中的group
                if isinstance(preitem.paper_sample, Paper_Sample):
                    # print('前一个item是：')
                    # print(preitem.paper_sample.to_dict)
                    self.paper_data.check_paper_sample_image(preitem.paper_sample)
                    # self.update_item_icon(preitem)
        # print('*' * 10)

    # 点击到了paper_note item
    def item_click(self, item):
        '''
        看看item是否被选中?
        '''
        if item:
            # 首先判断当前项目究竟是分组还是item
            fathergroup = item.parent()
            if fathergroup:
                print('点击item, index=%s, title=%s' % (item.paper_data_key, item.paper_sample.title))
            else:
                if hasattr(item, 'paper_sample'):  # 这样才能确认是note item，不然有可能是选中的group
                    pass

        # if item.checkState(0) == Qt.Checked:
        #     if self.tmpuseritem.count(item) == 0:
        #         self.tmpuseritem.append(item)
        # # 若联系人的状态是Qt.Checked（被选中），我们一定要先在tmpuseritem列表查查我们点击的联系人对象是不是已经存在了。
        # else:
        #     if len(self.tmpuseritem) > 0:
        #         if self.tmpuseritem.count(item) != 0:
        #             i = self.tmpuseritem.index(item)
        #             del self.tmpuseritem[i]
        # # 如果tmpuseritem列表有联系人的话，取消选中的时候，我们要判断一下这个联系人存在的话，获取它的索引，然后将它从列表中删除。

    # 按下搜索按钮, 准备出一个搜索分组，但是也要删掉这个搜索分组
    def on_search_button_clicked(self):
        '''
        查找笔记
        '''
        print('查找笔记')
        pass
        # username = self.lineEdit.text()
        # if len(username) > 0:
        #     useritemindex = self.searchuser(username)
        #     useritem = self.userslist[useritemindex]['user']
        #     self.treeWidget.setCurrentItem(useritem)

    # 按下添加按钮
    def on_bt_addnote_clicked(self):
        print('添加笔记')
        new_paper_note, new_p_key = self.paper_data.new_paper_note()
        # 如果给的这个key是已经有的
        if new_p_key in self.tree_view_child_ls.keys():
            child = self.tree_view_child_ls[new_p_key]
        else:
            child = self.get_paper_widget_item(new_paper_note)
            child.paper_sample = new_paper_note  # todo 这里把该sample记录了
            child.paper_data_key = new_p_key  # todo key也记录了
            child.setToolTip(2, new_paper_note.title)
            self.tree_view_child_ls[new_p_key] = child
            # 添加到所有笔记的分组里面 todo 后面去实现：当前选中节点在哪个group，就添加到哪个group
            group = self.tree_view_grouplist['所有笔记']
            group.addChild(child)
        self.paper_tree_view.setCurrentItem(child)

    @classmethod
    def demo(cls):
        class Example(QWidget):

            def __init__(self):
                super().__init__()

                self.initUI()

            def initUI(self):
                settings = Settings()
                paper_data = Paper_Data.demo_data()

                lneditor = Note_list(settings, paper_data)

                hbox = QHBoxLayout()
                hbox.addStretch(1)
                hbox.addWidget(lneditor)

                self.setLayout(hbox)

                self.setGeometry(300, 300, 600, 600)
                self.setWindowTitle('Paper_ls')
                self.show()

        app = QApplication(sys.argv)
        conf = Settings()
        # app.setStyleSheet(qdarktheme.load_stylesheet(theme='dark'))
        app.setStyleSheet(qdarktheme.load_stylesheet(theme=conf.theme))
        # # set flat theme, 失败了，估计得重新做
        # dark_palette = qdarktheme.load_palette()
        # palette = app.palette()
        # palette.setColor(QPalette.ColorRole.Link, dark_palette.link().color())
        # app.setPalette(palette)

        # show
        ex = Example()

        sys.exit(app.exec_())


if __name__ == '__main__':
    import sys

    Note_list.demo()

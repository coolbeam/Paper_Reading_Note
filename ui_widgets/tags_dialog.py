from utils.tools import tools
from utils.settings import Settings, Paper_Sample, Paper_Data
import qdarktheme
from qdarktheme.qtpy.QtCore import QDir, Qt, Slot, QSize
from qdarktheme.util import get_qdarktheme_root_path
from qdarktheme.qtpy.QtGui import QAction, QActionGroup, QFont, QIcon, QTextOption
from qdarktheme.qtpy.QtWidgets import (QPushButton, QFrame, QGroupBox,
                                       QApplication, QColorDialog, QFileDialog, QVBoxLayout, QHBoxLayout, QLabel, QMainWindow, QMenuBar, QMessageBox, QSizePolicy, QStackedWidget, QDialogButtonBox,
                                       QDialog, QLineEdit, QGridLayout,QScrollArea,QScroller,
                                       QStatusBar, QToolBar, QToolButton, QSplitter, QWidget, QTextEdit, QTreeWidget, QTreeWidgetItem, QAbstractItemView, QHeaderView, QStyleOptionGroupBox)
import sys, os
from ui_widgets.flow_layout import FlowLayout
import qtawesome as qta


# 有个line edit可以创建新的tag，这个不行，这个里面的按钮不好看，也不好用
class Edit_Tags_Dialog(QDialog):
    class Btn():
        def __init__(self, update_func, btn: QPushButton, name: str, exist_tag_dict: dict):
            self.update_func = update_func
            self.btn = btn
            self.name = name
            self.exist_tag_dict = exist_tag_dict
            # setup
            self.btn.setText(self.name)
            self.btn.setCheckable(True)
            # self.btn.setFlat(True)#不知道有啥用
            self.btn.checkStateSet()
            self.btn.setChecked(False)
            self.btn.clicked.connect(self.on_click)
            self.btn.setAutoFillBackground(True)

        def on_click(self):
            if self.btn.isChecked():
                self.exist_tag_dict[self.name] = True

            else:
                self.exist_tag_dict[self.name] = False
            self.update_func()

    def __init__(self):
        super(Edit_Tags_Dialog, self).__init__()
        self.exist_tag_ls = ['光流', '分割', '检测', 'HDR']  # demo for debug
        self.exist_tag_dict = {}
        self.tag_btn_ls = {}
        for i in self.exist_tag_ls:
            self.exist_tag_dict[i] = False  # 默认为不选中

        # # ===== setup IU items exist_tag_dict必须要先建立好，我觉得，但好像不用先建立好也可以？
        for i in self.exist_tag_ls:
            self.tag_btn_ls[i] = Edit_Tags_Dialog.Btn(update_func=self.tags_update, btn=QPushButton(), name=i, exist_tag_dict=self.exist_tag_dict)

        self.decision_btn = QDialogButtonBox(self)
        self.decision_btn.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.decision_btn.accepted.connect(self.on_decision_btn_accepted)
        self.decision_btn.rejected.connect(self.on_buttonBox_rejected)

        # ==== setup UI layout
        self.setup_ui_layout()

    def tags_update(self):
        chosen_tag_ls = []
        for i in self.exist_tag_dict.keys():
            if self.exist_tag_dict[i]:
                chosen_tag_ls.append(i)
        # print(chosen_tag_ls)

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

    @classmethod
    def _make_flow_layout(cls, widget_ls, space=0, margins=(0, 0, 0, 0)):
        temp_hbox = FlowLayout()
        temp_container = QWidget()
        temp_hbox.setSpacing(space)
        temp_hbox.setContentsMargins(margins[0], margins[1], margins[2], margins[3])
        for i_widget in widget_ls:
            temp_hbox.addWidget(i_widget)
        temp_container.setLayout(temp_hbox)
        return temp_container

    def setup_ui_layout(self):
        btn_ls = [self.tag_btn_ls[i].btn for i in self.tag_btn_ls.keys()]
        # btn_ls_container=self._make_flow_layout(btn_ls,space=5)
        btn_ls_container = self._make_h_layout(btn_ls, space=5)

        global_v_layout = QVBoxLayout(self)
        global_v_layout.addWidget(btn_ls_container)
        global_v_layout.addWidget(self.decision_btn)
        self.resize(300, 300)

    def on_decision_btn_accepted(self):
        """
        点击了ok
        """
        # if len(self.lineEdit.text()) == 0:
        #     QMessageBox.information(self, '提示', '好友姓名为空')
        #     self.lineEdit.setFocus()
        # else:
        #     self.done(1)# 给主窗口的返回值
        print('点击确认了')
        self.tags_update()
        self.done(1)  # 给主窗口的返回值

    def on_buttonBox_rejected(self):
        """
        点击了取消
        """
        print('点击取消了')
        self.done(-1)

    @classmethod
    def demo(cls):
        class Example(QWidget):

            def __init__(self):
                super().__init__()
                self.btn = QPushButton()
                self.btn.setText('呼唤dialog按钮')
                self.btn.clicked.connect(self.button_click)
                #
                self.demo_btn = QPushButton('demo btn')
                self.demo_btn.setCheckable(True)
                self.demo_btn.setChecked(False)

                self.demo_btn2 = QPushButton('demo btn2')
                self.demo_btn2.setCheckable(True)
                self.demo_btn2.setChecked(False)
                self.initUI()

            def initUI(self):
                hbox = QHBoxLayout()
                hbox.addStretch(1)
                hbox.setSpacing(5)
                hbox.addWidget(self.btn)
                hbox.addWidget(self.demo_btn)
                hbox.addWidget(self.demo_btn2)

                self.setLayout(hbox)

                self.setGeometry(300, 300, 600, 600)
                self.setWindowTitle('editor')
                self.show()

            def button_click(self):
                print('按下呼唤按钮了')
                adduser = Edit_Tags_Dialog()  # 自定义增加联系人对话框
                # for g in self.grouplist:
                #     adduser.comboBox.addItem(g['groupname'])
                r = adduser.exec_()
                if r > 0:
                    print('')

        app = QApplication(sys.argv)
        ex = Example()
        app.setStyleSheet(qdarktheme.load_stylesheet('dark'))
        sys.exit(app.exec_())


class Tag_Btn(QPushButton):
    def __init__(self, update_func, name: str, tag_dict: dict, font=None):
        super(Tag_Btn, self).__init__()
        self.update_func = update_func
        self.tag_dict = tag_dict
        self.name = name

        # setup
        self.setText(self.name)
        # self.setCheckable(True)
        # self.setChecked(self.tag_dict[self.name])
        self.clicked.connect(self.on_click)

        if font:
            self.setFont(font)

    def on_click(self):
        if self.tag_dict[self.name]:  # 如果已经被选中了,那么就取消选中
            self.tag_dict[self.name] = False
        else:
            self.tag_dict[self.name] = True
        self.update_func(self)


# 边框上还得加上标题,这个后面再说,给两个东西，note_tag, all_tag 都是list, 输出两个东西新的note_tag和all_tag
class Choose_Tag(QWidget):

    def __init__(self, tag_dict: dict, conf: Settings):
        super(Choose_Tag, self).__init__()
        '''
        Choose_Tag: global layout: V layout
            group_show:有标题:已选tags,有框
                    layout_show: 可以加button
                        button: 各种tag
            grou_choose: 有标题: 候选tags
                    layout_choose:可以加button
                        button:各种tag
            label+lineEdit+button 新增tag(如果新增的tag已有,那就加入已选,如果已经是已选了,那就不管)
        '''
        self.conf = conf
        self.tag_show_layout = FlowLayout()  # 用于展示
        self.tag_chose_layout = FlowLayout()  # 用于选择
        self.add_tag_line = QLineEdit()
        self.add_tag_btn = QPushButton()
        self.tag_dict = tag_dict

        # ===== font
        self.btn_font = QFont()
        self.btn_font.setStyleHint(QFont.Monospace)
        self.btn_font.setFixedPitch(True)
        self.btn_font.setFamily(self.conf.editor_font_family)
        self.btn_font.setPointSize(self.conf.editor_font_size)

        #
        self.btn_ls = {}

        self.setup_ui_layout()

    def create_btn(self, name, if_show=True):
        if name not in self.tag_dict.keys():
            self.tag_dict[name] = if_show  # 新增加的tag默认选中
        btn = Tag_Btn(update_func=self.update_btn, name=name, tag_dict=self.tag_dict, font=self.btn_font)
        self.btn_ls[name] = btn
        self.update_btn(btn)

    def update_btn(self, btn: Tag_Btn):
        if self.tag_dict[btn.name]:  # 如果是选中了
            self.tag_chose_layout.removeWidget(btn)
            self.tag_show_layout.addWidget(btn)
        else:
            self.tag_show_layout.removeWidget(btn)
            self.tag_chose_layout.addWidget(btn)

        # print(self.tag_dict)

    def add_new_tag(self):
        tag_str = self.add_tag_line.text()
        # print(tag_str)
        if tag_str == '':
            pass
            # print('添加tag失败,无tag输入')
        elif tag_str in self.tag_dict.keys():
            # print('已经存在tag:%s' % tag_str)
            self.tag_dict[tag_str] = True
            self.update_btn(self.btn_ls[tag_str])
        else:
            # print('创建新tag:%s' % tag_str)
            self.create_btn(name=tag_str, if_show=True)
            self.add_tag_line.clear()

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

    def setup_ui_layout(self):
        self.add_tag_line.setPlaceholderText('新增tag')
        self.add_tag_btn.setIcon(QIcon(os.path.join(self.conf.res_save_dir, 'add.ico')))
        self.add_tag_btn.clicked.connect(self.add_new_tag)
        # cho_sho_container=QWidget()
        global_layout = QGridLayout(self)

        # 要有大边框
        group_choose = QGroupBox("候选tags")  # 这样框上面就有标题了

        group_show = QGroupBox("已选tags")
        # group_show.setCheckable(True)

        # frame_box.setFrameShape(QFrame.Shape.Box) # 三种frame的形式
        # frame_panel.setFrameShape(QFrame.Shape.Panel)
        # frame_none.setFrameShape(QFrame.Shape.NoFrame)

        # frame_choose = QFrame()  # 这样就有框了
        # frame_show = QFrame()
        # frame_choose.setFrameShape(QFrame.Shape.Box)  # 注意有多种框的方式
        # frame_show.setFrameShape(QFrame.Shape.Box)

        # v_layout = QVBoxLayout(group_choose)  # 这样就把frame加到了group里面,有框和标题了
        # v_layout.addWidget(frame_choose)
        #
        # v_layout = QVBoxLayout(group_show)  # 这样就把frame加到了group里面,有框和标题了
        # v_layout.addWidget(frame_show)

        self.tag_show_layout.setSpacing(5)  # 设置间隔
        self.tag_chose_layout.setSpacing(5)  # 设置间隔

        group_show.setLayout(self.tag_show_layout)  # 这样就把layout放在了框里面了
        group_choose.setLayout(self.tag_chose_layout)

        # # 试试先
        # self.tag_chose_layout.addWidget(QPushButton('choose'))  # 在框里面加东西了
        # self.tag_show_layout.addWidget(QPushButton('show'))
        # temp = None
        # for i in range(10):
        #     k = QPushButton('show_%s' % i)
        #     if i == 8:
        #         temp = k
        #     self.tag_show_layout.addWidget(k)
        # self.tag_show_layout.removeWidget(temp)
        # self.tag_show_layout.addWidget(temp)
        # 初始化btn
        for i in self.tag_dict.keys():
            self.create_btn(name=i, if_show=self.tag_dict[i])

        global_layout.addWidget(group_show, 0, 0, 4, 1)  # 第0行第0列，跨3行，跨1列
        global_layout.addWidget(group_choose, 4, 0, 4, 1)

        edit_container = self._make_h_layout([self.add_tag_line, self.add_tag_btn], space=5)
        global_layout.addWidget(edit_container, 8, 0, 1, 1)
        # self.setGeometry(300, 300, 600, 600)
        # self.resize(300, 300)

    @classmethod
    def demo(cls):
        class Example(QWidget):

            def __init__(self):
                super().__init__()
                self.tag_dict = {'a': False, 'b': False, 'c': True, 'd': False}
                conf = Settings()
                self.chose_tag = Choose_Tag(self.tag_dict, conf)
                self.initUI()

            def initUI(self):
                hbox = QHBoxLayout()
                hbox.addWidget(self.chose_tag)

                self.setLayout(hbox)
                # self.setGeometry(300, 300, 600, 600)
                self.setWindowTitle('Chose Tag')
                self.show()

        app = QApplication(sys.argv)
        ex = Example()
        app.setStyleSheet(qdarktheme.load_stylesheet('dark'))
        sys.exit(app.exec_())


class Choose_Tags_Dialog(QDialog):
    def __init__(self, tag_dict: dict, conf: Settings):
        super(Choose_Tags_Dialog, self).__init__()
        self.tag_dict = tag_dict
        self.conf = conf

        self.choose_tag = Choose_Tag(self.tag_dict, self.conf)
        self.decision_btn = QDialogButtonBox(self)
        self.decision_btn.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.decision_btn.accepted.connect(self.on_decision_btn_accepted)
        self.decision_btn.rejected.connect(self.on_buttonBox_rejected)

        # ==== setup UI layout
        self.setup_ui_layout()

    def setup_ui_layout(self):
        global_v_layout = QVBoxLayout(self)
        global_v_layout.addWidget(self.choose_tag)
        global_v_layout.addWidget(self.decision_btn)
        # self.resize(300, 300)

    def on_decision_btn_accepted(self):
        """
        点击了ok
        """
        # if len(self.lineEdit.text()) == 0:
        #     QMessageBox.information(self, '提示', '好友姓名为空')
        #     self.lineEdit.setFocus()
        # else:
        #     self.done(1)# 给主窗口的返回值
        print('点击确认了')
        self.done(1)  # 给主窗口的返回值

    def on_buttonBox_rejected(self):
        """
        点击了取消
        """
        print('点击取消了')
        self.done(-1)

    @classmethod
    def demo(cls):
        class Example(QWidget):

            def __init__(self):
                super().__init__()
                self.tag_dict = {'a': False, 'b': False, 'c': True, 'd': False}
                self.conf = Settings()
                self.btn = QPushButton()
                self.btn.setText('呼唤dialog按钮')
                self.btn.clicked.connect(self.button_click)
                #
                self.demo_btn = QPushButton('demo check btn')
                self.demo_btn.setCheckable(True)
                self.demo_btn.setChecked(False)

                self.demo_btn2 = QPushButton('demo check btn2')
                self.demo_btn2.setCheckable(True)
                self.demo_btn2.setChecked(False)
                self.initUI()

            def initUI(self):
                hbox = QHBoxLayout()
                # hbox.addStretch(1)
                hbox.setSpacing(5)
                hbox.addWidget(self.btn)
                hbox.addWidget(self.demo_btn)
                hbox.addWidget(self.demo_btn2)

                self.setLayout(hbox)

                self.setGeometry(300, 300, 600, 600)
                self.setWindowTitle('editor')
                self.show()

            def button_click(self):
                print('按下呼唤按钮了')
                chose_tag = Choose_Tags_Dialog(self.tag_dict, self.conf)  # 自定义增加联系人对话框
                # for g in self.grouplist:
                #     adduser.comboBox.addItem(g['groupname'])
                r = chose_tag.exec_()
                if r > 0:
                    print(chose_tag.tag_dict)

        app = QApplication(sys.argv)
        ex = Example()
        app.setStyleSheet(qdarktheme.load_stylesheet('dark'))
        sys.exit(app.exec_())


# 给两个东西，note_tag, all_tag 都是list, 输出两个东西新的note_tag和all_tag, 添加滚动条，防止东西太多了就
class Choose_Tag_ls(QWidget):
    class Tag_Btn(QPushButton):
        def __init__(self, update_func, name: str, note_tag: list, rest_tag: list, font=None):
            super(Choose_Tag_ls.Tag_Btn, self).__init__()
            self.update_func = update_func
            self.note_tag = note_tag
            self.rest_tag = rest_tag
            self.name = name

            # setup
            self.setText(self.name)
            # self.setCheckable(True)
            # self.setChecked(self.tag_dict[self.name])
            self.clicked.connect(self.on_click)

            if font:
                self.setFont(font)

        def on_click(self):
            if self.name in self.note_tag:  # 如果已经被选中了,就去掉选中，加入rest
                self.note_tag.remove(self.name)
                if self.name not in self.rest_tag:
                    self.rest_tag.append(self.name)
            else:  # 没被选中
                self.note_tag.append(self.name)
                if self.name in self.rest_tag:
                    self.rest_tag.remove(self.name)
            self.update_func(self)

    def __init__(self, note_tag: list, all_tag: list, conf: Settings):
        super(Choose_Tag_ls, self).__init__()
        '''
        Choose_Tag: global layout: V layout
            group_show:有标题:已选tags,有框
                    layout_show: 可以加button
                        button: 各种tag
            grou_choose: 有标题: 候选tags
                    layout_choose:可以加button
                        button:各种tag
            label+lineEdit+button 新增tag(如果新增的tag已有,那就加入已选,如果已经是已选了,那就不管)
        '''
        self.conf = conf
        self.tag_show_layout = FlowLayout()  # 用于展示
        self.tag_chose_layout = FlowLayout()  # 用于选择
        self.add_tag_line = QLineEdit()
        self.add_tag_btn = QPushButton()
        self.note_tag = []  # 已选的tag
        self.all_tag = []
        self.rest_tag = []  # 余下的候选tag
        for i in all_tag:
            if i not in self.all_tag:  # 所有标签，去重
                self.all_tag.append(i)
            if i not in note_tag:  # 除掉note tag中，剩余的tag
                self.rest_tag.append(i)
        for i in note_tag:  # note_tag也去重
            if i not in self.note_tag:  # 所有标签，去重
                self.note_tag.append(i)
            if i not in all_tag:  # 如果是没在all tag里面的，all tag得更新一下
                self.all_tag.append(i)

        # ===== font
        self.btn_font = QFont()
        self.btn_font.setStyleHint(QFont.Monospace)
        self.btn_font.setFixedPitch(True)
        self.btn_font.setFamily(self.conf.editor_font_family)
        self.btn_font.setPointSize(self.conf.editor_font_size)

        #
        self.btn_ls = {}

        self.setup_ui_layout()

    # 初始化的时候创建tag
    def create_btn(self, name, if_show=True):
        if name not in self.all_tag:
            self.all_tag.append(name)
            self.note_tag.append(name)
        btn = Choose_Tag_ls.Tag_Btn(update_func=self.update_btn, name=name, note_tag=self.note_tag, rest_tag=self.rest_tag)
        self.btn_ls[name] = btn
        self.update_btn(btn)

    def update_btn(self, btn: Tag_Btn):
        if btn.name in self.note_tag:  # 如果是选中了
            self.tag_chose_layout.removeWidget(btn)
            self.tag_show_layout.addWidget(btn)
        else:
            self.tag_show_layout.removeWidget(btn)
            self.tag_chose_layout.addWidget(btn)
        # print('选中：',self.note_tag)
        # print('未选中：', self.rest_tag)
        # print('所有：', self.all_tag)
        # print('')

    # 点击按钮新增加tag
    def add_new_tag(self):
        tag_str = self.add_tag_line.text()
        # print(tag_str)
        if tag_str == '':
            pass
            # print('添加tag失败,无tag输入')
        elif tag_str in self.all_tag:
            # print('已经存在tag:%s' % tag_str)
            self.tag_dict[tag_str] = True
            self.update_btn(self.btn_ls[tag_str])
            if tag_str in self.note_tag:  # 不管
                pass
            elif tag_str in self.rest_tag:
                self.rest_tag.remove(tag_str)
                self.note_tag.append(tag_str)
            else:
                raise ValueError('不知道哪里可能出问题了')
        else:
            # print('创建新tag:%s' % tag_str)
            self.create_btn(name=tag_str, if_show=True)
            self.add_tag_line.clear()

    @classmethod
    def _make_h_layout(cls, widget_ls, space=0, margins=(0, 0, 0, 0),stretch=0):
        temp_hbox = QHBoxLayout()
        temp_container = QWidget()
        temp_hbox.setSpacing(space)
        temp_hbox.addStretch(stretch)
        temp_hbox.setContentsMargins(margins[0], margins[1], margins[2], margins[3])
        for i_widget in widget_ls:
            temp_hbox.addWidget(i_widget)
        temp_container.setLayout(temp_hbox)
        return temp_container

    def setup_ui_layout(self):
        def make_edit_layout(tag_line,tag_btn):
            temp_layout = QGridLayout()
            temp_container = QWidget()
            temp_layout.setSpacing(5)
            temp_layout.addWidget(tag_line, 0, 0, 1, 8)  # 第0行第0列，跨3行，跨1列
            temp_layout.addWidget(tag_btn, 0, 8, 1, 1)
            temp_container.setLayout(temp_layout)
            return temp_container
        # 初始化btn
        for i in self.all_tag:
            self.create_btn(name=i, if_show=i in self.note_tag)

        self.add_tag_line.setPlaceholderText('新增tag')
        self.add_tag_btn.setIcon(QIcon(os.path.join(self.conf.res_save_dir, 'add.ico')))
        self.add_tag_btn.clicked.connect(self.add_new_tag)
        # cho_sho_container=QWidget()
        global_layout = QVBoxLayout(self)

        # 要有大边框
        group_choose = QGroupBox("候选tags")  # 这样框上面就有标题了

        group_show = QGroupBox("已选tags")
        # group_show.setCheckable(True)

        # frame_box.setFrameShape(QFrame.Shape.Box) # 三种frame的形式
        # frame_panel.setFrameShape(QFrame.Shape.Panel)
        # frame_none.setFrameShape(QFrame.Shape.NoFrame)

        # frame_choose = QFrame()  # 这样就有框了
        # frame_show = QFrame()
        # frame_choose.setFrameShape(QFrame.Shape.Box)  # 注意有多种框的方式
        # frame_show.setFrameShape(QFrame.Shape.Box)

        # v_layout = QVBoxLayout(group_choose)  # 这样就把frame加到了group里面,有框和标题了
        # v_layout.addWidget(frame_choose)
        #
        # v_layout = QVBoxLayout(group_show)  # 这样就把frame加到了group里面,有框和标题了
        # v_layout.addWidget(frame_show)

        self.tag_show_layout.setSpacing(5)  # 设置间隔
        self.tag_chose_layout.setSpacing(5)  # 设置间隔

        group_show.setLayout(self.tag_show_layout)  # 这样就把layout放在了框里面了
        group_choose.setLayout(self.tag_chose_layout)
        group_show.setMinimumSize(400,200)
        group_choose.setMinimumSize(400, 200)
        # group_show.resize(500,250)
        # group_choose.resize(500, 250)

        show_scrol=QScrollArea()
        choose_scroll=QScrollArea()

        show_scrol.setWidget(group_show)
        choose_scroll.setWidget(group_choose)



        global_layout.addWidget(show_scrol, )  # 第0行第0列，跨3行，跨1列
        global_layout.addWidget(choose_scroll, )

        edit_container = make_edit_layout(self.add_tag_line,self.add_tag_btn)
        global_layout.addWidget(edit_container, )
        # self.setMaximumHeight(400)
        # self.setGeometry(300, 300, 600, 600)
        # self.resize(300, 300)


    @classmethod
    def demo(cls):
        class Example(QWidget):

            def __init__(self):
                super().__init__()
                self.note_tag = ['%s' % i for i in range(2)]
                self.all_tag = ['%s' % i for i in range(5)]
                conf = Settings()
                self.chose_tag = Choose_Tag_ls(note_tag=self.note_tag, all_tag=self.all_tag, conf=conf)
                self.initUI()

            def initUI(self):
                hbox = QHBoxLayout()
                hbox.addWidget(self.chose_tag)

                self.setLayout(hbox)
                # self.setGeometry(300, 300, 600, 600)
                self.setWindowTitle('Chose Tag ls')
                self.show()

        app = QApplication(sys.argv)
        ex = Example()
        app.setStyleSheet(qdarktheme.load_stylesheet('dark'))
        sys.exit(app.exec_())


class Choose_Tag_ls_Dialog(QDialog):
    def __init__(self, note_tag: list, all_tag: list, conf: Settings):
        super(Choose_Tag_ls_Dialog, self).__init__()
        self.note_tag = note_tag
        self.all_tag = all_tag
        self.conf = conf

        self.choose_tag = Choose_Tag_ls(self.note_tag, self.all_tag, self.conf)
        self.decision_btn = QDialogButtonBox(self)
        self.decision_btn.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.decision_btn.accepted.connect(self.on_decision_btn_accepted)
        self.decision_btn.rejected.connect(self.on_buttonBox_rejected)

        # ==== setup UI layout
        self.setup_ui_layout()

    def setup_ui_layout(self):
        global_v_layout = QVBoxLayout(self)
        global_v_layout.addWidget(self.choose_tag)
        global_v_layout.addWidget(self.decision_btn)
        # self.resize(800, 400)
        # self.setGeometry(300, 300, 600, 600)

    def on_decision_btn_accepted(self):
        """
        点击了ok
        """
        # if len(self.lineEdit.text()) == 0:
        #     QMessageBox.information(self, '提示', '好友姓名为空')
        #     self.lineEdit.setFocus()
        # else:
        #     self.done(1)# 给主窗口的返回值
        # print('点击确认了')
        self.note_tag = self.choose_tag.note_tag
        for i in self.note_tag:
            if i not in self.all_tag:
                self.all_tag.append(i)

        self.done(1)  # 给主窗口的返回值

    def on_buttonBox_rejected(self):
        """
        点击了取消
        """
        # print('点击取消了')
        self.done(-1)

    @classmethod
    def demo(cls):
        class Example(QWidget):

            def __init__(self):
                super().__init__()
                self.note_tag = ['Ex%s' % i for i in range(10)]
                self.all_tag = ['Ex%s' % i for i in range(100)]
                self.conf = Settings()
                self.btn = QPushButton()
                self.btn.setText('呼唤dialog按钮')
                self.btn.clicked.connect(self.button_click)
                #
                self.demo_btn = QPushButton('demo check btn')
                self.demo_btn.setCheckable(True)
                self.demo_btn.setChecked(False)

                self.demo_btn2 = QPushButton('demo check btn2')
                self.demo_btn2.setCheckable(True)
                self.demo_btn2.setChecked(False)
                self.initUI()

            def initUI(self):
                hbox = QHBoxLayout()
                # hbox.addStretch(1)
                hbox.setSpacing(5)
                hbox.addWidget(self.btn)
                hbox.addWidget(self.demo_btn)
                hbox.addWidget(self.demo_btn2)

                self.setLayout(hbox)

                self.setGeometry(300, 300, 600, 600)
                # self.resize(1200,600)
                self.setWindowTitle('editor')
                self.show()

            def button_click(self):
                print(self.note_tag)
                print(self.all_tag)
                print('按下呼唤按钮了')
                chose_tag = Choose_Tag_ls_Dialog(self.note_tag, self.all_tag, self.conf)  # 自定义增加联系人对话框
                # for g in self.grouplist:
                #     adduser.comboBox.addItem(g['groupname'])
                r = chose_tag.exec_()
                if r > 0:
                    print(chose_tag.note_tag)
                    print(chose_tag.all_tag)
                    self.note_tag=chose_tag.note_tag
                    self.all_tag=chose_tag.all_tag
                    print('确认了tag')
                    print('')

        app = QApplication(sys.argv)
        ex = Example()
        app.setStyleSheet(qdarktheme.load_stylesheet('dark'))
        sys.exit(app.exec_())


if __name__ == '__main__':
    Choose_Tag_ls_Dialog.demo()

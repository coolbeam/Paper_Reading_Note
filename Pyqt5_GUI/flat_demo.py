import sys
import os

'''
https://github.com/5yutan5/PyQtDarkTheme
'''
from utils.tools import tools
from utils.settings import Settings, Paper_Sample, Paper_Data
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtCore import Qt
import qdarktheme
from qdarktheme.qtpy.QtCore import QDir, Qt, Slot, QSize
from qdarktheme.util import get_qdarktheme_root_path
from qdarktheme.qtpy.QtGui import QAction, QActionGroup, QFont, QIcon, QTextOption
from qdarktheme.qtpy.QtWidgets import (
    QApplication,
    QColorDialog,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenuBar,
    QMessageBox,
    QSizePolicy,
    QStackedWidget,
    QStatusBar,
    QToolBar,
    QToolButton,
    QSplitter,
    QWidget, QTextEdit,
    QTreeWidget, QTreeWidgetItem,
    QAbstractItemView, QHeaderView,
)
from qdarktheme.widget_gallery.ui.dock_ui import DockUI
from qdarktheme.widget_gallery.ui.frame_ui import FrameUI
from qdarktheme.widget_gallery.ui.widgets_ui import WidgetsUI
from pyqt_custom_titlebar_window import CustomTitlebarWindow
import qtawesome as qta

icon_ls = ['folder_open_24dp', 'palette_24dp', 'font_download_24dp',
           'circle_24dp', 'clear_24dp', 'widgets_24dp', 'flip_to_front_24dp', 'crop_din_24dp', 'settings_24dp',
           'announcement_24dp', 'contrast_24dp']
from Pyqt5_GUI.flat_editor import Paper_Note_Editor

class Note_editor_page_ui(QWidget):
    def __init__(self, conf=None, paper_data=None):
        super(Note_editor_page_ui, self).__init__()
        assert isinstance(conf, Settings)
        assert isinstance(paper_data, Paper_Data)
        self.conf = conf
        self.paper_data = paper_data

        # ==== tree view部分
        self.tree_view = QTreeWidget()
        self.tree_view.setColumnCount(3)  # 一共三列
        self.tree_view.setHeaderLabels(["年份", '出处', '标题'])
        self.tree_view.setSortingEnabled(True)  # 可排序
        # self.tree_view.setIconSize(QSize(70, 70))
        # self.tree_view.setTreePosition(0)
        self.tree_view.setAnimated(True)

        self.tree_view.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)  # 设置宽度自适应
        self.tree_view.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)  # 设置宽度自适应
        self.tree_view.header().setSectionResizeMode(2, QHeaderView.ResizeToContents)  # 设置宽度自适应

        self.tree_view.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 同时设置多选的方式
        self.tree_view_grouplist = {}
        # 初始化
        root = self.update_paper_group_tree_view()  # 默认分组为所有笔记，这里需要加一个按最近阅读排序
        root.setExpanded(True)  # 所有笔记的分组默认是展开

        # ==== editor的部分，分俩，一个text editor一个view
        self.text_editor = QTextEdit()
        self.text_viewer = QTextEdit()  # 先用俩text edit代替
        # ==== editor的部分还要加上几个line_editor: 标题，年份，出处，阅读程度，code链接，pdf下载链接，还有添加标签的模块

        # takeChild 是取出来，原来的list里面就无了
        # self.text_editor.append(self.tree_view_grouplist['所有笔记']['group'].takeChild(0).paper_sample.text)  # 显示所有笔记里面的第一个
        self.text_editor.setWordWrapMode(QTextOption.WrapMode.NoWrap)

        # === 中线 Widgets,1用来装treeview和editor，2用来在editor里面分text和view的部分
        h_splitter_1, h_splitter_2 = QSplitter(Qt.Orientation.Horizontal), QSplitter(Qt.Orientation.Horizontal)

        h_splitter_2.addWidget(self.text_editor)
        h_splitter_2.addWidget(self.text_viewer)

        h_splitter_1.addWidget(self.tree_view)
        h_splitter_1.addWidget(h_splitter_2)

        h_layout = QHBoxLayout(self)
        h_layout.addWidget(h_splitter_1)

    def update_paper_group_tree_view(self):
        all_paper_ls = [self.paper_data.fetch(i) for i in self.paper_data.keys()]

        # 建立所有笔记的分组
        group_name = '所有笔记'

        group_all_note = QTreeWidgetItem(self.tree_view)  # 所有笔记的分组（QTreeWidgetItem类型），这个分组是挂在self.treeWidget下的
        groupdic = {'group': group_all_note,  # 分组信息字典,记录起来
                    'groupname': group_name,
                    'childcount': 0, }

        # 根据分组名称设置图标的
        # icon = self.searchicon(group_name)
        # group_all_note.setIcon(0, icon)

        # 对每个paper的笔记都加入这个组
        for paper_i in all_paper_ls:
            child = self.get_paper_widget_item(paper_i)
            group_all_note.addChild(child)  # 加入分组

        childnum = group_all_note.childCount()  # 统计每个分组下的数量

        groupdic['childcount'] = childnum
        # 更新groupdic中的数据

        # group_name += ' [%s]' % childnum
        # 将当前groupname设置成类似：我的好友 8/10 的样式

        group_all_note.setText(0, group_name + ' [%s]' % childnum)
        # 将给定列中显示的文本设置为给定文本，如：我的好友 8/10

        self.tree_view_grouplist[group_name] = groupdic
        # 把分组加入到分组列表中
        return group_all_note

    def get_paper_widget_item(self, paper_sample: Paper_Sample):
        if len(paper_sample.image_ls) > 0:
            icon_image_name = paper_sample.image_ls[0]
            icon_image_path = os.path.join(self.conf.image_save_dir, icon_image_name)
        else:
            icon_image_path = os.path.join(self.conf.image_save_dir, 'defaut_paper_ico.jpg')

        sample_icon = QIcon(icon_image_path)  # size会自动处理

        font = QFont()
        font.setPointSize(self.conf.list_font_size)
        font.setBold(True)

        font2 = QFont()
        font2.setPointSize(self.conf.list_font_size - 2)

        child = QTreeWidgetItem()
        # 0=年份, 1=出处, 2=标题
        child.setText(0, '%s' % paper_sample.years)
        child.setText(1, '%s' % paper_sample.produce)
        child.setText(2, '%s' % paper_sample.title)
        child.paper_sample = paper_sample

        child.setFont(0, font)
        child.setFont(1, font)
        child.setFont(2, font)

        child.setIcon(0, sample_icon)

        child.setTextAlignment(0, Qt.AlignHCenter | Qt.AlignVCenter)
        return child


class _Main_window_ui():
    def __init__(self, main_win: QMainWindow, conf: Settings, paper_data: Paper_Data) -> None:
        # Actions
        self.actions_theme = [QAction(theme, main_win) for theme in ["dark", "light"]]  # 主题修改部分
        self.actions_page = (
            QAction(QIcon("icons:flip_to_front_24dp.svg"), "我的页面"),
            QAction(QIcon("icons:widgets_24dp.svg"), "页面1"),  # 换页面部分
            QAction(QIcon("icons:flip_to_front_24dp.svg"), "页面2"),
            QAction(QIcon("icons:crop_din_24dp.svg"), "页面3"),
        )
        self.actions_corner_radius = (QAction(text="rounded"), QAction(text="sharp"))  # 最好放在设置页面吧
        action_group_toolbar = QActionGroup(main_win)

        # Widgets
        self.central_window = QMainWindow()
        self.stack_widget = QStackedWidget()

        activitybar = QToolBar("activitybar")  # 左侧页面栏
        statusbar = QStatusBar()
        tool_btn_settings = QToolButton()  # 设置按钮
        spacer = QToolButton()  # 左侧页面栏的空白

        # Setup Actions
        for action in self.actions_page:
            action.setCheckable(True)
            action_group_toolbar.addAction(action)
        self.actions_page[0].setChecked(True)  # 默认进入第一页

        # Setup Widgets
        spacer.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        spacer.setEnabled(False)

        activitybar.setMovable(False)
        activitybar.addActions(self.actions_page)
        activitybar.addWidget(spacer)
        activitybar.addWidget(tool_btn_settings)

        tool_btn_settings.setIcon(QIcon("icons:settings_24dp.svg"))

        # 设置我的界面,第一页： tree view和编辑器
        self.note_editor_page = Note_editor_page_ui(conf, paper_data)
        self.stack_widget.addWidget(self.note_editor_page)

        # Layout,设置其他几个默认界面
        for ui in (WidgetsUI, DockUI, FrameUI):
            container = QWidget()
            ui().setup_ui(container)
            self.stack_widget.addWidget(container)

        self.central_window.setCentralWidget(self.stack_widget)

        main_win.setCentralWidget(self.central_window)
        main_win.addToolBar(Qt.ToolBarArea.LeftToolBarArea, activitybar)
        main_win.setStatusBar(statusbar)


class Main_window(QMainWindow):
    def __init__(self) -> None:
        self.conf = Settings()
        self.conf.load_settings()  # 初始化
        # self.paper_data=Paper_Data(self.conf)
        # self.paper_data.load()
        self.paper_data = Paper_Data.demo_data()  # 先使用demo data来看看

        """Initialize the WidgetGallery class."""
        super().__init__()
        QDir.addSearchPath("icons", f"{get_qdarktheme_root_path().as_posix()}/widget_gallery/svg")
        self._ui = _Main_window_ui(self, self.conf, self.paper_data)
        self._theme = "dark"
        self._border_radius = "rounded"

        # Signal
        for action in self._ui.actions_theme:
            action.triggered.connect(self._change_theme)
        for action in self._ui.actions_page:
            action.triggered.connect(self._change_page)
        for action in self._ui.actions_corner_radius:
            action.triggered.connect(self._change_corner_radius)

    @Slot()
    def _change_page(self) -> None:
        action_name: str = self.sender().text()  # type: ignore
        if "我的页面" in action_name:
            index = 0
        elif "页面1" in action_name:
            index = 1
        elif "页面2" in action_name:
            index = 2
        else:
            index = 3
        self._ui.stack_widget.setCurrentIndex(index)

    @Slot()
    def _change_theme(self) -> None:
        self._theme = self.sender().text()  # type: ignore
        QApplication.instance().setStyleSheet(qdarktheme.load_stylesheet(self._theme, self._border_radius))

    @Slot()
    def _change_corner_radius(self) -> None:
        self._border_radius: str = self.sender().text()  # type: ignore
        QApplication.instance().setStyleSheet(qdarktheme.load_stylesheet(self._theme, self._border_radius))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    if hasattr(Qt.ApplicationAttribute, "AA_UseHighDpiPixmaps"):  # Enable High DPI display with Qt5
        app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)  # type: ignore

    win = Main_window()
    # win.menuBar().setNativeMenuBar(False)
    # customTitlebarWindow = CustomTitlebarWindow(win)
    #
    # # customTitlebarWindow.setTopTitleBar(icon_filename='icons:settings_24dp.svg')
    # customTitlebarWindow.setButtons()
    # customTitlebarWindow.show()

    # Apply dark theme
    app.setStyleSheet(qdarktheme.load_stylesheet())

    win.show()

    app.exec()

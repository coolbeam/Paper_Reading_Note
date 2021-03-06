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

icon_ls = ['folder_open_24dp', 'palette_24dp', 'font_download_24dp',
           'circle_24dp', 'clear_24dp', 'widgets_24dp', 'flip_to_front_24dp', 'crop_din_24dp', 'settings_24dp',
           'announcement_24dp', 'contrast_24dp']
from Pyqt5_GUI.flat_editor import Paper_Note_Editor_preview
from Pyqt5_GUI.flat_note_list import Note_list


class Note_editor_page_ui(QWidget):
    def __init__(self, conf=None, paper_data=None):
        super(Note_editor_page_ui, self).__init__()
        assert isinstance(conf, Settings)
        assert isinstance(paper_data, Paper_Data)
        # ==== setup data source
        self.conf = conf
        self.paper_data = paper_data

        # ==== setup UI items
        self.note_list = Note_list(conf=self.conf, paper_data=self.paper_data)
        self.text_editor = Paper_Note_Editor_preview(settings=self.conf, paper_sample=Paper_Sample())

        # ==== setup UI actions
        self.setup_ui_actions()

        # ==== setup UI layout
        self.setup_ui_layout()

    def setup_ui_actions(self):
        # self.note_list.paper_tree_view.currentItemChanged.connect(self.on_currentItemChanged)  # ???????????????????????????????????????
        self.text_editor.year_editor.textChanged.connect(self.note_list.on_year_text_change)
        self.text_editor.produ_editor.textChanged.connect(self.note_list.on_produce_change)
        self.text_editor.title_editor.textChanged.connect(self.note_list.on_title_change)
        self.note_list.paper_tree_view.currentItemChanged.connect(self.on_currentItemChanged)  # ?????????????????????????????????????????????editor?????????????????????????????????????????????????????????????????????????????????
        self.note_list.init_set_item()

    def setup_ui_layout(self):
        # === ?????? Widgets,1?????????list ???editor???2?????????editor?????????text???view?????????
        h_splitter_1 = QSplitter(Qt.Orientation.Horizontal)
        h_splitter_1.addWidget(self.note_list)
        h_splitter_1.addWidget(self.text_editor)

        h_layout = QHBoxLayout(self)
        h_layout.addWidget(h_splitter_1)

    ''' ??????????????????  '''

    # list????????????item????????????????????????????????????item???note?????????editor??????
    def on_currentItemChanged(self, item, preitem):
        '''
        ???????????????????????????
        '''
        if item:
            # ??????????????????????????????????????????????????????
            if hasattr(item, 'paper_sample'):  # ?????????????????????note item??????????????????????????????group
                if isinstance(item.paper_sample, Paper_Sample):
                    self.text_editor.load_paper_sample(item.paper_sample)

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


class Main_window(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        QDir.addSearchPath("icons", f"{get_qdarktheme_root_path().as_posix()}/widget_gallery/svg")

        # ==== setup data source
        self.conf = Settings()
        self.conf.load_settings()  # ?????????
        self.paper_data = Paper_Data.demo_data()  # ?????????demo data?????????
        self._theme = self.conf.theme
        self._border_radius = "rounded"

        # ==== setup UI items
        self.central_window = QMainWindow()
        self.stack_widget = QStackedWidget()
        self.note_editor_page = Note_editor_page_ui(self.conf, self.paper_data)

        # ==== setup UI actions
        self.actions_theme = [QAction(theme, self) for theme in ["dark", "light"]]  # ??????????????????
        self.actions_page = (  # ???????????????
            QAction(QIcon("icons:flip_to_front_24dp.svg"), "????????????"),
            QAction(QIcon("icons:widgets_24dp.svg"), "??????1"),
            QAction(QIcon("icons:flip_to_front_24dp.svg"), "??????2"),
            QAction(QIcon("icons:crop_din_24dp.svg"), "??????3"),
        )
        self.actions_corner_radius = (QAction(text="rounded"), QAction(text="sharp"))  # ????????????????????????
        self.setup_ui_actions()

        # ==== setup UI layout
        self.setup_ui_layout()

    def setup_ui_actions(self):
        # Signal
        for action in self.actions_theme:  # ?????????
            action.triggered.connect(self._change_theme)
        for action in self.actions_page:  # ?????????
            action.triggered.connect(self._change_page)
        for action in self.actions_corner_radius:  # ????????????
            action.triggered.connect(self._change_corner_radius)

        # ??????????????????
        action_group_toolbar = QActionGroup(self)
        for action in self.actions_page:
            action.setCheckable(True)
            action_group_toolbar.addAction(action)
        self.actions_page[0].setChecked(True)  # ?????????????????????

    def setup_ui_layout(self):
        # self.setWindowFlag(Qt.FramelessWindowHint)  # ?????????
        self.setAutoFillBackground(True)
        activitybar = QToolBar("activitybar")  # ???????????????
        statusbar = QStatusBar()
        tool_btn_settings = QToolButton()  # ????????????
        spacer = QToolButton()  # ????????????????????????

        # Setup Widgets
        spacer.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        spacer.setEnabled(False)

        activitybar.setMovable(False)
        activitybar.addActions(self.actions_page)

        activitybar.addWidget(spacer)
        activitybar.addWidget(tool_btn_settings)

        tool_btn_settings.setIcon(QIcon("icons:settings_24dp.svg"))

        # ??????????????????,???????????? tree view????????????

        self.stack_widget.addWidget(self.note_editor_page)

        # Layout,??????????????????????????????
        for ui in (WidgetsUI, DockUI, FrameUI):
            container = QWidget()
            ui().setup_ui(container)
            self.stack_widget.addWidget(container)

        self.central_window.setCentralWidget(self.stack_widget)

        self.setCentralWidget(self.central_window)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, activitybar)
        self.setStatusBar(statusbar)

    @Slot()
    def _change_page(self) -> None:
        action_name: str = self.sender().text()  # type: ignore
        if "????????????" in action_name:
            index = 0
        elif "??????1" in action_name:
            index = 1
        elif "??????2" in action_name:
            index = 2
        else:
            index = 3
        self.stack_widget.setCurrentIndex(index)

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
    win.menuBar().setNativeMenuBar(False)

    # Apply dark theme
    app.setStyleSheet(qdarktheme.load_stylesheet())

    win.show()

    app.exec()

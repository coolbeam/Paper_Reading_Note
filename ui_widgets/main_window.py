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
from qdarktheme.qtpy.QtCore import QDir, Qt, Slot, QSize
from qdarktheme.util import get_qdarktheme_root_path
from qdarktheme.qtpy.QtGui import QAction, QActionGroup, QFont, QIcon, QTextOption
from qdarktheme.qtpy.QtWidgets import (
    QApplication,
    QMainWindow,
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
import qtawesome as qta

icon_ls = ['folder_open_24dp', 'palette_24dp', 'font_download_24dp',
           'circle_24dp', 'clear_24dp', 'widgets_24dp', 'flip_to_front_24dp', 'crop_din_24dp', 'settings_24dp',
           'announcement_24dp', 'contrast_24dp']
from ui_widgets.note_editor import Paper_Note_Editor_preview
from ui_widgets.note_list import Note_list
from ui_widgets.tags_dialog import Choose_Tag_ls_Dialog
import time


class Note_editor_page_ui(QWidget):
    def __init__(self, main_win=None, conf=None, paper_data=None, ):
        super(Note_editor_page_ui, self).__init__()
        assert isinstance(conf, Settings)
        assert isinstance(paper_data, Paper_Data)
        # ==== setup data source
        self.conf = conf
        self.paper_data = paper_data
        self.main_win = main_win

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
        self.text_editor.reading_progress.currentIndexChanged.connect(self.note_list.on_reading_progress_change)
        self.note_list.paper_tree_view.currentItemChanged.connect(self.on_currentItemChanged)  # ?????????????????????????????????????????????editor?????????????????????????????????????????????????????????????????????????????????
        self.note_list.init_set_item()

        self.text_editor.btn_save.clicked.connect(self.on_save_btn)
        self.text_editor.btn_save.setShortcut('ctrl+s')  # ?????????????????????

        self.text_editor.btn_tag_edit.clicked.connect(self.on_tag_edit_btn)

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
                    # print('??????paper note??? ', item.paper_sample.to_dict)
                    self.text_editor.load_paper_sample(item.paper_sample)

    # ?????????editor?????????save?????????????????????????????????save
    def on_save_btn(self):
        # print('?????????save??????')
        self.main_win.status_bar.showMessage('??????????????????', 2000)  # 2000ms
        self.paper_data.check_paper_sample_image(self.text_editor.paper_sample)
        self.paper_data.update_static_ls()
        self.main_win.save_data()

    # ?????????editor?????????save?????????????????????????????????save
    def on_tag_edit_btn(self):
        self.main_win.status_bar.showMessage('??????note tag', 2000)  # 2000ms

        chose_tag = Choose_Tag_ls_Dialog(self.text_editor.paper_sample.tags, self.paper_data.all_tags, self.conf)  # ?????????????????????????????????
        # for g in self.grouplist:
        #     adduser.comboBox.addItem(g['groupname'])
        r = chose_tag.exec_()
        if r > 0:
            self.text_editor.paper_sample.tags = chose_tag.note_tag
            self.text_editor.update_preview()
            self.paper_data.update_static_ls()
            self.note_list.item_update_favorate()
            self.main_win.status_bar.showMessage('note tag????????????', 2000)  # 2000ms

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

        # ==== setup data source ???????????????
        time_st = time.time()
        self.conf = Settings()
        self.conf.load_settings()  # ?????????
        self.paper_data = Paper_Data(self.conf)  #
        self.paper_data.load()  # ?????????????????????????????????????????????
        time_end = time.time()
        print('????????????????????? %s s' % (time_end - time_st))
        self._theme = self.conf.theme
        self._border_radius = "rounded"
        # ===== status bar
        self.status_bar = QStatusBar()

        # ==== setup UI items
        self.central_window = QMainWindow()
        self.stack_widget = QStackedWidget()
        self.note_editor_page = Note_editor_page_ui(self, self.conf, self.paper_data)

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
        self.setWindowIcon(qta.icon('mdi6.file-powerpoint-outline'))
        self.setWindowTitle('Paper Reading')
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

        # ???????????????style
        QApplication.instance().setStyleSheet(qdarktheme.load_stylesheet(self._theme, self._border_radius))

        # status bar
        self.status_bar.showMessage('Ready', 2000)  # 2000ms
        self.setStatusBar(self.status_bar)

    def save_data(self):
        self.conf.save_settings()
        self.paper_data.save()
        self.status_bar.showMessage('????????????', 2000)

    ''' ?????????????????? '''

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

    # ????????????
    def closeEvent(self, event):

        reply_box = QMessageBox.question(self, "????????????", "????????????", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply_box == QMessageBox.Yes:
            self.save_data()
            print('??????????????????????????????')
            event.accept()
        else:
            event.ignore()
        # yr_btn = reply.addButton('????????????', QWidget.QMessageBox.YesRole)
        # reply.addButton('???????????????', QWidget.QMessageBox.NoRole)
        # reply.exec_()
        # if reply.clickedButton() == yr_btn:
        #     event.accept()
        #     QWidget.qApp.quit()
        # # sys.exit(app.exec_())
        # else:
        #


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

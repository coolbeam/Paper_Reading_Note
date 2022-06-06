import sys
import os

'''
https://github.com/5yutan5/PyQtDarkTheme
'''
from utils.tools import tools
from utils.settings import Settings, Paper_Sample
from urllib.parse import urlparse
from urllib.request import url2pathname
# from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
import qdarktheme
from qdarktheme.qtpy.QtCore import QDir, Qt, Slot, pyqtSignal, QRect, QVariant, QMimeData, QUrl
from qdarktheme.util import get_qdarktheme_root_path
from qdarktheme.qtpy.QtGui import QAction, QActionGroup, QFont, QIcon, QTextOption, QPainter, QColor, QTextFormat, QTextCursor, QDropEvent, QPalette, QDesktopServices
from qdarktheme.qtpy.QtWidgets import (
    QApplication, QColorDialog, QFileDialog, QVBoxLayout, QHBoxLayout, QLabel, QMainWindow, QMenuBar,
    QMessageBox, QSizePolicy, QStackedWidget, QStatusBar, QToolBar, QToolButton, QSplitter, QLineEdit,
    QWidget, QTextEdit, QTreeWidget, QTreeWidgetItem, QAbstractItemView, QHeaderView, QFrame, QPlainTextEdit, QComboBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor
import commonmark
from markdown2 import Markdown
from Pyqt5_GUI.markdown_previewer.github_markdown_style import GITHUB_MARKDOWN_STYLE, GITHUB_MARKDOWN_STRYLE_DARK
import datetime


class CustomWebEnginePage(QWebEnginePage):
    """ Custom WebEnginePage to customize how we handle link navigation """
    # Store external windows.
    external_windows = []

    def acceptNavigationRequest(self, url, _type, isMainFrame):
        if (_type == QWebEnginePage.NavigationTypeLinkClicked):
            # Send the URL to the system default URL handler.
            QDesktopServices.openUrl(url)
            return False
        return super().acceptNavigationRequest(url, _type, isMainFrame)


class Editor(QPlainTextEdit):
    document_dropped = pyqtSignal(str)

    def __init__(self, settings: Settings):
        self.conf = settings
        self.paper_sample = Paper_Sample()

        self.view = QPlainTextEdit.__init__(self)
        self.setFrameStyle(QFrame.NoFrame)
        self.cursorPositionChanged.connect(self.highlight)
        # ===== font
        self.font = QFont()
        self.font.setStyleHint(QFont.Monospace)
        self.font.setFixedPitch(True)
        self.font.setFamily(self.conf.editor_font_family)
        self.font.setPointSize(self.conf.editor_font_size)
        self.setFont(self.font)

        # ===== clipboard
        self.clipboard = QApplication.clipboard()
        # self.clipboard.dataChanged.connect(self.clipboard_change) # debug test

    def load_paper_sample(self, paper_sample: Paper_Sample):
        self.paper_sample = paper_sample

    # 粘贴图片这里需要处理一下
    def insertFromMimeData(self, source) -> None:
        if source.hasFormat('text/plain'):
            self.insertPlainText(source.text())
            print('粘贴纯文本:', source.text())

        if source.hasFormat('application/x-qt-image'):
            im = self.clipboard.pixmap()
            a = im.toImage()
            # 保存试试
            quality = 50
            im_name = self.paper_sample.new_image_name()
            save_path = os.path.join(self.conf.image_save_dir, im_name)
            if_save = a.save(save_path, 'png', quality)
            self.insertPlainText('![image](./%s)' % im_name)
            print('粘贴图片:', if_save, save_path)

    def set_image_save_name(self, name_str):
        self.im_save_name = name_str

    # 这个只用来测试写代码用的
    def clipboard_change(self):
        pass
        # data = self.clipboard.mimeData()
        # # 获取格式信息
        # print(data.formats())
        # if (data.hasFormat('text/uri-list')):
        #     for path in data.urls():
        #         # 打印复制的路径
        #         print('复制路径:', path)
        #         # 提取字符串
        #         # s = str(path)
        #         # index1 = len(s) - s[::-1].index(".");
        #         # index2 = s.index("')");
        #         # print("提取的类型为:" + s[index1:index2])
        # # 如果是纯文本类型，打印文本的值
        # # if(data.formats() == ['text/plain']):
        # #     pass
        # if data.hasFormat('text/plain'):
        #     print('复制纯文本:', data.text())
        #
        # if data.hasFormat('application/x-qt-image'):
        #     im = self.clipboard.pixmap()
        #     a = im.toImage()
        #     # 保存试试
        #     for quality in [0, 50, 100]:
        #         # print(os.path.isdir(self.conf.main_data_dir))
        #         save_path = os.path.join(self.conf.main_data_dir, 'quality_%s.png' % quality)
        #         # save_path='../data/quality_%s.png' % quality
        #         print(save_path)
        #         if_save = a.save(save_path, 'png', quality)
        #         print(if_save)
        #     print('复制图片:', )
        # print(' ')

    def numberbar_paint(self, number_bar, event):
        font_metrics = self.fontMetrics()

        block = self.firstVisibleBlock()
        line_count = block.blockNumber()
        painter = QPainter(number_bar)
        painter.fillRect(event.rect(), self.palette().base())

        while block.isValid():
            line_count += 1
            block_top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()

            if not block.isVisible() or block_top >= event.rect().bottom():
                break

            painter.setFont(self.font)
            # painter.setPen(QColor(155, 155, 155))
            if self.conf.theme == 'dark':
                painter.setPen(QColor(155, 155, 155))
            elif self.conf.theme == 'light':
                painter.setPen(QColor(155, 155, 155))
            else:
                raise ValueError('only dark/light theme here')

            paint_rect = QRect(0, block_top, number_bar.width(), font_metrics.height())
            painter.drawText(paint_rect, Qt.AlignRight, str(line_count))

            block = block.next()

        painter.end()

    def highlight(self):
        hi_selection = QTextEdit.ExtraSelection()

        # hi_selection.format.setBackground(self.palette().alternateBase())
        if self.conf.theme == 'dark':
            lineColor = QColor(Qt.gray).lighter(60)
            hi_selection.format.setBackground(lineColor)
        elif self.conf.theme == 'light':
            hi_selection.format.setBackground(self.palette().alternateBase())
            # lineColor = QColor(Qt.gray).lighter(60)
            # hi_selection.format.setBackground(lineColor)
        else:
            raise ValueError('only dark/light theme here')
        hi_selection.format.setProperty(QTextFormat.FullWidthSelection, QVariant(True))
        hi_selection.cursor = self.textCursor()
        hi_selection.cursor.clearSelection()

        self.setExtraSelections([hi_selection])

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Tab or e.key() == Qt.Key_Backtab:
            handle_func = None

            if e.key() == Qt.Key_Backtab:
                handle_func = self.unindent

            if e.key() == Qt.Key_Tab:
                handle_func = self.indent

            cursor = self.textCursor()
            if cursor.hasSelection():
                start = cursor.blockNumber()
                cursor.setPosition(cursor.selectionEnd())
                diff = cursor.blockNumber() - start

                for n in range(diff + 1):
                    handle_func(cursor, True)
                    cursor.movePosition(QTextCursor.Up)
            else:
                handle_func(cursor, False)

            return

        QPlainTextEdit.keyPressEvent(self, e)

    def indent(self, cursor, is_block):
        if is_block:
            cursor.movePosition(QTextCursor.StartOfLine)

        cursor.insertText(" " * self.conf.editor_tab_width)

    def unindent(self, cursor, is_block):
        cursor.movePosition(QTextCursor.StartOfLine)

        curr_line = cursor.block().text()

        for char in curr_line[:self.conf.editor_tab_width]:
            if char != " ":
                break

            cursor.deleteChar()

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        url = e.mimeData().urls()[0].toString()

        if url.lower().endswith((".jpeg", ".jpg", ".png", ".gif")):
            self.textCursor().insertText("![blank]({url})".format(url=url))

        if url.lower().endswith((".txt", ".md")):
            path = url2pathname(urlparse(url).path)
            self.document_dropped.emit(path)

        # Construct dummy event in order to fire cleanup procedure in parent method
        mimeData = QMimeData()
        mimeData.setText("")
        dummyEvent = QDropEvent(
            e.posF(),
            e.possibleActions(),
            mimeData, e.mouseButtons(),
            e.keyboardModifiers()
        )

        QPlainTextEdit.dropEvent(self, dummyEvent)

    @classmethod
    def demo(cls):
        class Example(QWidget):

            def __init__(self):
                super().__init__()

                self.initUI()

            def initUI(self):
                settings = Settings()

                editor = Editor(settings)

                hbox = QHBoxLayout()
                hbox.addStretch(1)
                hbox.addWidget(editor)

                self.setLayout(hbox)

                self.setGeometry(300, 300, 600, 600)
                self.setWindowTitle('editor')
                self.show()

        conf = Settings()
        app = QApplication(sys.argv)
        ex = Example()
        app.setStyleSheet(qdarktheme.load_stylesheet(conf.theme))
        sys.exit(app.exec_())

    @classmethod
    def clipboard_demo(cls):
        app = QApplication([])
        clipboard = app.clipboard()
        data = clipboard.mimeData()
        # 获取格式信息
        print(data.formats())
        if (data.hasFormat('text/uri-list')):
            for path in data.urls():
                # 打印复制的路径
                print('复制的路径:', path)
                # 提取字符串
                # s = str(path)
                # index1 = len(s) - s[::-1].index(".");
                # index2 = s.index("')");
                # print("提取的类型为:" + s[index1:index2])
        # 如果是纯文本类型，打印文本的值
        # if(data.formats() == ['text/plain']):
        #     pass
        if data.hasFormat('text/plain'):
            print('纯文本:', data.text())


class NumberBar(QWidget):
    WIDTH_OFFSET = 10

    def __init__(self, editor: Editor, *args):
        super().__init__(*args)

        self._editor = editor
        self.adjust_width(1)

    def adjust_width(self, count):
        width = self.fontMetrics().width(str(count)) + self.WIDTH_OFFSET
        if self.width() != width:
            self.setFixedWidth(width)

    def update_contents(self, rect, scroll):
        if scroll:
            self.scroll(0, scroll)
        else:
            self.update()

    def paintEvent(self, event):
        self._editor.numberbar_paint(self, event)
        QWidget.paintEvent(self, event)


class Editor_With_Line(QFrame):
    def __init__(self, settings: Settings, *args):
        super().__init__(*args)
        self._editor = Editor(settings)
        self.conf = settings
        self._editor.setPlainText("")
        self.number_bar = NumberBar(self._editor)

        hbox = QHBoxLayout(self)
        hbox.setSpacing(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(self.number_bar)
        hbox.addWidget(self._editor)

        self._editor.blockCountChanged.connect(self.number_bar.adjust_width)
        self._editor.updateRequest.connect(self.number_bar.update_contents)

    @property
    def editor(self):
        return self._editor

    @classmethod
    def demo(cls):
        class Example(QWidget):

            def __init__(self):
                super().__init__()

                self.initUI()

            def initUI(self):
                settings = Settings()

                lneditor = Editor_With_Line(settings, *[])

                hbox = QHBoxLayout()
                hbox.addStretch(1)
                hbox.addWidget(lneditor)

                self.setLayout(hbox)

                self.setGeometry(300, 300, 600, 600)
                self.setWindowTitle('LineNumberEditor')
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


# ==== editor的部分还要加上几个line_editor: 标题，年份，出处，阅读程度，code链接，pdf下载链接，还有添加标签的模块
class Paper_Note_Editor(QWidget):
    def __init__(self, settings: Settings, *args):
        super().__init__(*args)
        self.editor = Editor(settings)
        self.conf = settings
        self.editor.setPlainText("")
        self.number_bar = NumberBar(self.editor)
        self.title_editor = QLineEdit()  # 标题
        self.year_editor = QLineEdit()  # 年份
        self.produ_editor = QLineEdit()  # 出处
        self.codeurl_editor = QLineEdit()  # code链接
        self.pdfurl_editor = QLineEdit()  # pdf下载链接
        self.reading_progress = QComboBox()

        # ===== actions
        self.setup_actions()

        # ===== UI layout,
        self.setup_ui()

    # ===== actions
    def setup_actions(self):
        self.editor.blockCountChanged.connect(self.number_bar.adjust_width)
        self.editor.updateRequest.connect(self.number_bar.update_contents)
        self.title_editor.setPlaceholderText("论文标题")
        self.year_editor.setPlaceholderText("论文年份")
        self.produ_editor.setPlaceholderText("论文出处")
        self.codeurl_editor.setPlaceholderText("代码链接")
        self.pdfurl_editor.setPlaceholderText("pdf链接")
        self.reading_progress.addItems(("1%", "20%", "50%", "80%", "99%"))

    # ===== UI layout,
    def setup_ui(self):
        def make_h_layout(widget_ls, space=0, margins=(0, 0, 0, 0)):
            temp_hbox = QHBoxLayout()
            temp_container = QWidget()
            temp_hbox.setSpacing(space)
            temp_hbox.setContentsMargins(margins[0], margins[1], margins[2], margins[3])
            for i_widget in widget_ls:
                temp_hbox.addWidget(i_widget)
            temp_container.setLayout(temp_hbox)
            return temp_container

        def make_v_layout(widget_ls, space=0, margins=(0, 0, 0, 0)):
            temp_hbox = QVBoxLayout()
            temp_container = QWidget()
            temp_hbox.setSpacing(space)
            temp_hbox.setContentsMargins(margins[0], margins[1], margins[2], margins[3])
            for i_widget in widget_ls:
                temp_hbox.addWidget(i_widget)
            temp_container.setLayout(temp_hbox)
            return temp_container

        globale_vbox = QVBoxLayout(self)  # 大的分区，分两部分，editor的部分和line输入部分

        # ===== 论文信息输入部分： 标题，年份，出处，阅读程度，code链接，pdf下载链接，还有添加标签的模块(这个感觉有点难，暂时不弄)
        title_container = make_h_layout([QLabel("标题"), self.title_editor])  # === 标题 一行
        globale_vbox.addWidget(title_container)

        # === 年份，出处，阅读进度，一行
        year_container = make_h_layout([QLabel("年份"), self.year_editor, ])
        pro_container = make_h_layout([QLabel("出处"), self.produ_editor, ], margins=[10, 0, 0, 0])  # 左侧margin
        read_container = make_h_layout([QLabel("阅读进度"), self.reading_progress, ], margins=[10, 0, 0, 0])
        year_pro_read_hbox_container = make_h_layout([year_container, pro_container, read_container])
        globale_vbox.addWidget(year_pro_read_hbox_container)

        # === 代码链接，pdf链接一行
        code_url_container = make_h_layout([QLabel("代码链接"), self.codeurl_editor, ])
        pdf_url_container = make_h_layout([QLabel("pdf链接"), self.pdfurl_editor, ], margins=[10, 0, 0, 0])
        code_pdf_read_hbox_container = make_h_layout([code_url_container, pdf_url_container])
        globale_vbox.addWidget(code_pdf_read_hbox_container)

        # ===== editor的部分
        text_editor_hbox = QHBoxLayout()
        text_editor_container = QWidget()
        text_editor_hbox.setSpacing(0)
        text_editor_hbox.setContentsMargins(0, 0, 0, 0)
        text_editor_hbox.addWidget(self.number_bar)
        text_editor_hbox.addWidget(self.editor)
        text_editor_container.setLayout(text_editor_hbox)

        globale_vbox.addWidget(text_editor_container)

    @classmethod
    def demo(cls):
        class Example(QWidget):

            def __init__(self):
                super().__init__()

                self.initUI()

            def initUI(self):
                settings = Settings()

                lneditor = Paper_Note_Editor(settings, *[])

                hbox = QHBoxLayout()
                hbox.addStretch(1)
                hbox.addWidget(lneditor)

                self.setLayout(hbox)

                self.setGeometry(300, 300, 600, 600)
                self.setWindowTitle('LineNumberEditor')
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


# 把preview也加上来了
class Paper_Note_Editor_preview(QWidget):
    def __init__(self, settings: Settings, paper_sample: Paper_Sample, *args):
        super().__init__(*args)
        self.conf = settings
        self.paper_sample = paper_sample  # 初始论文展示
        md = Markdown(extras=["fenced-code-blocks", "cuddled-lists", "code-friendly"])
        self.md = md.convert
        self.progress_dict = {"1%": 0, "20%": 1, "50%": 2, "80%": 3, "99%": 4}
        self.pmv_link_clicked = pyqtSignal(str)

        # text 编辑的部分
        self.editor = Editor(settings)
        self.number_bar = NumberBar(self.editor)
        self.title_editor = QLineEdit()  # 标题
        self.year_editor = QLineEdit()  # 年份
        self.produ_editor = QLineEdit()  # 出处
        self.codeurl_editor = QLineEdit()  # code链接
        self.pdfurl_editor = QLineEdit()  # pdf下载链接
        self.reading_progress = QComboBox()
        # preview的部分

        # self.text_viewer = QTextEdit()  # 先用俩text edit代替
        self.web_view = QWebEngineView()
        # ===== actions
        self.setup_actions()

        # ===== UI layout,
        self.setup_ui()

        # ===== init preview
        self.load_paper_sample(self.paper_sample)

    # ===== actions
    def setup_actions(self):
        self.editor.blockCountChanged.connect(self.number_bar.adjust_width)
        self.editor.updateRequest.connect(self.number_bar.update_contents)
        self.title_editor.setPlaceholderText("论文标题")
        self.year_editor.setPlaceholderText("论文年份")
        self.produ_editor.setPlaceholderText("论文出处")
        self.codeurl_editor.setPlaceholderText("代码链接")
        self.pdfurl_editor.setPlaceholderText("pdf链接")
        self.reading_progress.addItems(sorted(list(self.progress_dict.keys()), reverse=False))

        # 初始化paper sample
        self.editor.setPlainText(self.paper_sample.text)

        # 内容有变化时的事件
        self.editor.textChanged.connect(self.on_text_editor_text_change)
        self.title_editor.textChanged.connect(self.on_title_editor_text_change)
        self.year_editor.textChanged.connect(self.on_year_editor_text_change)
        self.produ_editor.textChanged.connect(self.on_produ_editor_text_change)
        self.codeurl_editor.textChanged.connect(self.on_code_editor_text_change)
        self.pdfurl_editor.textChanged.connect(self.on_pdf_editor_text_change)
        self.reading_progress.currentIndexChanged.connect(self.on_reading_progress_change)

        # web点击链接的时候用外部默认浏览器
        self.web_view.setPage(CustomWebEnginePage(self))

    # ===== UI layout,
    def setup_ui(self):
        def make_h_layout(widget_ls, space=0, margins=(0, 0, 0, 0)):
            temp_hbox = QHBoxLayout()
            temp_container = QWidget()
            temp_hbox.setSpacing(space)
            temp_hbox.setContentsMargins(margins[0], margins[1], margins[2], margins[3])
            for i_widget in widget_ls:
                temp_hbox.addWidget(i_widget)
            temp_container.setLayout(temp_hbox)
            return temp_container

        def make_v_layout(widget_ls, space=0, margins=(0, 0, 0, 0)):
            temp_hbox = QVBoxLayout()
            temp_container = QWidget()
            temp_hbox.setSpacing(space)
            temp_hbox.setContentsMargins(margins[0], margins[1], margins[2], margins[3])
            for i_widget in widget_ls:
                temp_hbox.addWidget(i_widget)
            temp_container.setLayout(temp_hbox)
            return temp_container

        # ===== 论文信息输入部分： 标题，年份，出处，阅读程度，code链接，pdf下载链接，还有添加标签的模块(这个感觉有点难，暂时不弄)
        title_container = make_h_layout([QLabel("标题"), self.title_editor])  # === 标题 一行

        # === 年份，出处，阅读进度，一行
        year_container = make_h_layout([QLabel("年份"), self.year_editor, ])
        pro_container = make_h_layout([QLabel("出处"), self.produ_editor, ], margins=[10, 0, 0, 0])  # 左侧margin
        read_container = make_h_layout([QLabel("阅读进度"), self.reading_progress, ], margins=[10, 0, 0, 0])
        year_pro_read_hbox_container = make_h_layout([year_container, pro_container, read_container])

        # === 代码链接，pdf链接一行
        code_url_container = make_h_layout([QLabel("代码链接"), self.codeurl_editor, ])
        pdf_url_container = make_h_layout([QLabel("pdf链接"), self.pdfurl_editor, ], margins=[10, 0, 0, 0])
        code_pdf_read_hbox_container = make_h_layout([code_url_container, pdf_url_container])

        # ===== text editor的部分
        text_editor_hbox = QHBoxLayout()
        text_editor_container = QWidget()
        text_editor_hbox.setSpacing(0)
        text_editor_hbox.setContentsMargins(0, 0, 0, 0)
        text_editor_hbox.addWidget(self.number_bar)
        text_editor_hbox.addWidget(self.editor)
        text_editor_container.setLayout(text_editor_hbox)

        # ===== editor的板块
        text_editor_all_v_box = make_v_layout([title_container, year_pro_read_hbox_container,
                                               code_pdf_read_hbox_container, text_editor_container], space=10)
        # =====
        h_splitter_1 = QSplitter(Qt.Orientation.Horizontal)

        h_splitter_1.addWidget(text_editor_all_v_box)
        h_splitter_1.addWidget(self.web_view)

        global_h_layout = QHBoxLayout(self)
        global_h_layout.addWidget(h_splitter_1)

    def load_paper_sample(self, paper_sample: Paper_Sample):
        def set_init_line_editor(leditor, content_str):
            if content_str == '':
                leditor.setText(content_str)#可能是想做什么特别的处理吧，但后来觉得没必要
            else:
                leditor.setText(content_str)

        self.paper_sample = paper_sample
        set_init_line_editor(self.year_editor, self.paper_sample.years)
        set_init_line_editor(self.title_editor, self.paper_sample.title)
        set_init_line_editor(self.produ_editor, self.paper_sample.produce)
        set_init_line_editor(self.codeurl_editor, self.paper_sample.code_url)
        set_init_line_editor(self.pdfurl_editor, self.paper_sample.pdf_url)
        self.editor.setPlainText(self.paper_sample.text)

        if self.paper_sample.readind_progress in self.progress_dict.keys():
            self.reading_progress.setCurrentIndex(self.progress_dict[self.paper_sample.readind_progress])
        else:
            self.reading_progress.setCurrentIndex(0)

        self.update_preview()

    def update_preview(self):
        md_text = self.paper_sample.make_markdown_text()
        self.show_web_preview(md_text)

    def show_web_preview(self, md_text):
        if self.conf.editor_markdown == 'markdown2':
            html_md = self.md(md_text)  #
        elif self.conf.editor_markdown == 'commonmark':
            html_md = commonmark.commonmark(md_text)
        else:
            raise ValueError('markdown的语法设置错误: %s' % self.conf.editor_markdown)
        if self.conf.theme == 'dark':
            text = f"<head><style>{GITHUB_MARKDOWN_STRYLE_DARK}</style></head><body>{html_md}</body>"
        elif self.conf.theme == 'light':
            text = f"<head><style>{GITHUB_MARKDOWN_STYLE}</style></head><body>{html_md}</body>"
        else:
            raise ValueError('wrong theme: %s' % self.conf.theme)
        # text = f"<head><style>{GITHUB_MARKDOWN_STYLE}</style></head><body>{html_md}</body>"
        self.web_view.setHtml(text, baseUrl=QUrl.fromLocalFile(self.conf.image_save_dir + os.path.sep))

    '''事件响应'''

    def on_text_editor_text_change(self):
        self.paper_sample.modify_date = datetime.datetime.now()
        self.paper_sample.text = self.editor.toPlainText()  # 笔记内容
        self.update_preview()

    def on_title_editor_text_change(self):
        self.paper_sample.modify_date = datetime.datetime.now()
        self.paper_sample.title = self.title_editor.text()
        self.update_preview()

    def on_year_editor_text_change(self):
        self.paper_sample.modify_date = datetime.datetime.now()
        self.paper_sample.years = self.year_editor.text()
        self.update_preview()

    def on_produ_editor_text_change(self):
        self.paper_sample.modify_date = datetime.datetime.now()
        self.paper_sample.produce = self.produ_editor.text()
        self.update_preview()

    def on_code_editor_text_change(self):
        self.paper_sample.modify_date = datetime.datetime.now()
        self.paper_sample.code_url = self.codeurl_editor.text()
        self.update_preview()

    def on_pdf_editor_text_change(self):
        self.paper_sample.modify_date = datetime.datetime.now()
        self.paper_sample.pdf_url = self.pdfurl_editor.text()
        self.update_preview()

    def on_reading_progress_change(self):
        self.paper_sample.modify_date = datetime.datetime.now()
        self.paper_sample.readind_progress = self.reading_progress.currentText()
        self.update_preview()

    # 就是为了展示一下看看markdown
    def demo_show_welcome(self):
        self.welcome_text = """ PreView
        ===


        Overview
        ---

        Supports **bold**, *italic* and ***bold-italic***!
        Inline `code` is possible, too!

        Images can be inserted using drag and drop or the corresponding MD syntax.

        ```
        #include<stdio.h>
        int main() {
            printf("Hello world!\n");
        }
        ```

        > A famous quote!
        > Multiline!

        * Unordered
        * foo

        1. Ordered
        2. bar

        ###### I am a tiny header!

        Types of links: <https://github.com/> [GitHub](https://github.com/)

        CLI usage
        ---

        `$ pymarkview -i "input.md" -o "output.html"`

        show image
        ---
        ![temp](./temp.png)
                                 """
        self.show_web_preview(self.welcome_text)

    @classmethod
    def demo(cls):
        class Example(QWidget):

            def __init__(self):
                super().__init__()

                self.initUI()

            def initUI(self):
                settings = Settings()

                lneditor = Paper_Note_Editor_preview(settings, Paper_Sample(text='论文笔记', code_url='https://www.baidu.com/'), *[])

                hbox = QHBoxLayout()
                # hbox.addStretch(1)
                hbox.addWidget(lneditor)

                self.setLayout(hbox)

                self.setGeometry(300, 300, 600, 600)
                self.setWindowTitle('LineNumberEditor')
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

    Paper_Note_Editor_preview.demo()

from utils.tools import tools
from utils.settings import Settings
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from urllib.parse import urlparse
from urllib.request import url2pathname
import os
import qdarktheme
from qdarktheme.qtpy.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QWidget, QTextEdit,QFrame,QPlainTextEdit
)
'''
todo:  
1. change font
2. change style
3. copy paste image[doing]
4. highlight markdown tags
5. add shortkey
'''


class NumberBar(QWidget):
    WIDTH_OFFSET = 10

    def __init__(self, editor, *args):
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


class Editor(QPlainTextEdit):
    document_dropped = pyqtSignal(str)

    def __init__(self, settings: Settings):
        self.settings = settings

        self.view = QPlainTextEdit.__init__(self)
        self.setFrameStyle(QFrame.NoFrame)
        self.cursorPositionChanged.connect(self.highlight)
        # ===== font
        self.font = QFont()
        self.font.setStyleHint(QFont.Monospace)
        self.font.setFixedPitch(True)
        self.font.setFamily(self.settings.editor_font_family)
        self.font.setPointSize(self.settings.editor_font_size)
        self.setFont(self.font)

        # ===== clipboard
        self.clipboard = QApplication.clipboard()
        # self.clipboard.dataChanged.connect(self.clipboard_change) # debug test

    def insertFromMimeData(self, source) -> None:
        if source.hasFormat('text/plain'):
            self.insertPlainText(source.text())
            print('纯文本:', source.text())

        if source.hasFormat('application/x-qt-image'):
            im = self.clipboard.pixmap()
            a = im.toImage()
            # 保存试试
            quality = 50
            save_path = os.path.join(self.settings.main_data_dir, 'quality_%s.png' % quality)
            if_save = a.save(save_path, 'png', quality)
            self.insertPlainText('![image](file:///%s)' % save_path)
            print('图片:', if_save, save_path)

    def clipboard_change(self):
        data = self.clipboard.mimeData()
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

        if data.hasFormat('application/x-qt-image'):
            im = self.clipboard.pixmap()
            a = im.toImage()
            # 保存试试
            for quality in [0, 50, 100]:
                # print(os.path.isdir(self.settings.main_data_dir))
                save_path = os.path.join(self.settings.main_data_dir, 'quality_%s.png' % quality)
                # save_path='../data/quality_%s.png' % quality
                print(save_path)
                if_save = a.save(save_path, 'png', quality)
                print(if_save)
            print('图片:', )
        print(' ')

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
            painter.setPen(QColor(155, 155, 155))

            paint_rect = QRect(0, block_top, number_bar.width(), font_metrics.height())
            painter.drawText(paint_rect, Qt.AlignRight, str(line_count))

            block = block.next()

        painter.end()

    def highlight(self):
        hi_selection = QTextEdit.ExtraSelection()

        # hi_selection.format.setBackground(self.palette().alternateBase())
        hi_selection.format.setBackground(self.palette().alternateBase())
        # linecolor = QColor(192,253,123).lighter(60)
        # hi_selection.format.setBackground(linecolor)

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

        cursor.insertText(" " * self.settings.editor_tab_width)

    def unindent(self, cursor, is_block):
        cursor.movePosition(QTextCursor.StartOfLine)

        curr_line = cursor.block().text()

        for char in curr_line[:self.settings.editor_tab_width]:
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

        app = QApplication(sys.argv)
        ex = Example()
        # app.setStyleSheet(qdarktheme.load_stylesheet())
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


class LineNumberEditor(QFrame):
    def __init__(self, settings: Settings, *args):
        super().__init__(*args)
        self._editor = Editor(settings)
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

                lneditor = LineNumberEditor(settings, *[])

                hbox = QHBoxLayout()
                hbox.addStretch(1)
                hbox.addWidget(lneditor)

                self.setLayout(hbox)

                self.setGeometry(300, 300, 600, 600)
                self.setWindowTitle('LineNumberEditor')
                self.show()

        app = QApplication(sys.argv)
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

    Editor.demo()

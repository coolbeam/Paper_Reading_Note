from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from urllib.parse import urlparse
from urllib.request import url2pathname


class LineNumberEditor(QFrame):
    def __init__(self, settings, *args):
        super().__init__(*args)

        self._editor = self.Editor(settings)
        self._editor.setPlainText("")
        self.number_bar = self.NumberBar(self._editor)

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

        def __init__(self, settings):
            self.settings = settings

            self.view = QPlainTextEdit.__init__(self)
            self.setFrameStyle(QFrame.NoFrame)

            self.font = QFont()
            self.font.setStyleHint(QFont.Monospace)
            self.font.setFixedPitch(True)
            self.font.setFamily(self.settings.font_family)
            self.font.setPointSize(self.settings.font_size)
            self.setFont(self.font)

            self.cursorPositionChanged.connect(self.highlight)

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

            hi_selection.format.setBackground(self.palette().alternateBase())
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

            cursor.insertText(" " * self.settings.tab_width)

        def unindent(self, cursor, is_block):
            cursor.movePosition(QTextCursor.StartOfLine)

            curr_line = cursor.block().text()

            for char in curr_line[:self.settings.tab_width]:
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
        class setting():
            font_family = 'Consolas'
            font_size = 12
            tab_width = 2

        class Example(QWidget):

            def __init__(self):
                super().__init__()

                self.initUI()

            def initUI(self):
                settings = setting()

                lneditor = LineNumberEditor(settings,*[])

                hbox = QHBoxLayout()
                hbox.addStretch(1)
                hbox.addWidget(lneditor)

                self.setLayout(hbox)

                self.setGeometry(300, 300, 600, 600)
                self.setWindowTitle('LineNumberEditor')
                self.show()


        app = QApplication(sys.argv)
        ex = Example()
        sys.exit(app.exec_())


if __name__ == '__main__':
    import sys

    LineNumberEditor.demo()

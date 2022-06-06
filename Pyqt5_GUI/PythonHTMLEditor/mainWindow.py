# - Project: HTML Editor
# - Version: 0.2
# - File   : mainWindow.py
# - Author : Laurens Nolting

from Pyqt5_GUI.PythonHTMLEditor.highlighter import *
from Pyqt5_GUI.PythonHTMLEditor.keywords import *

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MainWindow(QMainWindow):
    def __init__(self, userSettings):
        super().__init__()

        self.openedFilePath = ""
        self.saved = True

        self.shouldFormat = True
        self.cursorPosOne = 0
        self.cursorPosTwo = 0
        self.tag = ""
        self.didSetPosOne = False
        self.didSetTag = False

        self.setWindowTitle("HTML Editor - New File")

        # - Settings - #
        self.userSettings = userSettings

        self.font = QFont()
        self.font.setFamily(userSettings["FONT_FAMILY"])
        self.font.setPointSize(int(userSettings["FONT_SIZE"]))

        self.fontMetrics = QFontMetrics(self.font)
        self.tabWidth = int(userSettings["TAB_WIDTH"])
        self.tabSize = self.tabWidth * self.fontMetrics.width(" ")

        self.bgColorArray = [ int(x) for x in self.userSettings["BACKGROUND_COLOR"].strip("[]").split(",") ]
        self.bgColor = QColor(self.bgColorArray[0], self.bgColorArray[1], self.bgColorArray[2])

        self.textColorArray = [ int(x) for x in self.userSettings["TEXT_COLOR"].strip("[]").split(",") ]
        self.textColor = QColor(self.textColorArray[0], self.textColorArray[1], self.textColorArray[2])

        self.tagColorArray = [ int(x) for x in self.userSettings["TAG_COLOR"].strip("[]").split(",") ]
        self.tagColor = QColor(self.tagColorArray[0], self.tagColorArray[1], self.tagColorArray[2])

        self.tagPropertyColorArray = [ int(x) for x in self.userSettings["TAG_PROPERTY_COLOR"].strip("[]").split(",") ]
        self.tagPropertyColor = QColor(self.tagPropertyColorArray[0], self.tagPropertyColorArray[1], self.tagPropertyColorArray[2])

        self.cssColorArray = [ int(x) for x in self.userSettings["CSS_COLOR"].strip("[]").split(",") ]
        self.cssColor = QColor(self.cssColorArray[0], self.cssColorArray[1], self.cssColorArray[2])

        self.cssPropertyColorArray = [ int(x) for x in self.userSettings["CSS_PROPERTY_COLOR"].strip("[]").split(",") ]
        self.cssPropertyColor = QColor(self.cssPropertyColorArray[0], self.cssPropertyColorArray[1], self.cssPropertyColorArray[2])

        self.stringColorArray = [ int(x) for x in self.userSettings["STRING_COLOR"].strip("[]").split(",") ]
        self.stringColor = QColor(self.stringColorArray[0], self.stringColorArray[1], self.stringColorArray[2])

        self.commentColorArray = [ int(x) for x in self.userSettings["COMMENT_COLOR"].strip("[]").split(",") ]
        self.commentColor = QColor(self.commentColorArray[0], self.commentColorArray[1], self.commentColorArray[2])

        self.editorPalette = QPalette()
        self.editorPalette.setColor(QPalette.Base, self.bgColor)
        self.editorPalette.setColor(QPalette.Text, self.textColor)

        # - Toolbar - #
        toolbar = self.addToolBar("File")

        newAction = QAction("New", self)
        newAction.triggered.connect(self.newFileAction)
        toolbar.addAction(newAction)

        openAction = QAction("Open", self)
        openAction.triggered.connect(self.openFileAction)
        toolbar.addAction(openAction)

        saveAction = QAction("Save", self)
        saveAction.triggered.connect(self.saveFileAction)
        toolbar.addAction(saveAction)

        settingsAction = QAction("Settings", self)
        settingsAction.triggered.connect(self.settingsAction)
        toolbar.addAction(settingsAction)

        # - HBox Widget - #
        self.pane = QWidget()
        hbox = QHBoxLayout(self.pane)
        hbox.setContentsMargins(8, 8, 8, 8)
        self.setCentralWidget(self.pane)

        # - Editor - #
        self.editor = QPlainTextEdit()
        self.editor.textChanged.connect(self.didChangeText)
        self.editor.setFont(self.font)
        self.editor.setTabStopWidth(self.tabSize)
        self.editor.setPalette(self.editorPalette)
        self.editor.setLineWrapMode(False)

        # - Highlighter - #
        self.highlighter = SyntaxHighlighter(self.tagColor, self.tagPropertyColor,
                                             self.cssColor, self.cssPropertyColor,
                                             self.stringColor, self.commentColor,
                                             self.editor.document())

        # - Previewer - #
        self.previewer = QWebEngineView()

        # - Splitter - #
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.editor)
        splitter.addWidget(self.previewer)
        splitter.setSizes([300, 300])
        hbox.addWidget(splitter)

        # - Statusbar - #
        self.statusBar().setStyleSheet("font-family: \"Menlo\", sans-serif; font-size: 10px;")
        self.statusBar().showMessage(str(self.editor.textCursor().blockNumber()))

        self.pane.setLayout(hbox)
        self.pane.show()

    def newFileAction(self):
        return

    def openFileAction(self):
        fname = QFileDialog.getOpenFileName(self, "Open HTML File")

        if fname[0]:
            self.openedFilePath = fname[0]
            self.setWindowTitle("HTML Editor - " + self.openedFilePath)
            with open(fname[0], "r") as f:
                data = f.read()
                self.editor.clear()
                self.editor.setPlainText(data)
                f.close()

    def saveFileAction(self):
        self.saved = True

        if self.windowTitle()[len(self.windowTitle()) - 1:] == "*":
            self.setWindowTitle(self.windowTitle()[:-1])

        return

    def settingsAction(self):
        return

    def getStringBeforeLocation(self, string, location):
        return string[location - 1:location]

    def ArrayContainsString(self, string, array):
        if len(array) != 0:
            for i in array:
                if i == string:
                    return True
        else:
            return False

    def getTabsInlineBeforeChars(self, line):
        tabs = 0
        for c in line:
            if c == "\t":
                tabs += 1
            else:
                return tabs
        return tabs

    def didChangeText(self):
        if self.windowTitle()[len(self.windowTitle()) - 1] != "*":
            self.setWindowTitle(self.windowTitle() + "*")

        self.statusBar().showMessage(str(self.editor.textCursor().blockNumber()))
        self.previewer.setHtml(self.editor.toPlainText(), QUrl(""))
        self.format()

    def format(self):
        cursor = self.editor.textCursor()
        htmlString = self.editor.toPlainText()

        if self.getStringBeforeLocation(htmlString, cursor.position()) == "{":
            tabsInPrevLine = self.getTabsInlineBeforeChars(htmlString.splitlines()[cursor.blockNumber()])
            tabStrOne = "\t" * (tabsInPrevLine + 1)
            tabStrTwo = "\t" * tabsInPrevLine
            cursor.insertText("\r" + tabStrOne + "\r" + tabStrTwo + "}")
            cursor.movePosition(QTextCursor.MoveOperation(9), QTextCursor.MoveMode(0), 2 + tabsInPrevLine)
            self.editor.setTextCursor(cursor)

        if self.shouldFormat:
            if self.getStringBeforeLocation(htmlString, cursor.position()) == "<":
                self.cursorPosOne = cursor.position()
                self.didSetPosOne = True

            if self.ArrayContainsString(htmlString[self.cursorPosOne : cursor.position()], HTML_KEYWORDS_ALL):
                self.tag = htmlString[self.cursorPosOne : cursor.position()]
                self.cursorPosTwo = cursor.position()
                self.didSetTag = True

            if self.getStringBeforeLocation(htmlString, cursor.position()) == ">":
                if self.didSetPosOne and self.didSetTag:
                    closeTag = "</" + self.tag + ">"
                    tabsInPrevLine = self.getTabsInlineBeforeChars(htmlString.splitlines()[cursor.blockNumber()])
                    tabStrOne = "\t" * (tabsInPrevLine + 1)
                    tabStrTwo = "\t" * tabsInPrevLine

                    if self.ArrayContainsString(self.tag, HTML_INLINE_KEYWORDS):
                        self.shouldFormat = False
                        cursor.insertText(closeTag)
                        self.shouldFormat = True
                        cursor.movePosition(QTextCursor.MoveOperation(9), QTextCursor.MoveMode(0), 3 + len(self.tag))
                    else:
                        self.shouldFormat = False
                        cursor.insertText("\r" + tabStrOne + "\r" + tabStrTwo + closeTag)
                        self.shouldFormat = True
                        cursor.movePosition(QTextCursor.MoveOperation(9), QTextCursor.MoveMode(0), 4 + len(self.tag) + tabsInPrevLine)

                    self.editor.setTextCursor(cursor)

                    self.cursorPosOne = 0
                    self.cursorPosTwo = 0
                    self.tag = ""
                    self.didSetPosOne = False
                    self.didSetTag = False

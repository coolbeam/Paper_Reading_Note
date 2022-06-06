# - Project: HTML Editor
# - Version: 0.2
# - File   : highlighter.py
# - Author : Laurens Nolting

# - Reference: http://carsonfarmer.com/2009/07/syntax-highlighting-with-pyqt/ - #

from PyQt5.QtGui import *
from PyQt5.QtCore import *

# from keywords import HTML_KEYWORDS_ALL

class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, tagColor, tagPropertyColor,
                       cssColor, cssPropertyColor,
                       stringColor, commentColor, parent=None):
        super(SyntaxHighlighter, self).__init__(parent)

        self.shouldHighlight = True

        # - Color - #
        self.tagColor = tagColor
        self.tagPropertyColor = tagPropertyColor
        self.cssColor = cssColor
        self.cssPropertyColor = cssPropertyColor
        self.stringColor = stringColor
        self.commentColor = commentColor

        self.highlightingRules = []

        # - HTML Tags (e.g. <html>) - #
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(self.tagColor)
        self.highlightingRules.append((QRegExp("<([^>]+)>"), keywordFormat))

        """keywordPatterns = []

        for keyword in HTML_KEYWORDS_ALL:
            keywordPatterns.append("<" + keyword + ".*>")
            keywordPatterns.append("</" + keyword + ">")

        self.highlightingRules = [(QRegExp(pattern), keywordFormat) for pattern in keywordPatterns]"""

        # - HTML Tag Property (e.g. href="") - #
        tagPropertyFormat = QTextCharFormat()
        tagPropertyFormat.setForeground(self.tagPropertyColor)
        self.highlightingRules.append((QRegExp("[^\s]+="), tagPropertyFormat))

        # - CSS (e.g. body {}) - #
        cssFormat = QTextCharFormat()
        cssFormat.setForeground(self.cssColor)
        self.highlightingRules.append((QRegExp("^.*(?=\s+\{)"), cssFormat))

        # - CSS Property (e.g. font-family: ) - #
        cssPropertyFormat = QTextCharFormat()
        cssPropertyFormat.setForeground(self.cssPropertyColor)
        self.highlightingRules.append((QRegExp("([^\s]+)(?=: )"), cssPropertyFormat))

        # - Strings - #
        stringBrush = QBrush(self.stringColor, Qt.SolidPattern)
        stringFormat = QTextCharFormat()
        stringFormat.setForeground(stringBrush)
        stringPattern = QRegExp("\".*\"")
        stringPattern.setMinimal(True)
        self.highlightingRules.append((stringPattern, stringFormat))

        # - Comment - #
        commentBrush = QBrush(self.commentColor, Qt.SolidPattern)
        commentFormat = QTextCharFormat()
        commentFormat.setForeground(commentBrush)
        self.highlightingRules.append((QRegExp("/\*.*\*/"), commentFormat))
        self.highlightingRules.append((QRegExp("<!--.*-->"), commentFormat))

    def highlightBlock(self, text):
        if self.shouldHighlight:
            for pattern, format in self.highlightingRules:
                expression = QRegExp(pattern)
                index = expression.indexIn(text)

                while index >= 0:
                    length = expression.matchedLength()
                    self.setFormat(index, length, format)
                    index = expression.indexIn(text, index + length)

            self.setCurrentBlockState(0)

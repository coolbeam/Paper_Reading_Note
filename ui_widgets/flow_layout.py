# coding:utf-8
from qdarktheme.qtpy.QtCore import QSize, QPoint, Qt, QMargins, QRect
from qdarktheme.qtpy.QtWidgets import QLayout, QApplication, QWidget, QPushButton
import qdarktheme


class FlowLayout(QLayout):
    """ Flow layout """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__items = []
        self.__verticalSpacing = 10
        self.__horizontalSpacing = 10

    def __contains__(self, item):
        if item in self.__items:
            return True
        else:
            return False

    def addItem(self, item):
        self.__items.append(item)

    def count(self):
        return len(self.__items)

    def itemAt(self, index: int):
        if 0 <= index < len(self.__items):
            return self.__items[index]

        return None

    def takeAt(self, index: int):
        if 0 <= index < len(self.__items):
            return self.__items.pop(index)

        return None

    def removeAllWidgets(self):
        """ remove all widgets from layout """
        while self.__items:
            self.takeAt(0)

    def expandingDirections(self):
        return Qt.Orientation(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width: int):
        """ get the minimal height according to width """
        return self.__doLayout(QRect(0, 0, width, 0), False)

    def setGeometry(self, rect: QRect):
        super().setGeometry(rect)
        self.__doLayout(rect, True)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()

        for item in self.__items:
            size = size.expandedTo(item.minimumSize())

        m = self.contentsMargins()
        size += QSize(m.left() + m.right(), m.top() + m.bottom())

        return size

    def setVerticalSpacing(self, spacing: int):
        """ set vertical spacing between widgets """
        self.__verticalSpacing = spacing

    def verticalSpacing(self):
        """ get vertical spacing between widgets """
        return self.__verticalSpacing

    def setHorizontalSpacing(self, spacing: int):
        """ set horizontal spacing between widgets """
        self.__horizontalSpacing = spacing

    def horizontalSpacing(self):
        """ get horizontal spacing between widgets """
        return self.__horizontalSpacing

    def __doLayout(self, rect: QRect, move: bool):
        """ adjust widgets position according to the window size """
        margin = self.contentsMargins()
        x = rect.x() + margin.left()
        y = rect.y() + margin.top()
        rowHeight = 0
        spaceX = self.horizontalSpacing()
        spaceY = self.verticalSpacing()

        for item in self.__items:
            nextX = x + item.sizeHint().width() + spaceX

            if nextX - spaceX > rect.right() and rowHeight > 0:
                x = rect.x() + margin.left()
                y = y + rowHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                rowHeight = 0

            if move:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = nextX
            rowHeight = max(rowHeight, item.sizeHint().height())
        return y + rowHeight - rect.y()

    @classmethod
    def demo(cls):
        import sys
        class Demo(QWidget):

            def __init__(self):
                super().__init__()
                layout = FlowLayout(self)

                layout.setContentsMargins(30, 30, 30, 30)
                layout.setVerticalSpacing(20)
                layout.setHorizontalSpacing(10)

                layout.addWidget(QPushButton('aiko'))
                layout.addWidget(QPushButton('刘静爱'))
                layout.addWidget(QPushButton('柳井爱子'))
                layout.addWidget(QPushButton('aiko 赛高'))
                layout.addWidget(QPushButton('aiko 太爱啦😘'))

                self.resize(250, 300)
                # self.setStyleSheet('Demo{background: white} QPushButton{padding: 5px 10px; font:15px "Microsoft YaHei"}')

        app = QApplication(sys.argv)

        w = Demo()
        app.setStyleSheet(qdarktheme.load_stylesheet('dark'))
        w.show()
        app.exec_()


if __name__ == '__main__':
    FlowLayout.demo()

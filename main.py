import sys
import os
from qdarktheme.qtpy.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui_widgets.main_window import Main_window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    if hasattr(Qt.ApplicationAttribute, "AA_UseHighDpiPixmaps"):  # Enable High DPI display with Qt5
        app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)  # type: ignore

    win = Main_window()
    # win.menuBar().setNativeMenuBar(False)
    # Apply dark theme
    # app.setStyleSheet(qdarktheme.load_stylesheet())
    win.show()

    app.exec()

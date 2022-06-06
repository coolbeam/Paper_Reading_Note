# - Project: HTML Editor
# - Version: 0.2
# - File   : main.py
# - Author : Laurens Nolting

import sys
from Pyqt5_GUI.PythonHTMLEditor.mainWindow import MainWindow
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    settings = {}

    with open("sampleSettings.txt", "r") as f:
        for line in f.readlines():
            values = line.split(":")
            settings[str(values[0])] = str(values[1]).strip("\n")
        f.close()

    app = QApplication(sys.argv)
    mainWindow = MainWindow(settings)

    mainWindow.show()
    sys.exit(app.exec_())

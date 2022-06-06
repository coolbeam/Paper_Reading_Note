# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\PyQt5\PyQt540\ui.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(255, 678)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("res/logo.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.bt_search = QtWidgets.QToolButton(Form)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("res/search.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_search.setIcon(icon1)
        self.bt_search.setIconSize(QtCore.QSize(32, 32))
        self.bt_search.setAutoRaise(True)
        self.bt_search.setObjectName("bt_search")
        self.horizontalLayout.addWidget(self.bt_search)
        self.bt_adduser = QtWidgets.QToolButton(Form)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../../data/res/add.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_adduser.setIcon(icon2)
        self.bt_adduser.setIconSize(QtCore.QSize(32, 32))
        self.bt_adduser.setAutoRaise(True)
        self.bt_adduser.setObjectName("bt_adduser")
        self.horizontalLayout.addWidget(self.bt_adduser)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.treeWidget = QtWidgets.QTreeWidget(Form)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.verticalLayout.addWidget(self.treeWidget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "公众号：学点编程吧--TIM模拟"))
        self.bt_search.setToolTip(_translate("Form", "查找联系人"))
        self.bt_search.setWhatsThis(_translate("Form", "查找联系人"))
        self.bt_search.setText(_translate("Form", "..."))
        self.bt_adduser.setToolTip(_translate("Form", "新增好友"))
        self.bt_adduser.setWhatsThis(_translate("Form", "新增好友"))
        self.bt_adduser.setText(_translate("Form", "..."))
        self.treeWidget.setWhatsThis(_translate("Form", "TIM模拟"))

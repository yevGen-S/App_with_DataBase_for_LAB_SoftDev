# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(798, 615)
        MainWindow.setStyleSheet(u"QWidget{ \n"
"	\n"
"	border-radius : 15 px;\n"
"	background-color: rgb(65, 64, 66);\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.menuFrame = QFrame(self.centralwidget)
        self.menuFrame.setObjectName(u"menuFrame")
        self.menuFrame.setGeometry(QRect(0, -30, 71, 611))
        self.menuFrame.setFrameShape(QFrame.StyledPanel)
        self.menuFrame.setFrameShadow(QFrame.Raised)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
    # retranslateUi


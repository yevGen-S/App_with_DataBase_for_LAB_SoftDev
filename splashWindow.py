# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'splashWindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_SplashWindow(object):
    def setupUi(self, SplashWindow):
        if not SplashWindow.objectName():
            SplashWindow.setObjectName(u"SplashWindow")
        SplashWindow.resize(640, 250)
        SplashWindow.setMinimumSize(QSize(640, 250))
        SplashWindow.setBaseSize(QSize(640, 300))
        self.centralwidget = QWidget(SplashWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splashFrame = QFrame(self.centralwidget)
        self.splashFrame.setObjectName(u"splashFrame")
        self.splashFrame.setMinimumSize(QSize(0, 0))
        self.splashFrame.setStyleSheet(u"QFrame { \n"
"	\n"
"	border-radius : 15 px;\n"
"	background-color: rgb(65, 64, 66);\n"
"}")
        self.splashFrame.setFrameShape(QFrame.StyledPanel)
        self.splashFrame.setFrameShadow(QFrame.Raised)
        self.label_title = QLabel(self.splashFrame)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setGeometry(QRect(0, 40, 621, 51))
        font = QFont()
        font.setFamily(u"Montserrat")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet(u"QLabel { \n"
"rgb(31, 31, 31)\n"
"\n"
"}")
        self.label_title.setTextFormat(Qt.MarkdownText)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.progress_bar = QProgressBar(self.splashFrame)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setGeometry(QRect(60, 160, 511, 9))
        self.progress_bar.setStyleSheet(u"QProgressBar{\n"
"\n"
"}\n"
"QProgressBar::chunk{\n"
"	\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
"}")
        self.progress_bar.setValue(24)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.label_loading = QLabel(self.splashFrame)
        self.label_loading.setObjectName(u"label_loading")
        self.label_loading.setGeometry(QRect(250, 180, 131, 17))
        font1 = QFont()
        font1.setFamily(u"Montserrat")
        font1.setPointSize(8)
        font1.setItalic(True)
        font1.setUnderline(False)
        self.label_loading.setFont(font1)
        self.label_loading.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.splashFrame)

        SplashWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(SplashWindow)

        QMetaObject.connectSlotsByName(SplashWindow)
    # setupUi

    def retranslateUi(self, SplashWindow):
        SplashWindow.setWindowTitle(QCoreApplication.translate("SplashWindow", u"MainWindow", None))
        self.label_title.setText(QCoreApplication.translate("SplashWindow", u"<strong>Software</strong> Developmnet Company DB ", None))
        self.label_loading.setText(QCoreApplication.translate("SplashWindow", u"<strong>DB</strong> loading ...", None))
    # retranslateUi


import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from DB_class import MyDbRequests
from splashWindow import Ui_SplashWindow
import pickle
from windowActions import *
from mainWindowV2 import Ui_MainWindow

counter = 0


# main window of the app

class MainWindowV2(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        MyDbRequests()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.action = WindowActions(self.ui)
        self.setWindowTitle("SDC DB")


        try:
            with open("datadump.txt", "rb") as file:
                self.ui.date.setDate(pickle.load(file))
                deadline = self.ui.date.setDate(pickle.load(self.file)).addDays(random.randint(1, 2))
        except:
            pass






    def closeEvent(self, QCloseEvent):
        with open("datadump.txt", "wb") as file:
            pickle.dump(self.ui.date.date(), file)
        super().closeEvent(QCloseEvent)


#     def center(self):
#         qr = self.frameGeometry()
#         cp = QDesktopWidget().availableGeometry().center()
#         qr.moveCenter(cp)
#         self.move(qr.topLeft())
#
#
# # loading screen
# class SplashWindow(QMainWindow):
#     def __init__(self):
#         QMainWindow.__init__(self)
#         self.ui = Ui_SplashWindow()
#         self.ui.setupUi(self)
#         self.center()
#
#         self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
#         self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
#
#         self.timer = QtCore.QTimer()
#         self.timer.timeout.connect(self.progress)
#         # TIMER IN MILLISECONDS
#         self.timer.start(15)
#
#         self.show()
#
#     def center(self):
#         qr = self.frameGeometry()
#         cp = QDesktopWidget().availableGeometry().center()
#         qr.moveCenter(cp)
#         self.move(qr.topLeft())
#
#
#
#     def progress(self):
#         global counter
#         self.ui.progress_bar.setValue(counter)
#         if counter > 100:
#             self.timer.stop()
#             self.main = MainWindowV2()
#             self.main.show()
#             self.close()
#         counter += 1
#


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindowV2()
    window.show()
    sys.exit(app.exec_())

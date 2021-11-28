import random

from DB_class import MyDbRequests
from employee_table_model import EmployeeTableModel
from report_current_projects import CurrentProjectModel
from report_list_of_staff import ListOfStaffModel
from projects_to_end_table import ProjectsToEndTable
from testers_table import TesterTableModel
from developers_table import DevelopersTableModel
from mainWindowV2 import Ui_MainWindow
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtChart
from PyQt5.QtChart import QChartView
import pickle


class WindowActions:
    def __init__(self, ui: Ui_MainWindow):
        self.ui = ui
        self.connectActionsToTabQueries()

        self.ui.btnDiagram.clicked.connect(self.diagramHandler)


        self.ui.projectBox.addItems(MyDbRequests.getAllProjects())

        self.tableModel = EmployeeTableModel()
        self.ui.tableEmployees.setModel(self.tableModel)

        self.tableModelTesters = TesterTableModel()
        self.ui.tableTesters.setModel(self.tableModelTesters)

        self.tableModelDevelopers = DevelopersTableModel()
        self.ui.tableDevelopers.setModel(self.tableModelDevelopers)

        self.tableModelCurrentProjects = CurrentProjectModel()
        self.ui.tableCurrentProjects.setModel(self.tableModelCurrentProjects)

        self.tableModelListOfStaff = ListOfStaffModel()
        self.ui.tableListOfStaff.setModel(self.tableModelListOfStaff)

        self.tableModelProjectsToEnd = ProjectsToEndTable()
        self.ui.tableProjectsToEnd.setModel(self.tableModelProjectsToEnd)

        self.errorMessage = QMessageBox()

        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.ui.date.setDate(self.ui.date.date().addDays(2)))
        self.timer.start(1000)

        self.timer_bug_gen = QTimer()
        self.timer.timeout.connect(
            lambda: MyDbRequests.getRandomBug(self.ui.date.date().toString(), self.ui.date.date().toString()))
        self.timer_bug_gen.timeout.connect(lambda: MyDbRequests.randFix())
        self.timer.timeout.connect(self.updateFiringTablesHandler)
        self.timer_bug_gen.start(1000)

        # fire an employee
        self.ui.btnDismiss.clicked.connect(lambda: MyDbRequests.fireEmployee(7, 7))

        # transfer page functionality

        self.ui.comboBoxEmployee.currentTextChanged.connect(self.comboBoxTransferingHandler)
        self.ui.btnTransfer.clicked.connect(self.switchTransferPageHandler)

        self.ui.btnTransferEmployee.clicked.connect(self.btnTransferEmployeeHandler)

        # Handler to update info for recruiters
        self.ui.btnRecruit.clicked.connect(self.switchPageHandler)

        # stacked pages
        self.ui.btnStartProject.clicked.connect(
            lambda: self.ui.frameQueriesPages.setCurrentWidget(self.ui.startProjectPage))

        self.ui.btnEndProject.clicked.connect(self.switchToEndingPageHandler)
        self.ui.comboBoxEmployee.addItems(MyDbRequests.getAllEmployees())
        self.ui.btnTransfer.clicked.connect(lambda: self.ui.frameQueriesPages.setCurrentWidget(self.ui.transferPage))

        self.ui.btnFire.clicked.connect(self.switchFiringPageHadler)

        # handler to update report of current projects
        self.ui.btnCurrentProjects.clicked.connect(self.switchReportsHandler)

        self.ui.btnListOfStaff.clicked.connect(self.switchListOfStaffHandler)
        self.ui.btnDiagram.clicked.connect(lambda: self.ui.reportPages.setCurrentWidget(self.ui.reportDiagram))

        # Transfer page/ add to project btn
        self.ui.btnAddToProject.clicked.connect(
            lambda: MyDbRequests.addEmployeeToProject(self.ui.comboBoxEmployee.currentText(),
                                                      self.ui.comboBoxProjectsWhereToAdd.currentText()))

    def diagramHandler(self):
        self.data = MyDbRequests.getInfoForDiagram()
        self.series = QtChart.QBarSeries()
        for i in range(len(self.data)):
            set = QtChart.QBarSet(f"{self.data[i][0]}")
            set.append(self.data[i][1]/(self.data[i][2]*self.data[i][3]))
            self.series.append(set)
        # print(self.series)
        self.chart = QtChart.QChart()
        self.chart.setTitle("Koef = bugs / (employees * days)")
        self.chart.addSeries(self.series)
        self.chart.setAnimationOptions(QtChart.QChart.SeriesAnimations)
        # chart.setAnimationOptions(QtChart.QChart.SeriesAnimations)
        projects = []
        for i in range(len(self.data)):
            projects.append(self.data[i][0])
        self.chartView = QChartView(self.chart)
        self.ui.diagram.setChart(self.chart)

    def updateFiringTablesHandler(self):
        self.tableModelDevelopers.update_info()
        self.ui.tableDevelopers.update()
        self.tableModelTesters.update_info()
        self.ui.tableTesters.update()

    def connectActionsToTabQueries(self):
        self.ui.btnAddEmployee.clicked.connect(self.addEmployeeHandler)
        self.ui.btnAddProject.clicked.connect(self.startProjectHandler)
        self.ui.btnEndProject_2.clicked.connect(self.endProjectHandler)

    def emptyNameFieldHandler(self, name_of_field):
        if name_of_field == '':
            self.errorMessage.setText("Error :Empty field of name\r")
            self.errorMessage.setInformativeText("Try to enter the name of company")
            self.errorMessage.setStandardButtons(self.errorMessage.Ok or self.errorMessage.Cancel)
            self.errorMessage.setDefaultButton(self.errorMessage.Ok)
            self.errorMessage.exec()
            return 1
        else:
            return 0

    def addEmployeeHandler(self):
        if not (self.emptyNameFieldHandler(self.ui.addName.text())):
            if self.ui.jobBox.currentText() == "tester":
                MyDbRequests.addTester(self.ui.addName.text(), self.ui.projectBox.currentText())
                self.tableModel.update_info(self.ui.addName.text(), self.ui.jobBox.currentText(),
                                            self.ui.projectBox.currentText())
            else:
                MyDbRequests.addDeveloper(self.ui.addName.text(), self.ui.projectBox.currentText())
                self.tableModel.update_info(self.ui.addName.text(), self.ui.jobBox.currentText(),
                                            self.ui.projectBox.currentText())
            self.ui.addName.clear()
            self.ui.tableEmployees.update()

    def startProjectHandler(self):
        if not (self.emptyNameFieldHandler(self.ui.addProjectName.text())):
            MyDbRequests.startProject(self.ui.addProjectName.text(), self.ui.date.date().toString())
            self.ui.addProjectName.clear()

    def endProjectHandler(self):
        if not (self.emptyNameFieldHandler(self.ui.endProjectName.text())):
            MyDbRequests.endProject(self.ui.endProjectName.text(), self.ui.date.date().toString())
            self.ui.endProjectName.clear()
            self.tableModelProjectsToEnd.update_info()
            self.ui.tableProjectsToEnd.update()

    def switchPageHandler(self):
        self.ui.frameQueriesPages.setCurrentWidget(self.ui.recruitPage)
        self.ui.projectBox.clear()
        self.ui.projectBox.addItems(MyDbRequests.getCurrentProjects())

    # def connectActionsToTabReports(self):

    def switchReportsHandler(self):
        self.ui.reportPages.setCurrentWidget(self.ui.reportCurrentProjects)
        self.ui.projectBox.clear()
        self.ui.projectBox.addItems(MyDbRequests.getAllProjects())
        self.tableModelCurrentProjects.update_info()
        self.ui.tableCurrentProjects.update()

    def comboBoxTransferingHandler(self):
        self.ui.comboBoxProejctFrom.clear()
        self.ui.comboBoxProejctFrom.addItems(
            MyDbRequests.getProjectsWhereEmployeeWork(self.ui.comboBoxEmployee.currentText()))
        self.ui.comboBoxProjectTo.clear()
        self.ui.comboBoxProjectTo.addItems(
            MyDbRequests.getProjectsWhereEmployeeCanTransfer(self.ui.comboBoxEmployee.currentText()))
        self.ui.comboBoxProjectsWhereToAdd.clear()
        self.ui.comboBoxProjectsWhereToAdd.addItems(
            MyDbRequests.getProjectsWhereEmployeeCanTransfer(self.ui.comboBoxEmployee.currentText()))

    def switchTransferPageHandler(self):
        self.ui.frameQueriesPages.setCurrentWidget(self.ui.transferPage)
        self.ui.comboBoxEmployee.clear()
        self.ui.comboBoxEmployee.addItems(MyDbRequests.getAllEmployees())

    def switchListOfStaffHandler(self):
        self.ui.reportPages.setCurrentWidget(self.ui.reportListOfStaff)
        self.tableModelListOfStaff.update_info()
        self.ui.tableListOfStaff.update()

    def switchToEndingPageHandler(self):
        self.ui.frameQueriesPages.setCurrentWidget(self.ui.endProjectPage)
        self.tableModelProjectsToEnd.update_info()
        self.ui.tableProjectsToEnd.update()

    def btnTransferEmployeeHandler(self):
        MyDbRequests.transferEmployee(self.ui.comboBoxEmployee.currentText(), self.ui.comboBoxProejctFrom.currentText(),
                                      self.ui.comboBoxProjectTo.currentText())
        self.comboBoxTransferingHandler()

    def switchFiringPageHadler(self):
        self.ui.frameQueriesPages.setCurrentWidget(self.ui.firePage)
        self.tableModelDevelopers.update_info()
        self.ui.tableDevelopers.update()
        self.tableModelTesters.update_info()
        self.ui.tableTesters.update()

    def btnFireHandler(self):
        MyDbRequests.fireEmployee(5, 5)
        self.tableModelDevelopers.update_info()
        self.ui.tableDevelopers.update()
        self.tableModelTesters.update_info()
        self.ui.tableTesters.update()

from sqlalchemy import sql, create_engine
from random import choice
from PyQt5.QtWidgets import QMessageBox


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MyDbRequests(metaclass=SingletonMeta):
    SERVER = create_engine("postgresql://yevs:12345@127.0.0.1:5432/postgres", echo=True)

    def __init__(self):
        self.SERVER.connect()

    bugs = ["Functional error", "Performance defect",
            "Usability defect", "Compatibility defect",
            "Security defect", "Syntax error", "Logic error",
            "Unit-level bug", "Code Duplication", "Data Type Mismatch "]

    @staticmethod
    def __separate_table(input_data) -> list[list]:
        data = []
        for row in input_data:
            data.append(list(map(lambda x: x.strip().replace("\'", ""), str(row)[1:-1].split(","))))
        return data

    @staticmethod
    def __addEmployee(name, projectName):
        msgBox = QMessageBox()

        projectName = f'{projectName}'
        query1 = sql.text(f"INSERT INTO employees(employee_name,status) VALUES('{name}','working')\n")
        query_res1 = MyDbRequests.SERVER.execute(query1)
        query2 = sql.text("INSERT INTO employees_project(employee_id,project_1_id)\n"
                          f"SELECT employee_id,{MyDbRequests.convertProjectNameToProjectId(projectName)} FROM employees e\n"
                          "ORDER BY employee_id DESC \n"
                          "LIMIT 1\n")
        query_res2 = MyDbRequests.SERVER.execute(query2)
        query3 = sql.text("UPDATE projects set number_of_employees = number_of_employees + 1"
                          f"WHERE project_id = {MyDbRequests.convertProjectNameToProjectId(projectName)}")
        MyDbRequests.SERVER.execute(query3)

    @staticmethod
    def addTester(name, projectName):
        MyDbRequests.__addEmployee(name, projectName)
        query = sql.text("INSERT INTO testers(employee_id)\n"
                         "SELECT employee_id FROM employees e\n"
                         "ORDER BY employee_id DESC \n"
                         "LIMIT 1")
        query_res = MyDbRequests.SERVER.execute(query)

    @staticmethod
    def addDeveloper(name, projectName):
        MyDbRequests.__addEmployee(name, projectName)
        query = sql.text("INSERT INTO developers(employee_id)\n"
                         "SELECT employee_id FROM employees e\n"
                         "ORDER BY employee_id DESC \n"
                         "LIMIT 1")
        query_res = MyDbRequests.SERVER.execute(query)

    @staticmethod
    def startProject(projectName, date_of_start):
        query = sql.text("INSERT INTO projects(project_name,date_of_start,number_of_employees) \n"
                         f"VALUES ('{projectName}','{date_of_start}', 0)\n")
        query_res = MyDbRequests.SERVER.execute(query)

    @staticmethod
    def endProject(endProjectName, date_of_end):
        query = sql.text("UPDATE projects\n"
                         f"SET date_of_finish = '{date_of_end}'\n"
                         f"WHERE project_name LIKE '{endProjectName}'")
        query_res = MyDbRequests.SERVER.execute(query)

    @staticmethod
    def getListOfEmployees():
        query = sql.text("SELECT employee_name FROM employees\n"
                         "ORDER BY employee_name")
        qeury_res = MyDbRequests.SERVER.execute(query)
        return [row[0] for row in qeury_res]

    @staticmethod
    def getAllProjects():
        query = sql.text("SELECT project_name FROM projects\n"
                         "ORDER BY project_name")
        qeury_res = MyDbRequests.SERVER.execute(query)
        return [list(row)[0] for row in qeury_res]

    @staticmethod
    def getCurrentProjects():
        query = sql.text("SELECT project_name FROM projects\n"
                         "WHERE date_of_finish IS NULL\n"
                         "ORDER BY project_name")
        qeury_res = MyDbRequests.SERVER.execute(query)
        return [list(row)[0] for row in qeury_res]

    @staticmethod
    def convertProjectNameToProjectId(name):
        query = sql.text("SELECT project_id \n"
                         "FROM projects p\n"
                         f"WHERE project_name = '{name}'")
        id = MyDbRequests.SERVER.execute(query)
        return list(id)[0][0]

    @staticmethod
    def reportCurrentProjects():
        query = sql.text("SELECT project_name,employee_name,e.employee_id FROM projects\n"
                         "JOIN employees_project ON projects.project_id = employees_project.project_1_id OR "
                         "projects.project_id = employees_project.project_2_id\n "
                         "JOIN employees e ON employees_project.employee_id = e.employee_id\n"
                         "WHERE date_of_finish IS NULL\n"
                         "ORDER BY project_name\n")
        query_res = MyDbRequests.SERVER.execute(query)
        data = list(query_res)
        return data

    @staticmethod
    def getAllEmployees():
        query = sql.text("SELECT employee_name FROM employees")
        query_res = MyDbRequests.SERVER.execute(query)
        return [list(row)[0] for row in query_res]

    @staticmethod
    def getProjectsWhereEmployeeWork(name):
        query = sql.text("SELECT project_name FROM  projects p\n"
                         "JOIN employees_project ep ON p.project_id = ep.project_1_id OR p.project_id = ep.project_2_id \n"
                         "JOIN employees e ON e.employee_id  = ep.employee_id\n "
                         f"WHERE e.employee_name = '{name}' AND date_of_finish is NULL")
        query_res = MyDbRequests.SERVER.execute(query)
        return [list(row)[0] for row in query_res]

    @staticmethod
    def getProjectsWhereEmployeeCanTransfer(name):
        query = sql.text(" SELECT project_name FROM projects p\n"
                         "  WHERE date_of_finish is null")
        query_res = MyDbRequests.SERVER.execute(query)
        query2 = sql.text("SELECT project_name FROM  projects p\n"
                          "JOIN employees_project ep ON p.project_id = ep.project_1_id OR p.project_id = ep.project_2_id \n"
                          "JOIN employees e ON e.employee_id  = ep.employee_id\n "
                          f"WHERE e.employee_name = '{name}'")
        query_res2 = MyDbRequests.SERVER.execute(query2)
        data = [str(row[0]) for row in query_res]
        query_res2 = [str(row[0]) for row in query_res2]
        data = set(data) - set(query_res2)
        return list(data)

    @staticmethod
    def reportListOfStaff():
        query = sql.text("SELECT employee_name, project_name, date_of_start, date_of_finish FROM "
                         "employees e\n "
                         "JOIN employees_project ep ON e.employee_id = ep.employee_id \n"
                         "JOIN projects p ON ep.project_1_id = p.project_id OR ep.project_2_id = p.project_id\n"
                         "ORDER BY date_of_start")

        query_res = MyDbRequests.SERVER.execute(query)
        data = list(query_res)
        return [[str(el) for el in row] for row in data]

    @staticmethod
    def tableProjectsToEnd():
        query = sql.text("SELECT project_name from projects\n"
                         "WHERE date_of_finish is NULL")

        query_res = MyDbRequests.SERVER.execute(query)
        return [row[0] for row in query_res]

    @staticmethod
    def transferEmployee(employeeName, projectNameFrom, projectNameTo):
        query1 = sql.text("SELECT project_1_id, project_2_id FROM employees_project ep\n"
                          "JOIN employees e ON e.employee_id = ep.employee_id\n"
                          f"WHERE employee_name = '{employeeName}'")
        employee_projects = MyDbRequests.SERVER.execute(query1)
        data = list(employee_projects)

        query1 = sql.text("UPDATE employees_project SET project_1_id = (SELECT projects.project_id\n"
                          f"FROM projects WHERE project_name = '{projectNameTo}' LIMIT 1)\n"
                          "WHERE project_1_id = (SELECT projects.project_id\n"
                          f"FROM projects WHERE project_name = '{projectNameFrom}' LIMIT 1)\n"
                          "AND employee_id = (SELECT employee_id FROM employees\n"
                          f"WHERE employee_name = '{employeeName}')")
        MyDbRequests.SERVER.execute(query1)

        query2 = sql.text("UPDATE employees_project SET project_2_id = (SELECT projects.project_id\n"
                          f"FROM projects WHERE project_name = '{projectNameTo}' LIMIT 1)\n"
                          "WHERE project_2_id = (SELECT projects.project_id\n"
                          f"FROM projects WHERE project_name = '{projectNameFrom}' LIMIT 1)\n"
                          "AND employee_id = (SELECT employee_id FROM employees\n"
                          f"WHERE employee_name = '{employeeName}')")
        MyDbRequests.SERVER.execute(query2)

    @staticmethod
    def addEmployeeToProject(employeeName, projectName):
        msgBox = QMessageBox()
        query1 = sql.text("SELECT project_1_id, project_2_id FROM employees_project ep\n"
                          "JOIN employees e ON e.employee_id = ep.employee_id\n"
                          f"WHERE employee_name = '{employeeName}'")
        employee_projects = MyDbRequests.SERVER.execute(query1)
        data = list(employee_projects)
        if data == []:
            id = 1
            query2 = sql.text(
                f"INSERT INTO employees_project(project_{id}_id) VALUES( {MyDbRequests.convertProjectNameToProjectId(projectName)})")
            MyDbRequests.SERVER.execute(query2)

        elif data[0][0] is None:
            id = 1
            query2 = sql.text(
                f"UPDATE employees_project SET project_{id}_id = {MyDbRequests.convertProjectNameToProjectId(projectName)}")
            MyDbRequests.SERVER.execute(query2)
        elif data[0][1] is None:
            id = 2
            query2 = sql.text(
                f"UPDATE employees_project SET project_{id}_id = {MyDbRequests.convertProjectNameToProjectId(projectName)}")
            MyDbRequests.SERVER.execute(query2)
        else:
            msgBox.setText("Error: Employee is already in 2 projects\r")
            msgBox.setStandardButtons(msgBox.Ok or msgBox.Cancel)
            msgBox.setDefaultButton(msgBox.Ok)
            msgBox.exec()

    @staticmethod
    def getDevelopersForTable():
        query = sql.text("SELECT employee_name, number_of_bugs FROM developers d\n"
                         "JOIN employees e ON e.employee_id = d.employee_id\n"
                         "JOIN employees_project ep on ep.employee_id = e.employee_id\n"
                         "JOIN projects p ON p.project_id = ep.project_1_id OR p.project_id = ep.project_2_id\n"
                         "WHERE status = 'working' and p.date_of_finish is NULL")
        query_res = MyDbRequests.SERVER.execute(query)
        data = list(query_res)
        return [[str(el) for el in row] for row in data]

    @staticmethod
    def getTestersForTable():
        query = sql.text("SELECT employee_name, fixed_bugs_number FROM testers t\n"
                         "JOIN employees e ON e.employee_id = t.employee_id\n"
                         "JOIN employees_project ep on ep.employee_id = e.employee_id\n"
                         "JOIN projects p ON p.project_id = ep.project_1_id OR p.project_id = ep.project_2_id\n"
                         "WHERE status = 'working' and  p.date_of_finish is NULL")
        query_res = MyDbRequests.SERVER.execute(query)
        data = list(query_res)
        return [[str(el) for el in row] for row in data]

    @staticmethod
    def fireEmployee(number_of_bugs, fixed_bugs):
        query = sql.text("UPDATE employees SET status ='dismissed'\n"
                         "WHERE employee_id IN (SELECT e.employee_id FROM employees e\n"
                         "JOIN developers d ON d.employee_id = e.employee_id\n "
                         f"           WHERE d.number_of_bugs > {number_of_bugs})")
        query2 = sql.text("UPDATE employees SET status ='dismissed'\n"
                          "WHERE employee_id IN (SELECT e.employee_id FROM employees e\n"
                          "JOIN testers t ON t.employee_id = e.employee_id \n"
                          f"WHERE t.fixed_bugs_number < {fixed_bugs})")
        MyDbRequests.SERVER.execute(query)
        MyDbRequests.SERVER.execute(query2)

    @staticmethod
    def getRandomBug(current_date, deadline):
        query = sql.text("INSERT INTO bugs(categorie,time_bug_found,fix_deadline , developer_id , project_id)\n"
                         f"SELECT bt,'{current_date}','{current_date}',developer_id ,project_id FROM rnd_bug")

        MyDbRequests.SERVER.execute(query)
        query5 = sql.text("UPDATE developers d2 SET number_of_bugs = number_of_bugs + 1\n"
                          "WHERE d2.developer_id = (\n"
                          "SELECT developer_id FROM bugs b\n"
                          "ORDER BY bug_id DESC\n"
                          "LIMIT 1\n"
                          ")")

        MyDbRequests.SERVER.execute(query5)

        query2 = sql.text("UPDATE bugs SET\n"
                          "tester_found_id = (\n"
                          "SELECT tester_id FROM testers AS t\n"
                          "JOIN employees AS e ON e.employee_id = t.employee_id \n"
                          "JOIN employees_project AS ep ON ep.employee_id = e.employee_id\n"
                          "JOIN projects AS p ON p.project_id  = ep.project_1_id  OR p.project_id  = ep.project_2_id\n"
                          "WHERE bugs.project_id = ep.project_1_id  OR bugs.project_id  = ep.project_2_id\n"
                          "ORDER BY random() LIMIT 1\n"
                          ")")
        MyDbRequests.SERVER.execute(query2)
        query3 = sql.text("UPDATE bugs SET \n"
                          "tester_fix_id = (\n"
                          "SELECT tester_id FROM testers AS t \n"
                          "JOIN employees AS e ON e.employee_id = t.employee_id \n"
                          "JOIN employees_project AS ep ON ep.employee_id = e.employee_id\n"
                          "JOIN projects AS p ON p.project_id  = ep.project_1_id  OR p.project_id  = ep.project_2_id \n"
                          "	WHERE (bugs.project_id = ep.project_1_id  OR bugs.project_id  = ep.project_2_id) AND tester_id != bugs.tester_found_id \n"
                          "ORDER BY random() LIMIT 1 \n"
                          ")")
        MyDbRequests.SERVER.execute(query3)

    @staticmethod
    def randFix():
        query = sql.text(" UPDATE bugs SET fix_status = TRUE\n"
                         "WHERE tester_fix_id = (\n"
                         "SELECT tester_fix_id FROM bugs\n"
                         "ORDER BY random()\n"
                         "LIMIT 1\n"
                         ")\n"
                         "AND fix_status = FALSE")

        # query2 = sql.text("UPDATE developers d2 SET number_of_bugs = number_of_bugs - 1\n"
        #                   "WHERE d2.developer_id = (SELECT developer_id FROM bugs b ORDER BY bug_id DESC LIMIT 1)")

        query3 = sql.text("UPDATE testers t2 SET fixed_bugs_number = fixed_bugs_number + 1 \n"
                          "WHERE t2.tester_id = (SELECT tester_fix_id FROM bugs b ORDER BY bug_id DESC LIMIT 1)")

        MyDbRequests.SERVER.execute(query)
        # MyDbRequests.SERVER.execute(query2)
        MyDbRequests.SERVER.execute(query3)

    @staticmethod
    def getInfoForDiagram():
        query = sql.text("SELECT DISTINCT  project_name,\n"
                         "(SELECT count(*) AS number_of_bugs FROM bugs \n"
                         "WHERE project_id = p.project_id\n"
                         "),\n"
                         "number_of_employees,\n"
                         "(date_of_finish - date_of_start) AS hours\n"
                         "FROM projects p \n"
                         "	JOIN bugs b ON b.project_id = p .project_id\n"
                         "WHERE p.date_of_finish IS NOT NULL")
        return list(MyDbRequests.SERVER.execute(query))

MyDbRequests()
print(MyDbRequests.getInfoForDiagram())
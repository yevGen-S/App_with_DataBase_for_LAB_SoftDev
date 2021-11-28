from typing import Any

from PyQt5.QtCore import Qt, QAbstractTableModel
from sqlalchemy import sql, create_engine


class EmployeeTableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self._data = []
        self._table_titles = ["Employee name", "Job type", "Project"]

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self._table_titles[section]

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            return self._data[index.row()][index.column()]
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._table_titles)

    def update_info(self, name, type, project_name):
        self.beginResetModel()
        self._data.append([name, type, project_name])
        self.endResetModel()
"""
Copyright (C) 10-04-2022 Vera Pliushchikova
email: plyushchikova.v.s@gmail.com
https://github.com/VeraPl
The program is built on Python 3.9.5 and PyQt5. The icon was taken from open sources - https://www.flaticon.com

This code create QTableView (10x10) and calculate multiplication.
Users can choose  which cells to fill with color by combobox - Even, odd or prime numbers.

"""

import sys
from PyQt5.QtCore import Qt, QVariant, QAbstractItemModel, QModelIndex
from PyQt5.QtWidgets import QTableView, QApplication, QMainWindow
from PyQt5.QtGui import QColor
from PyQt5 import uic


class Model(QAbstractItemModel):
    def __init__(self, parent=None, condition="-"):
        super(Model, self).__init__(parent)
        self.fill_condition = condition
        size_num = range(1, 11)
        self.items = []
        for i in size_num:
            self.items.append([str(i * j) for j in size_num])

    def index(self, row, column, parent=QModelIndex()):
        return self.createIndex(row, column, None)

    def parent(self, child):
        return QModelIndex()

    def rowCount(self, parent=QModelIndex()):
        return len(self.items)

    def columnCount(self, parent=QModelIndex()):
        if self.items:
            return max([len(item) for item in self.items])
        return 0

    def data(self, index=None, role=None):
        row = index.row()
        col = index.column()
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self.items[index.row()][index.column()]
        if role == Qt.BackgroundColorRole:
            if self.fill_condition == "Odd":
                if not index.row() % 2 and not col % 2:
                    fill_color = QColor(161, 189, 217)
                else:
                    fill_color = QColor(247, 248, 242)
            elif self.fill_condition == "Even":
                if index.row() % 2 or col % 2:
                    fill_color = QColor(161, 189, 217)
                else:
                    fill_color = QColor(247, 248, 242)
            elif self.fill_condition == "Prime":
                prime_num = ([0, 1], [0, 2], [0, 4], [0, 6], [1, 0], [2, 0], [4, 0], [6, 0])
                if [row, col] in prime_num:
                    fill_color = QColor(161, 189, 217)
                else:
                    fill_color = QColor(247, 248, 242)
            else:
                fill_color = QColor(247, 248, 242)
            return QVariant(QColor(fill_color))
        elif role == Qt.TextAlignmentRole:
            return QVariant(int(Qt.AlignHCenter | Qt.AlignVCenter))


class Multiplicationtable(QMainWindow):
    def __init__(self, parent=None):
        super(Multiplicationtable, self).__init__(parent)
        Form, Base = uic.loadUiType('MultiplicationTable.ui')
        self.ui = Form()
        self.ui.setupUi(self)
        self.setWindowTitle("Multiplication table")

        self.model = Model()
        self.ui.Table.setModel(self.model)
        self.ui.Table.resizeColumnsToContents()

        self.ui.comboBox.currentIndexChanged.connect(self.fill_cells)

    def fill_cells(self):
        self.model = Model(condition=self.ui.comboBox.currentText())
        self.ui.Table.setModel(self.model)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Multiplicationtable()
    window.show()
    app.exec_()

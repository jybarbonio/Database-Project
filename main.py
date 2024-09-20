from openpyxl import load_workbook


import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = QtWidgets.QTableView()

        filename = 'Car Price List.xlsx'

        data = pyxl_load_workbook(filename)

        self.model = TableModel(data)
        self.table.setModel(self.model)

        self.setCentralWidget(self.table)

def pyxl_load_workbook(f):
    # wb = 'workbook'
    wb = load_workbook(filename = f, keep_vba=True, rich_text=True)
    row = wb['Sheet1']

    #ws = 'worksheet'
    ws = wb.active

    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToHeight = False

    arr = []

    for row in ws.iter_rows():
        arr_row = []    
        for cell in row:
            print(cell.value)
            arr_row.append(cell.value)

        arr.append(arr_row)

    return arr
    
app=QtWidgets.QApplication(sys.argv)
window=MainWindow()

window.show()
app.exec()

import sys
import sudoku_model
from PyQt5.QtWidgets import *



def intialize_graphics(sudoku_grid):
    monApp=QApplication(sys.argv)
    w=SudokuGridWidget(sudoku_grid)	
    w.resize(500,300)
    w.move(500, 500)
    w.setWindowTitle("Main sudoku")   
    w.show()
    sys.exit(monApp.exec_())

class SudokuGridWidget(QWidget):
    def __init__(self, sudoku_grid):
        QWidget.__init__(self)
        layout = QGridLayout()
        for i in range(3):
            for j in range(3):
                layout.addWidget(BoxWidget(i, j, sudoku_grid),i,j)	
        self.setLayout(layout)
        self.setStyleSheet("margin:10px; border:10px solid rgb(0, 0, 0); ")

class BoxWidget(QWidget):
    def __init__(self, i_box, j_box, sudoku):
        QWidget.__init__(self)
        layout = QGridLayout()
        for i in range(3):
            for j in range(3):
                index = j_box * 3 + i_box * 27 + i*9 + j + 1
                layout.addWidget(CellWidget(index, sudoku.cell_list[index-1]), i, j)	
        self.setLayout(layout)
        self.setStyleSheet("margin:5px; border:5px solid rgb(0, 0, 0); ")

class CellWidget(QLabel):
    def __init__(self, index, cell):
        QLabel.__init__(self, str(index))
        self.setFixedSize(60, 60)
        self.cell = cell
        self.index = index
        self.setStyleSheet("margin:1px; border:1px solid black; padding:5px; text-align:center")

    def set_value(self, mode):
        if mode == "value":
            self.setText(self.cell.to_value_str())
        else:
            self.setText(self.cell.to_possible_str())

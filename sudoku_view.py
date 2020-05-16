
import sys
import sudoku_model
from PyQt5.QtWidgets import *


def intialize_graphics(sudoku_grid):
    my_app = QApplication(sys.argv)
    my_main = LazySudokuMainWindow(sudoku_grid)
   
    my_main.show()
    my_app.exec_()

class LazySudokuMainWindow(QMainWindow):
    def __init__(self,sudoku_grid):
        QMainWindow.__init__(self)
        self.setWindowTitle("Lazy_sudoku")  
    
        sudoku_widget = SudokuGridWidget(sudoku_grid)
        sudoku_widget.resize(500, 300)
        sudoku_widget.move(500, 500)
        
        mode_button = ViewModeButton()
        print(type(sudoku_widget))
        mode_button.clicked.connect(lambda: mode_button.on_click(sudoku_widget))
        
        layout = QVBoxLayout()
        layout.addWidget(sudoku_widget)
        layout.addWidget(mode_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

class SudokuGridWidget(QWidget):
    def __init__(self, sudoku_grid):
        QWidget.__init__(self)
        layout = QGridLayout()
        for i in range(3):
            for j in range(3):
                layout.addWidget(BoxWidget(i, j, sudoku_grid),i,j)	
        self.setLayout(layout)
        self.setStyleSheet("margin:10px; border:10px solid rgb(0, 0, 0); ")

    def update_cells(self, mode):
        for box in self.children():
            for cell_widget in box.children():
                if isinstance(cell_widget, CellWidget):
                    cell_widget.set_value(mode)

class BoxWidget(QWidget):
    def __init__(self, i_box, j_box, sudoku):
        QWidget.__init__(self)
        layout = QGridLayout()
        for i in range(3):
            for j in range(3):
                index = j_box * 3 + i_box * 27 + i*9 + j + 1
                layout.addWidget(CellWidget(sudoku.cell_list[index-1]), i, j)	
        self.setLayout(layout)
        self.setStyleSheet("margin:5px; border:5px solid rgb(0, 0, 0); ")

class CellWidget(QLabel):

    @staticmethod
    def _coloration(dict):
        print(dict)
        for key, val in dict.items():
            tempo_list = "<font color="+ val + ">" + key +"</font>"
        if len(dict) == 1:
            to_return = "<font color="+ val + ">" + key +"</font>"
        else:
            to_return = ""
            for digit in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                if digit in dict:
                    to_return += "<font color="+ dict[digit] + ">" + digit +"</font>"
                else:
                    to_return += "_"
                if digit in ["3", "6"]:
                    to_return += "<br>"
                else:
                    to_return += " "
        return to_return

    def __init__(self, cell):
        QLabel.__init__(self, CellWidget._coloration(cell.to_value_str()))
        self.setFixedSize(60, 60)
        self.cell = cell
        self.setStyleSheet("margin:1px; border:1px solid black; padding:5px; text-align:center")

    def set_value(self, mode):
        if mode == "value":
            self.setText(CellWidget._coloration(self.cell.to_value_str()))
        else:
            self.setText(CellWidget._coloration(self.cell.to_possible_str()))

class ViewModeButton(QPushButton):
    def __init__(self):
        QPushButton.__init__(self)
        self.value_mode = "possible"
        self.setText(self.value_mode)

    def on_click(self, sudoku_grid):
        sudoku_grid.update_cells(self.value_mode)
        self.value_mode = "possible" if self.value_mode == "value" else "value"
        self.setText(self.value_mode)
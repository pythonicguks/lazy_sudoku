import sys

from PyQt5 import QtWidgets as qtw

CELL_SIZE = 60
WINDOW_SIZE = (500, 300)
WINDOW_POSITION = (500, 500)

DIGIT_ORDER = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
DIGITS_PER_LINE = 3


def initialize_graphics(sudoku_grid):
    my_app = qtw.QApplication(sys.argv)
    my_main = LazySudokuMainWindow(sudoku_grid)

    my_main.show()
    my_app.exec_()


class LazySudokuMainWindow(qtw.QMainWindow):
    def __init__(self, sudoku_grid):
        qtw.QMainWindow.__init__(self)
        self.setWindowTitle("Lazy_sudoku")

        sudoku_widget = SudokuGridWidget(sudoku_grid)
        sudoku_widget.resize(*WINDOW_SIZE)
        sudoku_widget.move(*WINDOW_POSITION)

        mode_button = ViewModeButton()
        mode_button.clicked.connect(lambda: mode_button.on_click(sudoku_widget))

        layout = qtw.QVBoxLayout()
        layout.addWidget(sudoku_widget)
        layout.addWidget(mode_button)

        central_widget = qtw.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


class SudokuGridWidget(qtw.QWidget):
    def __init__(self, sudoku_grid):
        qtw.QWidget.__init__(self)
        layout = qtw.QGridLayout()
        self.cell_widgets = []
        for i in range(3):
            for j in range(3):
                box = BoxWidget(i, j, sudoku_grid)
                self.cell_widgets.extend(box.cell_widgets)
                layout.addWidget(box, i, j)
        self.setLayout(layout)
        self.setStyleSheet("margin:10px; border:10px solid rgb(0, 0, 0); ")

    def update_cells(self, mode):
        for cell_widget in self.cell_widgets:
            cell_widget.set_value(mode)


class BoxWidget(qtw.QWidget):
    def __init__(self, i_box, j_box, sudoku_grid):
        qtw.QWidget.__init__(self)
        layout = qtw.QGridLayout()
        box_index = i_box * 3 + j_box + 1
        self.cell_widgets = []
        for position, cell_index in enumerate(sudoku_grid.get_box(box_index)):
            cell_widget = CellWidget(sudoku_grid.cell_list[cell_index])
            self.cell_widgets.append(cell_widget)
            layout.addWidget(cell_widget, position // 3, position % 3)
        self.setLayout(layout)
        self.setStyleSheet("margin:5px; border:5px solid rgb(0, 0, 0); ")


class CellWidget(qtw.QLabel):

    @staticmethod
    def _coloration(dico):
        if len(dico) == 1:
            for key, val in dico.items():
                to_return = "<font color=" + val + ">" + key + "</font>"
        else:
            to_return = ""
            for digit in DIGIT_ORDER:
                if digit in dico and dico[digit] is not None:
                    to_return += "<font color=" + dico[digit] + ">" + digit + "</font>"
                else:
                    to_return += "_"
                if digit in ("3", "6"):
                    to_return += "<br>"
                else:
                    to_return += " "
        return to_return

    def __init__(self, cell):
        qtw.QLabel.__init__(self, CellWidget._coloration(cell.to_value_str()))
        self.setFixedSize(CELL_SIZE, CELL_SIZE)
        self.cell = cell
        self.setStyleSheet("margin:1px; border:1px solid black; padding:5px; text-align:center")

    def set_value(self, mode):
        if mode == "value":
            self.setText(CellWidget._coloration(self.cell.to_value_str()))
        else:
            self.setText(CellWidget._coloration(self.cell.to_possible_str()))


class ViewModeButton(qtw.QPushButton):
    def __init__(self):
        qtw.QPushButton.__init__(self)
        self.value_mode = "possible"
        self.setText(self.value_mode)

    def on_click(self, sudoku_grid_widget):
        sudoku_grid_widget.update_cells(self.value_mode)
        self.value_mode = "possible" if self.value_mode == "value" else "value"
        self.setText(self.value_mode)

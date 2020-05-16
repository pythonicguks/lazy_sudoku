import sudoku_view
import sudoku_model


def lazy_sudoku(sudoku_list=None, params=None, debug=False):
    new_grid = sudoku_model.SudokuGrid(sudoku_list, mode_debug=debug)
    sudoku_view.intialize_graphics(new_grid)

if __name__ == "__main__":
    lazy_sudoku()

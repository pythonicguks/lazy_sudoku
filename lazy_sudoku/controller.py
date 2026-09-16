from lazy_sudoku import model, view


def lazy_sudoku(sudoku_list=None, params=None, debug=False):
    new_grid = model.SudokuGrid(sudoku_list, mode_debug=debug)
    view.initialize_graphics(new_grid)

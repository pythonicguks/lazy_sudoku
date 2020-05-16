import sudoku_controller

def index_test():
    """
    """
    sudoku_grid = [nb + 1 for nb in range(81)]
    sudoku_controller.lazy_sudoku(sudoku_grid, None , True)

def empty_grid():
    sudoku_grid = [0 for _ in range(81)]
    sudoku_controller.lazy_sudoku(sudoku_grid)

def custom_grid():
    sudoku_grid = [0, 0, 0,    2, 0, 0,     0, 0, 3,
                   0, 1, 0,    0, 0, 0,     0, 3, 0,
                   0, 0, 0,    0, 0, 2,     3, 0, 0,
                   
                   4, 0, 4,    5, 0, 5,     6, 0, 6,
                   0, 0, 0,    0, 5, 0,     6, 0, 6,
                   4, 0, 4,    5, 0, 5,     6, 0, 6,
                   
                   7, 7, 7,    8, 8, 8,     9, 9, 9,
                   0, 7, 0,    8, 0, 8,     9, 9, 9,
                   7, 7, 7,    8, 8, 8,     9, 9, 9]
    sudoku_controller.lazy_sudoku(sudoku_grid)

if __name__ == "__main__":
    custom_grid()
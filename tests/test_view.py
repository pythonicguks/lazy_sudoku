import pytest
from PyQt5 import QtWidgets as qtw

from lazy_sudoku.model import SudokuGrid
from lazy_sudoku.view import CellWidget, LazySudokuMainWindow, SudokuGridWidget


@pytest.fixture(scope="session")
def qapp():
    app = qtw.QApplication.instance() or qtw.QApplication([])
    yield app


def test_sudoku_grid_widget_creates_all_81_cells(qapp):
    grid = SudokuGrid()
    widget = SudokuGridWidget(grid)
    assert len(widget.cell_widgets) == 81
    # each model cell must be represented by exactly one CellWidget (boxes are
    # built independently of line order, so compare as sets, not sequences)
    assert {id(w.cell) for w in widget.cell_widgets} == {id(c) for c in grid.cell_list}


def test_update_cells_switches_display_mode(qapp):
    sudoku_list = [0] * 81
    sudoku_list[0] = 5
    grid = SudokuGrid(sudoku_list)
    widget = SudokuGridWidget(grid)

    widget.update_cells("possible")
    filled_cell_widget = widget.cell_widgets[0]
    assert "5" in filled_cell_widget.text()

    # a neighbouring empty cell should render the reduced possible values,
    # not crash on a color of None (regression test for the coloration bug)
    neighbour_widget = widget.cell_widgets[1]
    assert "5" not in neighbour_widget.text()


def test_main_window_builds_without_blocking(qapp):
    grid = SudokuGrid()
    window = LazySudokuMainWindow(grid)
    assert window.windowTitle() == "Lazy_sudoku"


def test_coloration_single_value():
    assert CellWidget._coloration({"5": "black"}) == "<font color=black>5</font>"


def test_coloration_possible_values_with_missing_digits():
    dico = {str(d): ("black" if d != 5 else None) for d in range(1, 10)}
    rendered = CellWidget._coloration(dico)
    assert "_" in rendered  # digit 5 removed from possibilities is rendered as a blank
    assert "<font color=None>" not in rendered

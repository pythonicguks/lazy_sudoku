import pytest

from lazy_sudoku.model import ALL_POSSIBLE_VALUES, SudokuCell, SudokuGrid


def test_default_grid_is_empty():
    grid = SudokuGrid()
    assert len(grid.cell_list) == 81
    assert all(cell.value is None for cell in grid.cell_list)
    assert all(cell.possible_values == ALL_POSSIBLE_VALUES for cell in grid.cell_list)


def test_invalid_cell_list_length_raises():
    with pytest.raises(ValueError):
        SudokuGrid([0] * 80)


def test_out_of_range_value_raises_without_debug():
    sudoku_list = [nb + 1 for nb in range(81)]
    with pytest.raises(ValueError):
        SudokuGrid(sudoku_list, mode_debug=False)


def test_out_of_range_value_allowed_with_debug():
    sudoku_list = [nb + 1 for nb in range(81)]
    grid = SudokuGrid(sudoku_list, mode_debug=True)
    assert [cell.value for cell in grid.cell_list] == sudoku_list


@pytest.mark.parametrize("family,accessor", [
    ("line", SudokuGrid.get_line),
    ("col", SudokuGrid.get_col),
    ("box", SudokuGrid.get_box),
])
def test_families_partition_the_grid(family, accessor):
    grid = SudokuGrid()
    seen = set()
    for index in range(1, 10):
        cells = accessor(grid, index)
        assert len(cells) == 9
        assert len(set(cells)) == 9, f"{family} {index} has duplicate cells"
        assert all(0 <= c <= 80 for c in cells)
        seen.update(cells)
    assert seen == set(range(81)), f"{family} families do not cover the whole grid"


def test_get_box_returns_a_proper_3x3_block():
    grid = SudokuGrid()
    # box 1 = top-left corner
    assert sorted(grid.get_box(1)) == [0, 1, 2, 9, 10, 11, 18, 19, 20]
    # box 5 = center block
    assert sorted(grid.get_box(5)) == [30, 31, 32, 39, 40, 41, 48, 49, 50]
    # box 9 = bottom-right corner
    assert sorted(grid.get_box(9)) == [60, 61, 62, 69, 70, 71, 78, 79, 80]


@pytest.mark.parametrize("family,index", [("line", 0), ("col", 10), ("box", 0)])
def test_family_index_out_of_bounds_raises(family, index):
    grid = SudokuGrid()
    with pytest.raises(ValueError):
        grid._get_cells_from_family_index(family, index)


def test_filling_a_cell_propagates_to_its_line_col_and_box():
    sudoku_list = [0] * 81
    sudoku_list[0] = 5  # top-left cell, index 0 -> line 1, col 1, box 1
    grid = SudokuGrid(sudoku_list)

    for cell_index in grid.get_line(1) + grid.get_col(1) + grid.get_box(1):
        if cell_index == 0:
            continue
        assert 5 not in grid.cell_list[cell_index].possible_values

    # a cell outside line 1, col 1 and box 1 is untouched
    untouched_index = 40
    assert grid.cell_list[untouched_index].possible_values == ALL_POSSIBLE_VALUES


def test_remove_possible_value_resolves_naked_single():
    cell = SudokuCell()
    for value in range(1, 9):
        cell.remove_possible_value(value)
    assert cell.possible_values == [9]
    assert cell.value == 9


def test_remove_possible_value_is_noop_once_cell_has_a_value():
    cell = SudokuCell(3)
    cell.remove_possible_value(3)
    assert cell.value == 3
    assert cell.possible_values is None

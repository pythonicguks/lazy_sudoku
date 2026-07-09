# Lazy Sudoku

A small Sudoku grid model with a PyQt5 viewer.

- `lazy_sudoku/model.py` — `SudokuGrid`/`SudokuCell`: grid state and constraint propagation (removing a value from the possible values of cells sharing a line/column/box).
- `lazy_sudoku/controller.py` — builds a grid and opens the viewer.
- `lazy_sudoku/view.py` — PyQt5 widgets rendering the grid, with a button to toggle between showing the resolved value or the remaining possible values per cell.

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

## Run

```bash
uv run python -m lazy_sudoku
```

Or pass a starting grid (a flat list of 81 ints, `0` for empty cells) from your own script:

```python
from lazy_sudoku.controller import lazy_sudoku

lazy_sudoku([0, 0, 0, 2, 0, 0, 0, 0, 3, ...])
```

## Tests

```bash
uv run pytest
```

Tests run headless (`QT_QPA_PLATFORM=offscreen`, set in `tests/conftest.py`) and never open a blocking window.

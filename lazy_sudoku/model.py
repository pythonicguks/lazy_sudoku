ALL_POSSIBLE_VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9]


class SudokuGrid:
    def __init__(self, cell_list=None, mode_debug=False):
        if cell_list is None:
            self.cell_list = [SudokuCell() for _ in range(81)]
        elif isinstance(cell_list, list) and len(cell_list) == 81:
            self.cell_list = list()
            for cell in cell_list:
                if isinstance(cell, SudokuCell):
                    self.cell_list.append(cell)
                elif mode_debug and isinstance(cell, int):
                    # mode_debug bypasses the 1-9 rule so cells can carry an
                    # arbitrary marker value (e.g. their own index) for
                    # visually checking cell/family indexing, not real solving.
                    self.cell_list.append(SudokuCell(cell))
                elif isinstance(cell, int) and cell in ALL_POSSIBLE_VALUES:
                    self.cell_list.append(SudokuCell(cell))
                elif cell is None or cell == 0:
                    self.cell_list.append(SudokuCell())
                else:
                    raise ValueError(f"Invalid cell value: {cell!r}")
        else:
            raise ValueError("cell_list must be a list of 81 elements or None")

        for cell_index, cell in enumerate(self.cell_list):
            if cell.value is not None:
                self.update_by_new_cell_value(cell_index)

    def update_by_new_cell_value(self, cell_index):
        for family, family_index in self._get_families_indexes(cell_index).items():
            for other_cell_index in self._get_cells_from_family_index(family, family_index):
                if other_cell_index != cell_index:
                    self.cell_list[other_cell_index].remove_possible_value(self.cell_list[cell_index].value)

    def _get_cells_from_family_index(self, family, index):
        if index < 1 or index > 9:
            raise ValueError(f"index must be between 1 and 9, got {index}")
        elif family == "line":
            cell_indexes_list = [i + (index - 1) * 9 for i in range(9)]
        elif family == "col":
            cell_indexes_list = [9 * i + index - 1 for i in range(9)]
        elif family == "box":
            row_box = (index - 1) // 3
            col_box = (index - 1) % 3
            top_left = row_box * 27 + col_box * 3
            cell_indexes_list = [top_left + relatif_pos for relatif_pos in [0, 1, 2, 9, 10, 11, 18, 19, 20]]
        else:
            raise ValueError(f"Unknown family: {family!r}")
        return cell_indexes_list

    def _get_families_indexes(self, cell_index):
        return {"line": cell_index // 9 + 1,
                "col": cell_index % 9 + 1,
                "box": cell_index // 27 * 3 + cell_index % 27 % 9 // 3 + 1}

    def get_line(self, index):
        return self._get_cells_from_family_index("line", index)

    def get_col(self, index):
        return self._get_cells_from_family_index("col", index)

    def get_box(self, index):
        return self._get_cells_from_family_index("box", index)


class SudokuCell:

    def __init__(self, value=None):
        if value is None:
            self.value = None
            self.possible_values = list(ALL_POSSIBLE_VALUES)
        else:
            self.value = value
            self.possible_values = None

    def remove_possible_value(self, val_to_remove):
        if self.value is None:
            self.possible_values = [val for val in self.possible_values if val != val_to_remove]
            if len(self.possible_values) == 1:
                self.value = self.possible_values[0]

    def to_value_str(self):
        if self.possible_values is None:
            to_return = {str(self.value): "black"}
        else:
            if self.value is None:
                to_return = {" ": "blue"}
            else:
                to_return = {str(self.value): "blue"}
        return to_return

    def to_possible_str(self):
        if self.possible_values is None:
            to_return = {str(self.value): "black"}
        else:
            to_return = {str(digit): ("black" if digit in self.possible_values else None) for digit in ALL_POSSIBLE_VALUES}
            if self.value is not None:
                to_return[str(self.value)] = "blue" if self.value in self.possible_values else "red"
        return to_return

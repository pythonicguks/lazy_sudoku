
ALL_POSSIBLE_VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9]

class SudokuGrid:
    def __init__(self, cell_list=None,mode_debug=False):
        if cell_list is None:
            self.cell_list = [SudokuCell() for _ in range(81)]
        elif isinstance(cell_list, list) and len(cell_list) == 81:
            self.cell_list = list()
            for cell in cell_list:
                if isinstance(cell, SudokuCell):
                    self.cell_list.append(cell)
                elif (isinstance(cell, int) and cell in ALL_POSSIBLE_VALUES) or mode_debug:
                    self.cell_list.append(SudokuCell(cell))
                elif cell is None or cell == 0:
                    self.cell_list.append(SudokuCell())
                else:
                    print(cell)
                    assert False
        else:
            assert False
        print(cell_list, type(cell_list), len(cell_list))

    def update_by_new_cell_value(self, cell_index):
        for family, family_index in self._get_families_indexes(cell_index):
            for other_cell_index in self._get_cells_from_family_index(family, family_index):
                if other_cell_index != cell_index:
                    self.cell_list[other_cell_index].remove_possible_value(self.cell_list[cell_index].value)

    def _get_cells_from_family_index(self, family, index):
        if index <= 1 or index > 9:
            raise(ValueError)
        elif family == "line" :
            cell_indexes_list = [i + (index - 1) * 9 for i in range(9)]
        elif family == "col" :
            cell_indexes_list = [9 * i + index - 1 for i in range(9)]
        elif family == "box" :
            offset = (index // 3 - 1) * 27
            cell_indexes_list = [index + offset + relatif_pos - 1 for relatif_pos in [0, 1, 2, 9, 10, 11, 18, 19, 20]]
        else:
            raise(ValueError)
        return cell_indexes_list

    def _get_families_indexes(self, cell_index):
        return({"line": cell_index // 9 + 1,
                "col": cell_index % 9 + 1,
                "box": cell_index // 27 * 3 + cell_index % 27 % 9 // 3 + 1})

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
               to_return[str(self.value)] = "blue" if value in self.possible_values else "red"
        return to_return

class SudokuTechniques:
      def __init__(self, value=None):
          self.value = self.value
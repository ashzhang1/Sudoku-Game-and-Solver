from typing import List

class SudokuCell:

    def __init__(self, curr_value: int, row: int, col: int, is_fixed: bool, possible_values: List[int]):
        self.curr_value = curr_value
        self.row = row
        self.col = col
        self.is_fixed = is_fixed
        self.possible_value = possible_values
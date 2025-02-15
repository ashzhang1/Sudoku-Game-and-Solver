from typing import List, Set, Tuple

class SudokuCell:

    def __init__(self, value: int, row: int, col: int, is_fixed: bool, possible_values: Set[int]):
        self.value = value
        self.row = row
        self.col = col
        self.is_fixed = is_fixed
        self.possible_values = possible_values

    def set_value(self, value: int) -> None:
        self.value = value
    
    def clear_value(self) -> None:
        self.value = None
    
    def is_empty(self) -> bool:
        return self.value == None
    
    def is_fixed(self) -> bool:
        return self.is_fixed == True
    
    def get_row_num(self) -> int:
        return self.row
    
    def get_col_num(self) -> int:
        return self.col
    
    def get_position(self) -> Tuple[int]:
        return (self.row, self.col)
    
    def get_box_num(self) -> int:
        return (self.row // 3) * 3 + (self.col // 3)
    
    # For the possible values - these will be useful for solver
    def get_candidate_values(self) -> Set[int]:
        return self.possible_values

    def add_candidate_value(self, value: int) -> None:
        self.possible_values.add(value)
    
    def remove_candidate_value(self, value: int) -> None:
        self.possible_values.remove(value)
    
    def clear_candidate_values(self) -> None:
        self.possible_values.clear()

    

    



    


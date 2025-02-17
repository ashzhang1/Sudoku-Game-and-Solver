from typing import List
from domain.sudoku_cell import SudokuCell

class SudokuValidator:

    def __init__(self):
        pass

    def is_section_valid(self, section: List[SudokuCell]) -> bool:
        seen = set()
        for cell in section:
            if cell.value is not None:  # Only check non-empty cells
                if cell.value in seen:
                    return False
                seen.add(cell.value)
        return True
    
    def is_move_legal(self, row: List[SudokuCell], col: List[SudokuCell], box: List[SudokuCell]) -> bool:
        return self.is_section_valid(row) and self.is_section_valid(col) and self.is_section_valid(box)

    def is_grid_valid(self, grid: List[List[SudokuCell]]) -> bool:
        num_rows = len(grid)
        num_cols = len(grid[0])

        row_map = {i: set() for i in range(num_rows)}
        col_map = {i: set() for i in range(num_rows)}
        box_map = {i: set() for i in range(num_rows)}

        for row_num in range(num_rows):
            for col_num in range(num_cols):
                cell = grid[row_num][col_num]
                if cell.value is None:
                    continue

                num = cell.value
                box_num = cell.get_box_num()

                # check row
                if num in row_map[row_num]:
                    return False
                row_map[row_num].add(num)

                # check column
                if num in col_map[col_num]:
                    return False
                col_map[col_num].add(num)

                # check box
                if num in box_map[box_num]:
                    return False
                box_map[box_num].add(num)
                
        return True
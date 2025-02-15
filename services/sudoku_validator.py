from typing import List
from domain.sudoku_cell import SudokuCell
from domain.sudoku_board import SudokuBoard

class SudokuValidator:

    def __init__(self):
        pass

    def is_section_valid(self, section: List[SudokuCell]) -> bool:
        seen = set()
        for cell in section:
            if cell.value in seen:
                return False
            seen.add(cell.value)
        return True
    
    def is_move_legal(self, row: List[SudokuCell], col: List[SudokuCell], box: List[SudokuCell]) -> bool:
        return self.is_section_valid(row) and self.is_section_valid(col) and self.is_section_valid(box)

    def is_board_valid(self, board: SudokuBoard) -> bool:
        num_rows = len(board)
        num_cols = len(board[0])

        row_map = {i: set() for i in range(num_rows)}
        col_map = {i: set() for i in range(num_rows)}
        box_map = {i: set() for i in range(num_rows)}

        for row_num in range(num_rows):
            for col_num in range(num_cols):
                if board.get_cell(row_num, col_num).value == None:
                    continue

                num = board.get_cell(row_num, col_num).value

                # check row
                if num in row_map[row_num]:
                    return False
                else:
                    row_map[row_num].add(num)

                # check column
                if num in col_map[col_num]:
                    return False
                else:
                    col_map[col_num].add(num)

                # check box
                box_num =  board.get_cell(row_num, col_num).get_box_num()
                if num in box_map[box_num]:
                    return False
                else:
                    box_map[box_num].add(num)
                
        return True
    

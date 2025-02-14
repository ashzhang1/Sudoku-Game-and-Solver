from typing import List
from domain.sudoku_cell import SudokuCell
from domain.sudoku_board import SudokuBoard

class SudokuValidator:

    def __init__(self):
        pass

    def is_section_valid(self, section: List[SudokuCell]) -> bool:
        seen = set()
        for num in section:
            if num in seen:
                return False
            seen.add(num)
        return True
    
    def is_move_legal(self, row: List[SudokuCell], col: List[SudokuCell], box: List[SudokuCell]) -> bool:
        return self.is_section_valid(row) and self.is_section_valid(col) and self.is_section_valid(box)

    def is_board_valid(self, board: SudokuBoard) -> bool:
        num_rows = len(board)
        num_cols = len(board[0])

        row_map = dict()
        col_map = dict()
        box_map = dict()

        # for row in range(num_rows):
        #     for col in range(num_cols):
        #         if board[row][col] == None:
        #             continue

        #         num = board[row][col]
                
        #         if num in row_map:
        #             return False
        #         else:
        #             row_map[]
            



        return True

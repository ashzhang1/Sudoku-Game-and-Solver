from __future__ import annotations
from typing import List, Set, Tuple
from domain.sudoku_cell import SudokuCell
import copy

class SudokuBoard:

    def __init__(self, board_grid: List[List[SudokuCell]], is_valid: bool, is_complete: bool, selected_position: Tuple[int, int], highlighted_positions: Set[Tuple[int, int]], fixed_positions: List[Tuple[int, int]]):
        self.board_grid = board_grid
        self.is_valid = is_valid
        self.is_complete = is_complete
        self.selected_position = selected_position
        self.highlighted_positions = highlighted_positions
        self.fixed_positions = fixed_positions
    
    def get_cell(self, row: int, col: int) -> SudokuCell:
        return self.board_grid[row][col]
    
    def set_cell_value(self, row: int, col: int, val: int) -> None:
        self.board_grid[row][col].set_value(val)
    
    def clear_cell_value(self, row: int, col: int) -> None:
        self.board_grid[row][col].clear_value
    
    def set_selected_position(self, row: int, col: int) -> None:
        self.selected_position = (row, col)
    
    def clear_selected_position(self) -> None:
        self.selected_position = None
    
    def get_row(self, row: int) -> List[SudokuCell]:
        row_cells = list()
        for col_index in range(len(self.board_grid[row])):
            row_cells.append(self.board_grid[row][col_index])
        return row_cells
    
    def get_column(self, col: int) -> List[SudokuCell]:
        col_cells = list()
        for row_index in range(len(self.board_grid)):
            col_cells.append(self.board_grid[row_index][col])
        return col_cells
    
    def get_box(self, row: int, col: int) -> List[SudokuCell]:
        box_num = (row // 3) * 3 + (col // 3)
        box_cells = list()

        for row_index in range(len(self.board_grid)):
            for col_index in range(len(self.board_grid[row])):
                if self.board_grid[row_index][col_index].get_box_num == box_num:
                    box_cells.append(self.board_grid[row_index][col_index])
        
        return box_cells
    
    def is_position_fixed(self, row: int, col: int) -> bool:
        return self.board_grid[row][col].is_fixed()
    
    def is_board_complete(self) -> bool:
        return self.is_complete

    def reset_board(self) -> None:

        for row_index in range(len(self.board_grid)):
            for col_index in range(len(self.board_grid[0])):
                if not self.board_grid[row_index][col_index] in self.fixed_positions:
                    self.board_grid[row_index][col_index] = None
    

    def copy_board(self) -> SudokuBoard:
        return copy.deepcopy(self)


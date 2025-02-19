from typing import Dict, List, Tuple, Optional
from domain.sudoku_board import SudokuBoard
from domain.sudoku_cell import SudokuCell
from services.sudoku_validator import SudokuValidator

class SudokuSolver:
    def __init__(self, sudoku_board: SudokuBoard, validator: SudokuValidator):
        self.sudoku_board = sudoku_board
        self._validator = validator

    def solve(self) -> Optional[SudokuBoard]:
        """Main solve method using backtracking"""
        # First check if initial board is valid
        if not self._validator.is_grid_valid(self.sudoku_board.get_board_grid()):
            return None
        
        if self._solve_backtrack():
            return self.sudoku_board
        return None

    def _solve_backtrack(self) -> bool:
        """
        Basic backtracking algorithm. Will extend later to use AC3
        """
        # Find an empty cell
        empty_cell = self._find_empty_cell()
        if not empty_cell:
            return True

        row, col = empty_cell.get_row_num(), empty_cell.get_col_num()

        # Trying digits 1-9
        for val in range(1, 10):

            # Check if it is valid to place the value
            if self._is_valid_to_place(empty_cell, val):
                # Place the value
                self.sudoku_board.place_value(row, col, val)

                # Recursively try to solve the rest
                if self._solve_backtrack():
                    return True

                # If we got here, then need to backtrack cus last value didn't work
                self.sudoku_board.clear_cell_value(row, col)

        return False

    def _find_empty_cell(self) -> Optional[SudokuCell]:
        """Find first empty cell in the board"""
        for row_num in range(9):
            for col_num in range(9):
                cell = self.sudoku_board.get_cell(row_num, col_num)
                if cell.is_empty():
                    return cell
        return None # If we got here, then no empty cells and its complete

    def _is_valid_to_place(self, cell: SudokuCell, val: int) -> bool:
        """Check if its valid to place value in cell"""

        # Temporarily place the value to check if its valid
        row, col = cell.get_row_num(), cell.get_col_num()

        original_value = cell.value
        self.sudoku_board.place_value(row, col, val)

        # Check if the move is legal
        is_legal = self._validator.is_move_legal(
            self.sudoku_board.get_row(row),
            self.sudoku_board.get_column(col),
            self.sudoku_board.get_box(row, col)
        )

        # Put back the original value
        self.sudoku_board.clear_cell_value(row, col)
        if original_value is not None:
            self.sudoku_board.place_value(row, col, original_value)

        return is_legal
from typing import List
from services.sudoku_validator import SudokuValidator
from services.sudoku_solver import SudokuSolver
from domain.sudoku_board import SudokuBoard
from domain.sudoku_cell import SudokuCell
import random

class SudokuGenerator:

    def __init__(self):
        self._validator = SudokuValidator()

    def generate_sudoku(self) -> SudokuBoard:

        starting_board_grid = self._generate_starting_board()
        sudoku_board = SudokuBoard(starting_board_grid)

        filled_board = self._fill_board(sudoku_board)
        if filled_board is None:
            return None
        
        self._remove_numbers(filled_board)
        return filled_board

    
    def _generate_starting_board(self) -> List[List[SudokuCell]]:
        board_grid = list()

        for row_num in range(9):
            row = list()
            for col_num in range(9):
                row.append(SudokuCell(row_num, col_num))
            board_grid.append(row)
        
        return board_grid
    
    def _fill_board(self, board: SudokuBoard) -> SudokuBoard:
        """
        Core generator logic
        """
        # place random seed numbers
        self._place_random_seeds(board)

        # use solver to solve the board
        solver = SudokuSolver(board, self._validator)
        completed_board = solver.solve()

        # validate the completed board
        if completed_board is not None and self._validator.is_board_valid(completed_board):
            return completed_board
        
        return None

    def _place_random_seeds(self, empty_board: SudokuBoard) -> None:

        # fill top left box (box num 0)
        self._randomly_fill_box(empty_board, 0)

        # fill middle box (box num 4)
        self._randomly_fill_box(empty_board, 4)

        # fill bottom right box (box num 8)
        self._randomly_fill_box(empty_board, 8)

    
    def _randomly_fill_box(self, board: SudokuBoard, box_num: int):

        cells = board.get_cells_by_box_num(box_num)
        numbers = list(range(1, 10))
        random.shuffle(numbers)

        for cell, val in zip(cells, numbers):
            board.place_value(cell.get_row_num(), cell.get_col_num(), val)


    def _remove_numbers(self, board: SudokuBoard) -> None:
        positions = [(row, col) for row in range(9) for col in range(9)]
        random.shuffle(positions)
        
        # 81 squares in total and 35 fixed squares --> 46 blank squares
        # This is going to be fixed for now
        numbers_to_remove = 46
        removed_count = 0
        
        for pos in positions:

            row, col = pos
            # Store original value before removal
            original_value = board.get_cell(row, col).value
            
            # Try removing this number
            board.get_cell(row, col).clear_value()
            
            # Create new solver to test unique solution
            test_solver = SudokuSolver(board, self._validator)
            if test_solver.solve() is not None:
                removed_count += 1
                if removed_count == numbers_to_remove:
                    break
            else:
                # Put the number back b/c removal makes puzzle unsolvable
                board.place_value(row, col, original_value)
        
        # Set remaining numbers as fixed
        for row in range(9):
            for col in range(9):
                cell = board.get_cell(row, col)
                if not cell.is_empty():
                    cell.is_fixed = True


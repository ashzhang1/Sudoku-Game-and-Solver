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
        """Generate a new Sudoku puzzle"""

        # Create empty board
        board = SudokuBoard(self._generate_empty_board())
        
        # Place random seeds
        self._place_random_seeds(board)
        
        # Solve the rest of the board
        solver = SudokuSolver(board, self._validator)
        filled_board = solver.solve()
        
        if filled_board is None:
            print("Failed to generate valid board")
            return None
        
        # Remove numbers to create the puzzle
        self._remove_numbers(filled_board)
        self._mark_all_numbers_fixed(filled_board)
        return filled_board

    def _generate_empty_board(self) -> List[List[SudokuCell]]:
        """Create an empty 9x9 board"""
        return [[SudokuCell(row, col) for col in range(9)] for row in range(9)]

    def _fill_diagonal_boxes(self, board: SudokuBoard) -> None:
        """Fill the three diagonal 3x3 boxes with valid numbers"""
        # 0 -> top left box, 4 -> middle box, 8 -> bottom right box
        for box_num in [0, 4, 8]:
            self._fill_box(board, box_num)

    def _fill_box(self, board: SudokuBoard, box_num: int) -> None:
        """Fill a 3x3 box with a complete set of numbers 1-9"""
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        
        # Calculate starting position
        start_row = (box_num // 3) * 3
        start_col = (box_num % 3) * 3
        
        # Fill the box
        for i in range(3):
            for j in range(3):
                row = start_row + i
                col = start_col + j
                value = numbers[i * 3 + j]
                board.place_value(row, col, value)
                board.get_cell(row, col)._is_fixed = True
    
    def _place_random_seeds(self, board: SudokuBoard) -> None:
        """Place random seed numbers as starting points"""
        # Place around 10-12 random numbers
        num_seeds = random.randint(10, 12)
        positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(positions)
        
        seeds_placed = 0
        for row, col in positions:
            if seeds_placed >= num_seeds:
                break
                
            # Get valid numbers for this position
            valid_numbers = list(range(1, 10))
            random.shuffle(valid_numbers)
            
            for num in valid_numbers:
                # Try placing the number
                board.place_value(row, col, num)
                
                # Check if it's valid
                if self._validator.is_grid_valid(board.get_board_grid()):
                    board.get_cell(row, col)._is_fixed = True
                    seeds_placed += 1
                    break
                else:
                    board.clear_cell_value(row, col)

    def _remove_numbers(self, board: SudokuBoard) -> None:
        """Remove numbers while ensuring unique solution remains"""
        positions = [(row, col) for row in range(9) for col in range(9)]
        random.shuffle(positions)
        
        # Removing 45-52 numbers is considered to be easy to medium
        numbers_to_remove = random.randint(45, 52)
        removed = 0
        
        for row, col in positions:
            if removed >= numbers_to_remove:
                break
                
            cell = board.get_cell(row, col)
            temp_value = cell.value
            
            # Try removing it
            board.clear_cell_value(row, col)
            
            # Make a copy of the board for solving
            test_board = board.copy_board()
            solver = SudokuSolver(test_board, self._validator)
            
            # If still uniquely solvable, keep it removed
            if solver.solve() is not None:
                removed += 1
            else:
                # Put it back if removing it creates multiple solutions
                board.place_value(row, col, temp_value)

    def _mark_all_numbers_fixed(self, board: SudokuBoard) -> None:
        """Mark all non-empty cells as fixed"""
        for row in range(9):
            for col in range(9):
                cell = board.get_cell(row, col)
                if cell.value is not None:
                    cell.set_is_fixed(True)
                else:
                    cell.set_is_fixed(False)
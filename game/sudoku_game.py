from services.sudoku_generator import SudokuGenerator
from services.sudoku_validator import SudokuValidator
from services.sudoku_solver import SudokuSolver
import random


class SudokuGame:

    def __init__(self):
        self._generator = SudokuGenerator()
        self._validator = SudokuValidator()
        self._sudoku_board = None

    def start_new_game(self) -> None:
       # Keep trying until we get a valid board
        while True:
            board = self._generator.generate_sudoku()
            if board is not None:
                self._sudoku_board = board
                break

    def process_players_move(self, row_num: int, col_num: int, val: int) -> bool:
        # Not a valid position
        if not self._sudoku_board.is_position_valid(row_num, col_num):
            return False
        
        cell = self._sudoku_board.get_cell(row_num, col_num)
        
        # Cell is fixed so cant change it
        if cell.is_fixed():
            return False
        
        # Value is not valid
        if val < 1 or val > 9:
            return False
        
        # Check if move follows Sudoku rules
        row = self._sudoku_board.get_row(row_num)
        col = self._sudoku_board.get_column(col_num)
        box = self._sudoku_board.get_box(row_num, col_num)
        
        # Temporarily place value to check if valid
        og_val = cell.value
        cell.set_value(val)
        
        if not self._validator.is_move_legal(row, col, box):
            # Restore original value if move isn't legal
            cell.set_value(og_val)
            return False
            
        # Passed all checks
        self._sudoku_board.place_value(row_num, col_num, val)
        return True


    def clear_number(self, row_num: int, col_num: int) -> bool:
        # Not a valid position
        if not self._sudoku_board.is_position_valid(row_num, col_num):
            return False
        
        cell = self._sudoku_board.get_cell(row_num, col_num)
        
        # Cell is fixed so cant change it
        if cell.is_fixed():
            return False

        # Clear the number
        self._sudoku_board.clear_cell_value(row_num, col_num)
        return True

    def is_game_won(self):
        return self._sudoku_board.is_board_complete()
    
    def get_hint(self) -> bool:
        """
        Reveals one random empty cell's correct value
        """
        # Get all empty cells
        empty_cells = []
        for row in range(9):
            for col in range(9):
                cell = self._sudoku_board.get_cell(row, col)
                if cell.is_empty():
                    empty_cells.append((row, col))
        
        if not empty_cells:
            return False  # No empty cells left
            
        # Pick a random empty cell
        row, col = random.choice(empty_cells)
        
        # Create a copy of the board for solving
        board_copy = self._sudoku_board.copy_board()
        solver = SudokuSolver(board_copy, self._validator)
        
        # Solve the board to get the correct value
        if solver.solve():
            correct_value = board_copy.get_cell(row, col).value
            # Place the value on the original board
            self._sudoku_board.place_value(row, col, correct_value)
            self._sudoku_board.get_cell(row, col).set_is_fixed(True)  # Make it fixed
            return True
            
        return False

    def solve_game(self) -> bool:
        if not self._sudoku_board:
            return False
            
        solver = SudokuSolver(self._sudoku_board, self._validator)
        
        if solver.solve():
            # Store which cells were empty before solving
            was_empty = [[self._sudoku_board.get_cell(row, col).is_empty() 
                        for col in range(9)] for row in range(9)]
            
            # Only mark newly filled cells as fixed (orange)
            for row in range(9):
                for col in range(9):
                    cell = self._sudoku_board.get_cell(row, col)
                    if was_empty[row][col]:  # Only change color of new numbers
                        cell.set_is_fixed(True)
            return True
            
        return False




from services.sudoku_generator import SudokuGenerator
from services.sudoku_validator import SudokuValidator
from services.sudoku_solver import SudokuSolver
from domain.sudoku_board import SudokuBoard
from domain.sudoku_cell import SudokuCell


class SudokuGame:

    def __init__(self):
        self._generator = SudokuGenerator()
        self._validator = SudokuValidator()
        self._sudoku_board = None

    def start_new_game(self) -> None:
       self._sudoku_board = self._generator.generate_sudoku()

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




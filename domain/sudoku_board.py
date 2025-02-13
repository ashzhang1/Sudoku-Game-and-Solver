from typing import List, Set, Tuple
from domain.sudoku_cell import SudokuCell

class SudokuBoard:

    def __init__(self, board_grid: List[List[SudokuCell]], is_valid: bool, is_complete: bool, selected_position: Tuple[int, int], highlighted_positions: Set[Tuple[int, int]], fixed_positions: List[Tuple[int, int]]):
        pass
from typing import Dict, List, Tuple
from domain.sudoku_board import SudokuBoard
from domain.sudoku_cell import SudokuCell
from services.sudoku_validator import SudokuValidator

class sudoku_solver:

    def __init__(self, sudoku_board: SudokuBoard):
        self.sudoku_board = sudoku_board
        self._validator = SudokuValidator()
        self._stack: List[Tuple[SudokuCell, int]] = []
        self._domain_changes: Dict[int, List[Tuple[int, int]]] = {}
        self._move_count = 0
    
    def solve(self): pass

    def _ac3(self): pass

    def _forward_check(self) -> bool:
        changes = self._domain_changes[self._move_count]
        for (cell, _) in changes:
            if len(cell.get_candidate_values()) == 0:
                return False
        
        return True

    def _get_mrv_cell(self) -> SudokuCell:
        num_rows = len(self.sudoku_board)
        num_cols = len(self.sudoku_board[0])

        min_cell = None
        min_remaining_vals = 9 # 9 is the max

        for row_num in range(num_rows):
            for col_num in range(num_cols):
                curr_cell = self.sudoku_board.get_cell(row_num, col_num)
                if not curr_cell.is_empty():
                    continue
                elif not curr_cell.is_fixed() and len(curr_cell.get_candidate_values()) < min_remaining_vals:
                    min_remaining_vals = len(curr_cell.get_candidate_values())
                    min_cell = curr_cell
        
        return min_cell

    def _place_value(self, cell: SudokuCell, value: int) -> None:

        # Add to the move count
        self._move_count += 1

        # Place the actual value
        cell.set_value(value)

        # Add to stack
        self._stack.append((cell, value))

        # Domain changes
        self._domain_changes[self._move_count] = []
        
        # Related cells
        related_cells = set()
        related_cells.update(self.sudoku_board.get_row(cell.get_row_num()))
        related_cells.update(self.sudoku_board.get_column(cell.get_col_num()))
        related_cells.update(self.sudoku_board.get_box(cell.get_row_num(), cell.get_col_num()))
        related_cells.remove(cell)

        for related_cell in related_cells:
            if value in related_cell.get_candidate_values():
                related_cell.remove_candidate_value(value)
                self._domain_changes[self._move_count].append((related_cell, value))
        

    def _undo_last_move(self) -> None:
        self._restore_domains()
        cell = self._stack.pop()[0]
        cell.clear_value()
        self._move_count -= 1

    def _is_value_valid(self, cell: SudokuCell, value: int) -> bool:
        row_num = cell.get_row_num()
        col_num = cell.get_col_num()
        box_num = cell.get_box_num()

        self._place_value(cell, value)

        valid = self._validator.is_move_legal(self.sudoku_board.get_row(row_num), 
                                              self.sudoku_board.get_column(col_num), 
                                              self.sudoku_board.get_box(box_num))
        self._undo_last_move()
        if valid:
            return True
        
        return False

    def _get_unassigned_cells(self) -> List[SudokuCell]:
        unassigned_cells = list()
        num_rows = len(self.sudoku_board)
        num_cols = len(self.sudoku_board[0])

        for row_num in range(num_rows):
            for col_num in range(num_cols):
                if self.sudoku_board.get_cell(row_num, col_num).value == None:
                    unassigned_cells.append(self.sudoku_board.get_cell(row_num, col_num))
        return unassigned_cells


    # Undoing the domain restrictions that came from your last move
    def _restore_domains(self) -> None:
        changes = self._domain_changes[self._move_count]
        for (cell, value) in changes:
            cell.add_candidate_value(value)
        
        del self._domain_changes[self._move_count]
        


        









    
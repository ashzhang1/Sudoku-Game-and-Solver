from typing import Dict, List, Tuple
from domain.sudoku_board import SudokuBoard
from domain.sudoku_cell import SudokuCell
from services.sudoku_validator import SudokuValidator
from collections import deque

class sudoku_solver:

    def __init__(self, sudoku_board: SudokuBoard):
        self.sudoku_board = sudoku_board
        self._validator = SudokuValidator()
        self._stack: List[Tuple[SudokuCell, int]] = []
        self._domain_changes: Dict[int, List[Tuple[int, int]]] = {}
        self._move_count = 0
    
    def solve(self) -> SudokuBoard:
        """
        main solve method
        """

        # Initial board is unsolvable
        if not self._ac3():
            return None

        while not self.sudoku_board.is_board_complete():

            mrv_cell = self._get_mrv_cell()

            # No more mrv cell, so we need to backtrack
            if mrv_cell == None:
                if len(self._stack) == 0:
                    return None # No solution exists
                self._undo_last_move()
                continue

            # Begin to try candidate values
            value_placed = False
            for val in mrv_cell.get_candidate_values():

                # Try this value
                self._place_value(mrv_cell, val)

                if not self._forward_check():
                    self._undo_last_move()
                    continue # Try next value

                if not self._ac3():
                    self._undo_last_move()
                    continue # Try next value

                value_placed = True
                break

             # None of values were able to be placed
            if not value_placed:
                if len(self._stack) == 0:
                    return None  # No solution exists
            self._undo_last_move()
            continue

        return self.sudoku_board


    def _ac3(self) -> bool:

        # Queue that contains the arcs
        queue = deque()
        queue.extend(self._get_all_arcs())

        # Iterate until queue is empty or we get inconsistency
        while queue:
            arc = queue.popleft()
            domain_changed = self._check_arc_consistency(arc)

            from_cell = arc[0]

            # Empty domain --> arc is inconsistent
            if len(from_cell.get_candidate_values()) == 0:
                return False

            if domain_changed:
                queue.extend(self._add_back_arcs(arc[0]))
        
        return True
    
    def _get_all_arcs(self) -> List[Tuple[SudokuCell, SudokuCell]]:
        result = list()
        num_rows = len(self.sudoku_board)
        num_cols = len(self.sudoku_board[0])

        for row_num in range(num_rows):
            for col_num in range(num_cols):
                from_cell = self.sudoku_board.get_cell(row_num, col_num)
                result.extend([(cell, from_cell) for cell in self.sudoku_board.get_row(row_num) if cell != from_cell])
                result.extend([(cell, from_cell) for cell in self.sudoku_board.get_column(col_num) if cell != from_cell])
                result.extend([(cell, from_cell) for cell in self.sudoku_board.get_box(row_num, col_num) if cell != from_cell])
        
        return result


    def _check_arc_consistency(self, arc: Tuple[SudokuCell, SudokuCell]) -> bool:
        """
        Given 2 cells (A, B), this function will find any values in A that have
        no supporting value in B. Then we need to remove that value.

        If we did remove that value from A's domain,
        then we return true as A's domain has changed
        """
        domain_changed = False
        cell_a = arc[0]
        cell_b = arc[1]

        for a_value in cell_a.get_candidate_values():
            supporting_val_found = self._find_supporting_value(a_value, cell_b.get_candidate_values())

            # value a is not supported, must be removed
            if not supporting_val_found:
                cell_a.remove_candidate_value(a_value)
                domain_changed = True
            
        return domain_changed
    

    def _find_supporting_value(self, val: int, candidates: List[int]) -> bool:
        for candidate in candidates:
            if candidate != val:
                return True
        return False


    def _add_back_arcs(self, cell: SudokuCell) -> List[Tuple[SudokuCell, SudokuCell]]:

        result = list()

        cell_row = cell.get_row_num()
        cell_col = cell.get_col_num()
        cell_box = cell.get_box_num()

        result.extend([(related_cell, cell) for related_cell in self.sudoku_board.get_row(cell_row) if cell != related_cell])
        result.extend([(related_cell, cell) for related_cell in self.sudoku_board.get_column(cell_col) if cell != related_cell])
        result.extend([(related_cell, cell) for related_cell in self.sudoku_board.get_box(cell_row, cell_box) if cell != related_cell])
        
        return result


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
        


        









    
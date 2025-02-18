from __future__ import annotations
from typing import List, Set, Tuple
from domain.sudoku_cell import SudokuCell
from services.sudoku_validator import SudokuValidator
import copy

class SudokuBoard:

    def __init__(
        self, 
        board_grid: List[List[SudokuCell]],
        selected_position: Tuple[int, int] = None, 
        highlighted_positions: Set[Tuple[int, int]] = None, 
        fixed_positions: List[Tuple[int, int]] = None
    ):
        self.board_grid = board_grid
        self.selected_position = selected_position
        self.highlighted_positions = highlighted_positions
        self.fixed_positions = fixed_positions

    def get_board_grid(self) -> List[List[SudokuCell]]:
        return self.board_grid
    
    def get_cell(self, row: int, col: int) -> SudokuCell:
        return self.board_grid[row][col]
    
    def place_value(self, row: int, col: int, val: int) -> None:
        self.board_grid[row][col].set_value(val)
        self.board_grid[row][col].clear_candidate_values()
        self._update_related_cells(self.board_grid[row][col], val)

    def _update_related_cells(self, cell: SudokuCell, value: int, is_removing: bool = True) -> None:
        # Get all related cells
        related_cells = set()
        related_cells.update(self.get_row(cell.get_row_num()))
        related_cells.update(self.get_column(cell.get_col_num()))
        related_cells.update(self.get_box(cell.get_row_num(), cell.get_col_num()))
        related_cells.remove(cell)  # Remove the cell itself

        # Update candidates of all related cells
        for related_cell in related_cells:
            if is_removing:
                if value in related_cell.get_candidate_values():
                    related_cell.remove_candidate_value(value)
            else:
                if value not in related_cell.get_candidate_values():
                    related_cell.add_candidate_value(value)
    
    def clear_cell_value(self, row: int, col: int) -> None:
        cell = self.board_grid[row][col]
        old_value = cell.value

        if old_value is not None:
            cell.clear_value()
            # Need to add back this value to the related cells
            self._update_related_cells(cell, old_value, is_removing=False)
    
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
        # Calculate box number from row and column
        box_num = (row // 3) * 3 + (col // 3)
        return self.get_cells_by_box_num(box_num)

    def get_cells_by_box_num(self, box_num: int) -> List[SudokuCell]:
        # Convert box_num to starting row/col
        start_row = (box_num // 3) * 3
        start_col = (box_num % 3) * 3
        
        box_cells = []
        
        for row in range(start_row, start_row + 3):
            for col in range(start_col, start_col + 3):
                box_cells.append(self.board_grid[row][col])
        
        return box_cells
    
    def is_position_fixed(self, row: int, col: int) -> bool:
        return self.board_grid[row][col].is_fixed()
    
    def is_board_complete(self) -> bool:
        for row in range(9):
            for col in range(9):
                if self.board_grid[row][col].is_empty():
                    return False
        
        validator = SudokuValidator()
        return validator.is_grid_valid(self.board_grid)

    def reset_board(self) -> None:
        for row_index in range(len(self.board_grid)):
            for col_index in range(len(self.board_grid[0])):
                cell = self.board_grid[row_index][col_index]
                if not cell.get_position() in self.fixed_positions:
                    self.board_grid[row_index][col_index] = None

    def copy_board(self) -> SudokuBoard:
        return copy.deepcopy(self)
    
    def is_position_valid(self, row: int, col: int) -> bool:
        return (row >= 0 and row < 9) and (col >= 0 and col < 9)
    
    def copy_board(self) -> 'SudokuBoard':
        """Create a new copy of this board"""
        # Create new grid with copied cells
        new_grid = []
        for row in self.board_grid:
            new_row = []
            for cell in row:
                new_row.append(cell.copy())
            new_grid.append(new_row)
        
        # Copy other board properties
        new_selected_pos = self.selected_position
        new_highlighted_pos = set(self.highlighted_positions) if self.highlighted_positions else None
        new_fixed_pos = list(self.fixed_positions) if self.fixed_positions else None
        
        return SudokuBoard(
            board_grid=new_grid,
            selected_position=new_selected_pos,
            highlighted_positions=new_highlighted_pos,
            fixed_positions=new_fixed_pos
        )

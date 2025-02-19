import pytest
from domain.sudoku_cell import SudokuCell
from services.sudoku_validator import SudokuValidator

# Test data for valid boards
valid_boards = [
    # Complete valid board
    ([
        [5,3,4,6,7,8,9,1,2],
        [6,7,2,1,9,5,3,4,8],
        [1,9,8,3,4,2,5,6,7],
        [8,5,9,7,6,1,4,2,3],
        [4,2,6,8,5,3,7,9,1],
        [7,1,3,9,2,4,8,5,6],
        [9,6,1,5,3,7,2,8,4],
        [2,8,7,4,1,9,6,3,5],
        [3,4,5,2,8,6,1,7,9]
    ], "complete valid board"),
    
    # Incomplete valid board
    ([
        [5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9]
    ], "incomplete valid board")
]

# Test data for invalid boards
invalid_boards = [
    # Duplicate in row
    ([
        [5,3,4,6,7,8,9,1,5],  # Duplicate 5 in first row
        [6,7,2,1,9,5,3,4,8],
        [1,9,8,3,4,2,5,6,7],
        [8,5,9,7,6,1,4,2,3],
        [4,2,6,8,5,3,7,9,1],
        [7,1,3,9,2,4,8,5,6],
        [9,6,1,5,3,7,2,8,4],
        [2,8,7,4,1,9,6,3,5],
        [3,4,5,2,8,6,1,7,9]
    ], "duplicate in row"),
    
    # Duplicate in column
    ([
        [5,3,4,6,7,8,9,1,2],
        [6,7,2,1,9,5,3,4,8],
        [1,9,8,3,4,2,5,6,7],
        [8,5,9,7,6,1,4,2,3],
        [4,2,6,8,5,3,7,9,1],
        [7,1,3,9,2,4,8,5,6],
        [9,6,1,5,3,7,2,8,4],
        [2,8,7,4,1,9,6,3,5],
        [3,4,5,2,8,6,1,7,2]  # Duplicate 2 in last column
    ], "duplicate in column"),

    ([
        [5,3,4,6,7,8,9,1,2],
        [6,7,2,1,9,5,3,4,8],
        [1,9,8,3,4,2,5,6,7],
        [8,5,9,7,6,1,4,2,3],
        [4,2,6,8,5,3,7,9,1],
        [7,1,3,9,2,4,8,5,6],
        [9,6,1,5,3,7,2,8,4],
        [2,8,7,4,1,9,6,3,5],
        [3,4,5,2,8,6,1,7,7]  # Duplicate 7 in bottom-right 3x3 box
], "duplicate in 3x3 box")


]

def create_grid(numbers):
    """Helper function to create grid of SudokuCell objects"""
    grid = []
    for i in range(9):
        row = []
        for j in range(9):
            value = None if numbers[i][j] == 0 else numbers[i][j]
            is_fixed = value is not None # Make non-zero values fixed
            cell = SudokuCell(i, j, value, is_fixed)
            row.append(cell)
        grid.append(row)
    return grid

@pytest.mark.parametrize("board,description", valid_boards)
def test_valid_boards(board, description):
    grid = create_grid(board)
    validator = SudokuValidator()
    assert validator.is_grid_valid(grid) == True, f"Failed on {description}"

@pytest.mark.parametrize("board,description", invalid_boards)
def test_invalid_boards(board, description):
    grid = create_grid(board)
    validator = SudokuValidator()
    assert validator.is_grid_valid(grid) == False, f"Failed on {description}"
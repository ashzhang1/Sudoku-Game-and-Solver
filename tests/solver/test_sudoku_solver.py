import pytest
from domain.sudoku_cell import SudokuCell
from domain.sudoku_board import SudokuBoard
from services.sudoku_solver import SudokuSolver
from services.sudoku_validator import SudokuValidator

# Test data for solvable boards
solvable_boards = [
    # Unsolved board 1
    ([
        [6,0,0,0,0,7,4,3,0],
        [0,0,3,0,0,0,6,8,2],
        [0,4,8,0,0,3,0,9,0],
        [7,6,0,0,4,1,0,0,0],
        [0,0,2,7,0,5,1,0,0],
        [0,0,0,3,8,0,0,7,9],
        [0,3,0,1,0,0,9,2,0],
        [8,1,4,0,0,0,5,0,0],
        [0,2,7,5,0,0,0,0,4]
    ], "standard unsolved board 1"),

    # Unsolved board 2
    ([
        [0,0,0,8,0,0,6,0,2],
        [6,4,0,5,0,7,0,0,0],
        [8,0,7,0,6,0,0,0,0],
        [4,9,6,3,0,2,1,0,7],
        [2,0,0,4,7,0,0,9,6],
        [7,5,3,9,0,0,0,0,4],
        [1,0,0,2,0,9,0,0,0],
        [0,6,0,7,0,0,0,0,0],
        [0,7,4,0,5,1,9,2,0]
    ], "standard unsolved board 2"),
    
    # Unsolved board 3
    ([
        [6,0,0,5,0,0,9,0,0],
        [8,0,1,6,0,4,2,7,0],
        [0,0,0,0,7,2,6,0,0],
        [0,0,0,0,8,1,7,0,4],
        [0,0,4,0,3,0,1,0,0],
        [0,5,0,0,0,9,0,2,3],
        [0,0,0,0,0,6,0,0,0],
        [0,6,0,0,0,0,4,0,0],
        [0,0,0,3,4,0,5,0,6]
    ], "standard unsolved board 3")
]

# Test data for unsolvable boards
unsolvable_boards = [
    # Board with row conflict
    ([
        [5,5,0,0,0,0,0,0,0],  # Two 5s in first row
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]
    ], "board with row conflict"),
    
    # Board with column conflict
    ([
        [0,0,0,0,2,0,0,0,0],
        [0,0,0,0,2,0,0,0,0],  # Two 5s in fifth column
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]
    ], "board with column conflict"),

    # Board with box conflict
    ([
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],  # Two 1s in last box
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0],
        [0,0,0,0,0,0,0,0,1]
    ], "board with box conflict"),
    ([
        [5,3,0,0,7,0,0,0,2],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [2,0,0,0,8,0,0,7,9]
    ], "unsolvable but no conflicts")
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

def print_board(grid):
    """Helper function to print the board"""
    print("\nBoard state:")
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            cell = grid[i][j]
            value = cell.value if cell.value is not None else "."
            print(value, end=" ")
        print()  # New line after each row
    print()

@pytest.mark.parametrize("board,description", solvable_boards)
def test_solvable_boards(board, description):
    print(f"\nTesting {description}")
    grid = create_grid(board)
    board = SudokuBoard(grid)
    
    print("Initial board:")
    print_board(board.get_board_grid())
    
    validator = SudokuValidator()
    solver = SudokuSolver(board, validator)
    
    result = solver.solve()
    
    assert result is not None, f"Failed to solve {description}"
    assert board.is_board_complete(), f"Board not complete after solving {description}"
    assert validator.is_grid_valid(board.get_board_grid()), f"Solution for {description} is not valid"
    
    print("Solved board:")
    print_board(board.get_board_grid())

@pytest.mark.parametrize("board,description", unsolvable_boards)
def test_unsolvable_boards(board, description):
    print(f"\nTesting {description}")
    grid = create_grid(board)
    board = SudokuBoard(grid)
    
    print("Initial board:")
    print_board(board.get_board_grid())
    
    validator = SudokuValidator()
    solver = SudokuSolver(board, validator)
    
    result = solver.solve()
    
    assert result is None, f"Should not be able to solve {description}"
    print("Result: UNSOLVABLE")
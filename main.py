from game.sudoku_game import SudokuGame

def debug_print_board(board):
    """Simple debug printing of the board - just for testing"""
    for row in range(9):
        if row % 3 == 0:
            print('-' * 25)
        row_str = ''
        for col in range(9):
            if col % 3 == 0:
                row_str += '| '
            cell = board.get_cell(row, col)
            value = cell.value if cell.value is not None else '.'
            fixed = '*' if cell.is_fixed() else ' '
            row_str += f"{value}{fixed} "
        print(row_str + '|')
    print('-' * 25)

def test_core_functionality():
    # Run multiple tests to check randomness
    for i in range(3):
        print(f"\nTest Game {i + 1}")
        print("=================")
        
        # Create and start new game
        game = SudokuGame()
        game.start_new_game()
        
        # Verify board was generated
        if game._sudoku_board is None:
            print("ERROR: Board generation failed")
            return
        print("✓ Board generated successfully")
        
        # Print the board
        print("\nGenerated board (fixed numbers marked with *):")
        debug_print_board(game._sudoku_board)
        
        # Count fixed cells
        fixed_count = sum(1 for row in range(9) for col in range(9) 
                         if game._sudoku_board.get_cell(row, col).is_fixed())
        print(f"✓ Board has {fixed_count} fixed cells")
        
        # Test some moves
        test_moves = [
            (0, 0, 5),
            (9, 9, 1),  # invalid position
            (0, 1, 10)  # invalid number
        ]
        
        for row, col, val in test_moves:
            if game._sudoku_board.is_position_valid(row, col):
                cell = game._sudoku_board.get_cell(row, col)
                if not cell.is_fixed():
                    success = game.process_players_move(row, col, val)
                    print(f"✓ Move ({row},{col})={val} {'succeeded' if success else 'failed'} as expected")

if __name__ == "__main__":
    test_core_functionality()
import pygame
from game.sudoku_game import SudokuGame
from views.sudoku_board_gui import SudokuBoardGUI
from views.game_control_panel import GameControlPanel

class SudokuGameGUI:
    def __init__(self):
        # Initialise pygame
        pygame.init()
        
        # Game window
        self.WINDOW_SIZE = (900, 600)
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption("Sudoku Game")
        
        # Sudokue game instance
        self.game = SudokuGame()
        self.game.start_new_game()
        
        # Create GUI components
        self.board = SudokuBoardGUI(50, 50, 450)
        self.board.set_board(self.game._sudoku_board)  # This connects the board GUI to actual game
        self.control_panel = GameControlPanel(550, 50, 300, 500)
    
    def run(self):
        running = True
        while running:
            # Handle events
            running = self.handle_events()
            
            # Clear screen
            self.screen.fill((255, 255, 255))
            
            # Draw components
            self.board.draw(self.screen)
            self.control_panel.draw(self.screen)
            
            # Update display
            pygame.display.flip()
            
        pygame.quit()
    
    def handle_control_action(self, action: str):
        """This handles the buttons in the control panel (right side)"""
        if action == "validate":
            # Check if board is complete first
            if not self.game._sudoku_board.is_board_complete():
                self.board.set_status("board is not complete")
            else:
                # Check if solution is valid
                validator = self.game._validator
                if validator.is_grid_valid(self.game._sudoku_board.get_board_grid()):
                    self.board.set_status("correct")
                else:
                    self.board.set_status("incorrect")
            pygame.display.flip()
        elif action == "new_game":
            self.game.start_new_game()
            self.board.set_board(self.game._sudoku_board)  # Update board reference
            self.board.selected_cell = None  # Clear any selected cell
            self.board.set_status("in progress")  # Reset status
            pygame.display.flip()
            print("Starting new game")
        elif action == "hint":
            success = self.game.get_hint()
            if success:
                # Update the board display
                self.board.set_board(self.game._sudoku_board)
                self.board.set_status("in progress - hint provided")  # Reset status
                pygame.display.flip()
        elif action == "solve":
            success = self.game.solve_game()
            if success:
                # Update the board display
                self.board.set_board(self.game._sudoku_board)
                self.board.selected_cell = None  # Clear any selected cell
                self.board.set_status("solved")  # Set solved status
                pygame.display.flip()
                print("Puzzle solved successfully")
            else:
                print("Unable to solve puzzle")
    
    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            # Handle board events
            if event.type == pygame.MOUSEBUTTONDOWN:
                cell = self.board.handle_click(event.pos)
                if cell:
                    print(f"Selected cell: {cell}")
                    
            # Handle keyboard input
            if event.type == pygame.KEYDOWN:
                self.handle_keyboard_input(event)
            
            # Handle control panel events
            action = self.control_panel.handle_event(event)
            if action:
                self.handle_control_action(action)
                
        return True
    
    def handle_keyboard_input(self, event):
        """This handles keyboard input for number entry"""
        selected_cell = self.board.get_selected_cell()
        if not selected_cell:
            return
            
        row, col = selected_cell
        
        # Handle number keys (both main keyboard and numpad)
        if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                        pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                        
            # Convert key to number (1-9)
            if event.key <= pygame.K_9:
                number = event.key - pygame.K_0
            else:
                number = event.key - pygame.K_KP0
                
            # Only place the number if it's a valid move
            if not self.game.process_players_move(row, col, number):
                print(f"Invalid move at ({row}, {col})")
                return
                
        # Delete/backspace to clear a cell
        elif event.key in [pygame.K_DELETE, pygame.K_BACKSPACE]:
            success = self.game.clear_number(row, col)
            if success:
                print(f"Cleared cell at ({row}, {col})")
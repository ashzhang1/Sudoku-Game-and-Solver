import pygame
from domain.sudoku_board import SudokuBoard

class SudokuBoardGUI:
    def __init__(self, x: int, y: int, width: int):
        self.x = x
        self.y = y
        self.width = width
        self.cell_size = width // 9
        self.selected_cell = None
        self.board = None
        
        # Colours
        self.grid_colour = (0, 0, 0)           # Black
        self.background_colour = (255, 255, 255)  # White
        self.selected_colour = (200, 200, 200)  # Light gray for selected cell
        self.fixed_number_colour = (236, 99, 48)    # Fixed numbers
        self.player_number_colour = (103, 206, 103)  # Blue for player numbers

        self.status_colours = {
            "in progress": (0, 0, 0),         # Black
            "incorrect": (255, 0, 0),         # Red
            "correct": (0, 128, 0)            # Dark Green
        }

        # Game status
        self.game_status = "in progress"
        self.status_font = pygame.font.Font(None, 24)
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        
    def set_board(self, board: SudokuBoard):
        """Set the game board to display"""
        self.board = board
        
    def draw(self, screen: pygame.Surface) -> None:
        # Draw background
        pygame.draw.rect(screen, self.background_colour, 
                        (self.x, self.y, self.width, self.width))
        
        # Draw selected cell if there is one
        if self.selected_cell:
            row, col = self.selected_cell
            pygame.draw.rect(screen, self.selected_colour,
                           (self.x + col * self.cell_size,
                            self.y + row * self.cell_size,
                            self.cell_size, self.cell_size))
        
        # Draw numbers if board exists
        if self.board:
            self._draw_numbers(screen)
        
        # Draw grid lines
        self._draw_grid(screen)

        # Draw status
        self._draw_status(screen)
    
    def _draw_numbers(self, screen: pygame.Surface):
        """This draws all numbers on the board"""
        for row in range(9):
            for col in range(9):
                cell = self.board.get_cell(row, col)
                if cell.value is not None:
                    # Get font and colour based on whether number is fixed
                    font = self.font
                    colour = self.fixed_number_colour if cell.is_fixed() else self.player_number_colour
                    
                    # Draw the number
                    number_text = str(cell.value)
                    text_surface = font.render(number_text, True, colour)
                    
                    # Center number in cell
                    text_rect = text_surface.get_rect()
                    text_rect.center = (self.x + col * self.cell_size + self.cell_size // 2,
                                      self.y + row * self.cell_size + self.cell_size // 2)
                    
                    screen.blit(text_surface, text_rect)
    
    def _draw_grid(self, screen: pygame.Surface):
        """Draw the grid lines"""
        for i in range(10):
            line_thickness = 3 if i % 3 == 0 else 1 # Every third one is bolded
            
            # Vertical lines
            pygame.draw.line(screen, self.grid_colour,
                           (self.x + i * self.cell_size, self.y),
                           (self.x + i * self.cell_size, self.y + self.width),
                           line_thickness)
            
            # Horizontal lines
            pygame.draw.line(screen, self.grid_colour,
                           (self.x, self.y + i * self.cell_size),
                           (self.x + self.width, self.y + i * self.cell_size),
                           line_thickness)
            
    def set_status(self, status: str) -> None:
        """
        Set the game status with optional number for invalid move messages
        Params:
            status: Status string (in progress/incorrect/correct/solved/invalid)
        """
        if status == "solved":
            self.game_status = "solved by computer"
        else:
            self.game_status = status.lower()
    
    def reset_status(self) -> None:
        self.game_status = "in progress"
    
    def _draw_status(self, screen: pygame.Surface) -> None:
        status_text = f"Game Status: {self.game_status.title()}"
        text_surface = self.status_font.render(
            status_text,
            True,
            self.status_colours.get(self.game_status, self.status_colours["in progress"])
        )
        
        # Position status below the board and aligned with left edge
        text_rect = text_surface.get_rect()
        text_rect.topleft = (self.x, self.y + self.width + 20)
        
        screen.blit(text_surface, text_rect)
        
    def handle_click(self, mouse_pos: tuple) -> tuple:
        """This converts the mouse position to grid position"""
        mouse_x, mouse_y = mouse_pos
    
        # Check if click is within board bounds
        if (self.x <= mouse_x <= self.x + self.width and 
            self.y <= mouse_y <= self.y + self.width):
            
            # Calculate grid position
            row = (mouse_y - self.y) // self.cell_size
            col = (mouse_x - self.x) // self.cell_size
            
            self.selected_cell = (row, col)
            return row, col
        
        self.selected_cell = None
        return None
        
    def get_selected_cell(self) -> tuple:
        return self.selected_cell
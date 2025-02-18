import pygame
from views.button import Button

class GameControlPanel:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        
        # Button dimensions
        self.new_game_width = 310
        self.new_game_height = 50
        self.small_button_width = 150
        self.small_button_height = 50
        
        # Calculate center position for buttons
        center_x = x + (width // 2)

        # Validate button
        self.validate_btn = Button(
            center_x - (self.new_game_width // 2),
            y + 250,
            self.new_game_width,
            self.new_game_height,
            "Validate"
        )
        
        # New game button
        self.new_game_btn = Button(
            center_x - (self.new_game_width // 2),
            y + 320,
            self.new_game_width, 
            self.new_game_height, 
            "New Game"
        )
        
        # Hint and solve buttons
        # Need to calculate this cus I want them half size of larger buttons
        small_buttons_total_width = (self.small_button_width * 2) + 10
        hint_x = center_x - (small_buttons_total_width // 2)
        solve_x = hint_x + self.small_button_width + 10
        
        self.hint_btn = Button(
            hint_x,
            y + 400, 
            self.small_button_width,
            self.small_button_height, 
            "Hint"
        )
        
        self.solve_btn = Button(
            solve_x,
            y + 400,
            self.small_button_width,
            self.small_button_height, 
            "Solve"
        )
        
        # Rules text
        self.rules = [
            "Rules of Sudoku",
            "1. Fill empty cells with numbers 1-9.",
            "2. Each row must include every number from 1 to 9 exactly once.",
            "3. Each column must include every number from 1 to 9 exactly once.",
            "4. Each 3×3 box must include every number from 1 to 9 exactly once."
        ]
        
        # Fonts for rules
        self.title_font = pygame.font.Font(None, 24)
        self.rules_font = pygame.font.Font(None, 20)
        self.title_font.set_bold(True)
        
        # Spacing params
        self.rules_margin = 8
        self.rules_padding = 15
        self.rules_line_height = 24
        self.rules_width = width - (self.rules_margin * 2)
        
    def draw(self, screen: pygame.Surface) -> None:
        # Start position for rules
        rules_start_y = self.rect.y + self.rules_padding
        y_offset = rules_start_y
        
        # Calculate rules box size and draw border
        total_height = 0
        lines_to_draw = []
        
        # Process each rule
        for rule in self.rules:
            words = rule.split()
            current_line = words[0]
            
            for word in words[1:]:
                test_line = current_line + " " + word
                test_font = self.title_font if current_line == "Rules of Sudoku" else self.rules_font
                test_surface = test_font.render(test_line, True, (0, 0, 0))
                
                if test_surface.get_width() <= self.rules_width - (self.rules_padding * 2):
                    current_line = test_line
                else:
                    lines_to_draw.append(current_line)
                    total_height += self.rules_line_height
                    current_line = word
            
            lines_to_draw.append(current_line)
            total_height += self.rules_line_height
        
        # Draw border around rules
        border_rect = pygame.Rect(
            self.rect.x + self.rules_margin - self.rules_padding,
            rules_start_y - self.rules_padding,
            self.rules_width + (self.rules_padding * 2),
            total_height + (self.rules_padding * 2)
        )
        pygame.draw.rect(screen, (0, 0, 0), border_rect, 2)
        
        # Draw the text
        y_offset = rules_start_y
        for line in lines_to_draw:
            # Use title font for "Rules of Sudoku", regular font for other lines
            if line == "Rules of Sudoku":
                text_surface = self.title_font.render(line, True, (0, 0, 0))
            else:
                text_surface = self.rules_font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect()
            text_rect.x = self.rect.x + self.rules_margin
            text_rect.y = y_offset
            screen.blit(text_surface, text_rect)
            y_offset += self.rules_line_height
        
        # Draw buttons
        self.validate_btn.draw(screen)
        self.new_game_btn.draw(screen)
        self.hint_btn.draw(screen)
        self.solve_btn.draw(screen)
        
    def handle_event(self, event: pygame.event.Event) -> str:
        if self.validate_btn.handle_event(event):
            return "validate"
        if self.new_game_btn.handle_event(event):
            return "new_game"
        if self.hint_btn.handle_event(event):
            return "hint"
        if self.solve_btn.handle_event(event):
            return "solve"
        return None
import pygame

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_hovered = False
        self.is_clicked = False
        
        # Colours
        self.normal_color = (255, 255, 255)    # White
        self.hover_color = (240, 240, 240)     # Light gray for hover
        self.border_color = (0, 0, 0)          # Black border
        self.text_color = (0, 0, 0)            # Black text
        
        # Font
        self.font = pygame.font.Font(None, 36)
        
    def draw(self, screen: pygame.Surface) -> None:
        # Draw button background
        color = self.hover_color if self.is_hovered else self.normal_color
        pygame.draw.rect(screen, color, self.rect)
        
        # Button border
        pygame.draw.rect(screen, self.border_color, self.rect, 2)
        
        # Button text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            # Update hover state
            self.is_hovered = self.rect.collidepoint(event.pos)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.is_clicked = True
                return False
                
        elif event.type == pygame.MOUSEBUTTONUP:
            was_clicked = self.is_clicked and self.rect.collidepoint(event.pos)
            self.is_clicked = False
            return was_clicked
            
        return False
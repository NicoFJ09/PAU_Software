import pygame
from utils.screen_config import PYGAME_CONFIG, COLORS

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = COLORS['GRAY']
        self.hover_color = (150, 150, 150)
        self.click_color = (100, 100, 100)
        self.current_color = self.color
        self.text = text
        self.font = pygame.font.SysFont(PYGAME_CONFIG['font']['name'], 32)
        self.is_hovered = False
        self.was_clicked = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            self.current_color = self.hover_color if self.is_hovered else self.color
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.was_clicked = True
                self.current_color = self.click_color
                return True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            self.current_color = self.hover_color if self.is_hovered else self.color
            
        return False
    
    def reset_click(self):
        self.was_clicked = False
                
    def draw(self, surface):
        pygame.draw.rect(surface, self.current_color, self.rect)
        text_surface = self.font.render(self.text, True, COLORS['BLACK'])
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
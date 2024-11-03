import pygame
from utils.screen_config import PYGAME_CONFIG, COLORS

class InputBox:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = COLORS['GRAY']
        self.text = ''
        self.active = False
        self.cursor_position = 0
        self.cursor_visible = True
        self.cursor_timer = 0
        self.font = pygame.font.SysFont(PYGAME_CONFIG['font']['name'], 28)
        self.text_offset = 0  # Para desplazamiento horizontal
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            if self.active:
                # Calcular posición del cursor basado en click
                self.cursor_position = len(self.text)
                
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                if self.cursor_position > 0:
                    self.text = self.text[:self.cursor_position-1] + self.text[self.cursor_position:]
                    self.cursor_position -= 1
            elif event.key == pygame.K_LEFT:
                self.cursor_position = max(0, self.cursor_position - 1)
            elif event.key == pygame.K_RIGHT:
                self.cursor_position = min(len(self.text), self.cursor_position + 1)
            else:
                self.text = self.text[:self.cursor_position] + event.unicode + self.text[self.cursor_position:]
                self.cursor_position += 1
                
    def draw(self, surface):
        # Renderizar texto
        txt_surface = self.font.render(self.text, True, COLORS['BLACK'])
        
        # Calcular offset para mantener el cursor visible
        cursor_x = self.font.size(self.text[:self.cursor_position])[0]
        if cursor_x - self.text_offset > self.rect.width - 10:
            self.text_offset = cursor_x - self.rect.width + 10
        elif cursor_x - self.text_offset < 0:
            self.text_offset = cursor_x
            
        # Dibujar texto con offset
        text_rect = pygame.Rect(self.rect.x + 5, self.rect.y + 5, 
                              self.rect.width - 10, self.rect.height - 10)
        surface.set_clip(text_rect)
        surface.blit(txt_surface, (self.rect.x + 5 - self.text_offset, self.rect.y + 5))
        
        # Dibujar cursor parpadeante
        if self.active:
            self.cursor_timer += 1
            if self.cursor_timer // 30 % 2 == 0:  # Parpadeo cada 30 frames
                cursor_pos = (self.rect.x + 5 + cursor_x - self.text_offset, self.rect.y + 5)
                pygame.draw.line(surface, 
                               COLORS['BLACK'],
                               cursor_pos,
                               (cursor_pos[0], cursor_pos[1] + self.font.get_height()),
                               2)
        
        surface.set_clip(None)
        # Borde del input box
        pygame.draw.rect(surface, self.color, self.rect, 2)

    def get_text(self):
        """Obtener el texto actual del input box"""
        return self.text
    
    def clear(self):
        """Limpiar el texto del input box"""
        self.text = ''
        self.cursor_position = 0
        self.text_offset = 0

# FILE: ScrollBar.py

import os
import sys

# Obtener la ruta absoluta del directorio raíz del proyecto
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(PROJECT_ROOT)

import pygame
from Admin_Dashboard.constants import COLORS

class Scrollbar:
    def __init__(self, x, y, width, height, total_items, visible_items):
        self.x = x
        self.y = y
        self.width = 10  # Ancho reducido
        self.height = height
        self.total_items = total_items
        self.visible_items = visible_items
        self.thumb_height = (visible_items / total_items) * height if total_items > visible_items else height
        self.thumb_y = y
        self.is_dragging = False
        self.drag_offset = 0
        
    def draw(self, surface):
        # Fondo del scrollbar con bordes redondeados
        pygame.draw.rect(
            surface, 
            COLORS['WHITE'], 
            (self.x, self.y, self.width, self.height),
            border_radius=5
        )
        
        # Thumb con bordes redondeados y más estilizado
        pygame.draw.rect(
            surface, 
            COLORS['YELLOW'], 
            (self.x, self.thumb_y, self.width, self.thumb_height),
            border_radius=5
        )
        
        # Borde decorativo opcional
        pygame.draw.rect(
            surface, 
            COLORS['YELLOW'], 
            (self.x, self.y, self.width, self.height),
            width=1,  # Solo el borde
            border_radius=5
        )

    def handle_event(self, event):
        # Manejar scroll del mouse
        if event.type == pygame.MOUSEWHEEL:
            scroll_amount = -event.y  # Invertir dirección
            current_percentage = (self.thumb_y - self.y) / (self.height - self.thumb_height)
            scroll_step = 1 / (self.total_items - self.visible_items)
            new_percentage = max(0, min(1, current_percentage + (scroll_step * scroll_amount)))
            self.set_scroll_position(new_percentage)
            return self.get_scroll_index()
            
        # Manejar arrastre del scrollbar
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if (self.x <= mouse_pos[0] <= self.x + self.width and 
                self.thumb_y <= mouse_pos[1] <= self.thumb_y + self.thumb_height):
                self.is_dragging = True
                self.drag_offset = mouse_pos[1] - self.thumb_y
                return self.get_scroll_index()
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_dragging = False
        
        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            mouse_pos = pygame.mouse.get_pos()
            new_y = mouse_pos[1] - self.drag_offset
            self.thumb_y = max(self.y, min(new_y, self.y + self.height - self.thumb_height))
            return self.get_scroll_index()
            
        return None
    
    def set_scroll_position(self, percentage):
        """Establece la posición del scrollbar basada en un porcentaje (0-1)"""
        self.thumb_y = self.y + (self.height - self.thumb_height) * percentage
    
    def get_scroll_index(self):
        scroll_percentage = (self.thumb_y - self.y) / (self.height - self.thumb_height)
        return int(scroll_percentage * (self.total_items - self.visible_items))
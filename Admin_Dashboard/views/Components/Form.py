import pygame
from utils.screen_config import PYGAME_CONFIG, COLORS
from .Button import Button
from .Input_box import InputBox

class Form:
    def __init__(self, x, y, width, height, fields):
        self.rect = pygame.Rect(x, y, width, height)
        self.input_boxes = []
        self.labels = []
        self.font = pygame.font.Font(None, 32)
        
        # Configuración del layout
        field_width = 150
        field_height = 30
        padding = 20
        items_per_row = 2
        
        # Calcular el ancho total de un conjunto de elementos
        item_set_width = field_width + padding * 2
        
        for i, field in enumerate(fields):
            # Calcular posición en la cuadrícula
            row = i // items_per_row
            col = i % items_per_row
            base_x = self.rect.left + (col * item_set_width)
            base_y = self.rect.top + (row * (field_height + padding * 2))
            
            # Crear etiqueta
            label = self.font.render(field, True, COLORS['BLACK'])
            label_rect = label.get_rect(topleft=(base_x, base_y))
            self.labels.append((label, label_rect))
            
            # Crear caja de entrada
            input_box = InputBox(base_x, base_y + 25, field_width, field_height)
            self.input_boxes.append(input_box)
        
        # Crear un único botón centrado debajo de los campos
        last_row = (len(fields) - 1) // items_per_row
        button_y = self.rect.top + (last_row + 1) * (field_height + padding * 2) + padding
        self.submit_button = Button(
            self.rect.centerx - 50,
            button_y,
            100,
            field_height,
            "Add"
        )

    def handle_event(self, event):
        # Manejar inputs
        for input_box in self.input_boxes:
            input_box.handle_event(event)
        
        # Manejar botón
        if self.submit_button.handle_event(event):
            values = [box.get_text() for box in self.input_boxes]
            # Limpiar inputs después de obtener valores
            for box in self.input_boxes:
                box.clear()
            return values
        return None

    def draw(self, surface):
        for label, rect in self.labels:
            surface.blit(label, rect)
        for input_box in self.input_boxes:
            input_box.draw(surface)
        self.submit_button.draw(surface)

    def get_height(self):
        """Calcula la altura total necesaria para el formulario"""
        if not self.labels:
            return 0
        items_per_row = 2
        rows = (len(self.labels) + items_per_row - 1) // items_per_row
        return (rows + 1) * (30 + 20 * 2)  # +1 para el botón
# FILE: components/container.py

import pygame
import pygame_gui
from Admin_Dashboard.constants import COLORS

class Container:
    def __init__(self, surface, ui_manager, position, width, config=None):
        self.surface = surface
        self.ui_manager = ui_manager
        self.x, self.y = position
        self.width = width
        
        # Configuración por defecto
        self.config = {
            'row_height': 40,
            'spacing': 10,
            'show_input': True,
            'show_button': True,
            'show_dividers': True,
            'input_width': 100,
            'button_width': 80,
            'button_text': 'Order',
            'text_formatter': lambda item: f"{item['nombre']} ({item['unidadMedida']})",
            'item_id_field': 'codigoProducto',
            'margin_top': 20,  # Márgenes ajustados
            'margin_bottom': 20
        }
        if config:
            self.config.update(config)
        
        self.content_font = pygame.font.SysFont("Georgia", 18)
        self.rows = []

    def create_row(self, item, index):
        """Crea una fila con elementos configurables"""
        # Calcular posición Y con margen superior
        y_pos = self.y + self.config['margin_top'] + (index * (self.config['row_height'] + self.config['spacing']))
        row_data = {}
        
        # Texto del item - centrado verticalmente en la fila
        text = self.config['text_formatter'](item)
        text_surface = self.content_font.render(text, True, COLORS['YELLOW'])
        text_rect = text_surface.get_rect(
            topleft=(self.x + 20, y_pos + (self.config['row_height'] - text_surface.get_height()) // 2)
        )
        row_data.update({
            'text': text_surface,
            'text_rect': text_rect,
            'item_id': item[self.config['item_id_field']]
        })
        
        # Input box (opcional)
        if self.config['show_input']:
            input_rect = pygame.Rect(
                self.x + self.width - self.config['button_width'] - self.config['input_width'] - 40,
                y_pos,
                self.config['input_width'],
                self.config['row_height']
            )
            input_box = pygame_gui.elements.UITextEntryLine(
                relative_rect=input_rect,
                manager=self.ui_manager,
                initial_text="0"
            )
            input_box.set_allowed_characters('numbers')
            input_box.set_text_length_limit(5)
            row_data['input'] = input_box
        
        # Botón (opcional)
        if self.config['show_button']:
            button_rect = pygame.Rect(
                self.x + self.width - self.config['button_width'] - 20,
                y_pos,
                self.config['button_width'],
                self.config['row_height']
            )
            button = pygame_gui.elements.UIButton(
                relative_rect=button_rect,
                text=self.config['button_text'],
                manager=self.ui_manager
            )
            row_data['button'] = button
        
        return row_data

    def setup_rows(self, items):
        """Configura todas las filas y ajusta la altura del contenedor"""
        self.rows = [
            self.create_row(item, i) 
            for i, item in enumerate(items)
        ]
        
        # Calcular altura total del contenedor incluyendo márgenes
        if len(self.rows) > 0:
            self.height = (
                self.config['margin_top'] +  # Margen superior
                (len(self.rows) * self.config['row_height']) +  # Altura de todas las filas
                ((len(self.rows) - 1) * self.config['spacing']) +  # Espaciado entre filas
                self.config['margin_bottom']  # Margen inferior
            )
        else:
            self.height = self.config['margin_top'] + self.config['margin_bottom']

    def draw_dividers(self):
        """Dibuja líneas divisorias centradas entre las filas"""
        if not self.config['show_dividers'] or len(self.rows) <= 1:
            return
            
        for i in range(len(self.rows) - 1):
            # Calcular posición Y del elemento actual y siguiente
            current_row_y = self.rows[i]['text_rect'].bottom
            next_row_y = self.rows[i + 1]['text_rect'].top
            
            # Calcular punto medio entre filas
            mid_y = (current_row_y + next_row_y) // 2
            
            # Dibujar línea divisoria
            pygame.draw.line(
                self.surface,
                COLORS['RED'],
                (self.x, mid_y),           # Punto inicial en x del contenedor
                (self.x + self.width-1, mid_y), # Punto final en x del contenedor
                2                          # Grosor igual al borde
            )

    def draw(self):
        """Dibuja el contenedor y sus elementos"""
        # Contenedor y borde
        pygame.draw.rect(
            self.surface,
            COLORS['GREEN'],
            (self.x, self.y, self.width, self.height)
        )
        pygame.draw.rect(
            self.surface,
            COLORS['RED'],
            (self.x, self.y, self.width, self.height),
            2
        )
        
        # Filas
        for row in self.rows:
            self.surface.blit(row['text'], row['text_rect'])

        # Líneas divisorias
        self.draw_dividers()

    def handle_event(self, event, callback):
        """Maneja eventos si hay botones configurados"""
        if not self.config['show_button']:
            return
            
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                for row in self.rows:
                    if event.ui_element == row['button']:
                        if self.config['show_input']:
                            amount = int(row['input'].get_text() or "0")
                            if amount > 0:
                                callback(row['item_id'], amount)
                                row['input'].set_text("0")
                        else:
                            callback(row['item_id'])
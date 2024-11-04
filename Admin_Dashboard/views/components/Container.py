import pygame
import pygame_gui
from Admin_Dashboard.constants import COLORS
from Admin_Dashboard.views.components.ScrollBar import Scrollbar


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
            'margin_top': 20,
            'margin_bottom': 20,
            'visible_rows': 5 
        }
        if config:
            self.config.update(config)
        
        # Calcular altura inicial del contenedor
        self.height = (
            self.config['margin_top'] +
            (self.config['visible_rows'] * self.config['row_height']) +
            ((self.config['visible_rows'] - 1) * self.config['spacing']) +
            self.config['margin_bottom']
        )
        
        self.content_font = pygame.font.SysFont("Georgia", 18)
        self.rows = []
        self.scrollbar = None
        self.scroll_index = 0
        

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
        # Crear todas las filas
        self.rows = [
            self.create_row(item, i) 
            for i, item in enumerate(items)
        ]
        
        # Altura fija para las filas visibles
        self.height = (
            self.config['margin_top'] +
            (self.config['visible_rows'] * self.config['row_height']) +
            ((self.config['visible_rows'] - 1) * self.config['spacing']) +
            self.config['margin_bottom']
        )
        
        # Crear scrollbar si hay más filas que el límite visible
        if len(self.rows) > self.config['visible_rows']:
            self.scrollbar = Scrollbar(
                x=self.x + self.width - 20,
                y=self.y,
                width=20,
                height=self.height,
                total_items=len(self.rows),
                visible_items=self.config['visible_rows']
            )
            
            # Simular scroll inicial para forzar actualización
            self.scroll_index = 1
            self.update_visible_elements()
            self.scroll_index = 0
            self.update_visible_elements()

    def update_visible_elements(self):
        """Actualiza la visibilidad de los elementos según el scroll"""
        for i, row in enumerate(self.rows):
            y_pos = self.y + self.config['margin_top'] + ((i - self.scroll_index) * (self.config['row_height'] + self.config['spacing']))
            
            # Determinar si el elemento está visible
            is_visible = (y_pos >= self.y and 
                        y_pos + self.config['row_height'] <= self.y + self.height)
            
            # Actualizar visibilidad de elementos UI
            if 'input' in row:
                if is_visible:
                    row['input'].show()
                    row['input'].set_relative_position((
                        row['input'].relative_rect.x,
                        y_pos
                    ))
                else:
                    row['input'].hide()
                    
            if 'button' in row:
                if is_visible:
                    row['button'].show()
                    row['button'].set_relative_position((
                        row['button'].relative_rect.x,
                        y_pos
                    ))
                else:
                    row['button'].hide()

    def draw_dividers(self):
        """Dibuja líneas divisorias centradas entre las filas"""
        if not self.config['show_dividers'] or len(self.rows) <= 1:
            return
            
        visible_rows = self.rows[self.scroll_index:self.scroll_index + self.config['visible_rows']]
        for i in range(len(visible_rows) - 1):
            # Calcular posición Y del elemento actual y siguiente
            current_row_y = self.y + self.config['margin_top'] + (i + 1) * (self.config['row_height'] + self.config['spacing']) - self.config['spacing'] // 2
            
            # Dibujar línea divisoria
            pygame.draw.line(
                self.surface,
                COLORS['RED'],
                (self.x, current_row_y),
                (self.x + self.width - 1, current_row_y),
                2
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
        
        # Actualizar elementos visibles
        self.update_visible_elements()
        
        # Dibujar solo las filas visibles
        visible_rows = self.rows[self.scroll_index:self.scroll_index + self.config['visible_rows']]
        for i, row in enumerate(visible_rows):
            y_pos = self.y + self.config['margin_top'] + (i * (self.config['row_height'] + self.config['spacing']))
            
            # Solo dibujar si está dentro del contenedor
            if y_pos >= self.y and y_pos + self.config['row_height'] <= self.y + self.height:
                text_rect = row['text_rect'].copy()
                text_rect.y = y_pos + (self.config['row_height'] - row['text'].get_height()) // 2
                self.surface.blit(row['text'], text_rect)

        # Líneas divisorias
        self.draw_dividers()
        
        # Dibujar scrollbar si existe
        if self.scrollbar:
            self.scrollbar.draw(self.surface)

    def handle_event(self, event, callback):
        """Maneja eventos si hay botones configurados"""
        if self.scrollbar:
            new_index = self.scrollbar.handle_event(event)
            if new_index is not None:
                self.scroll_index = new_index
                return
        
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
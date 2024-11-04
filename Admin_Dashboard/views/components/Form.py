import pygame
import pygame_gui
from Admin_Dashboard.constants import COLORS

class Form:
    def __init__(self, container_bottom_y, ui_manager, surface, config=None):
        self.ui_manager = ui_manager
        self.surface = surface

        self.title_font = pygame.font.SysFont("Georgia", 45)  # Fuente grande para el encabezado
        self.content_font = pygame.font.SysFont("Georgia", 18)
        
        # Configuración por defecto
        self.config = {
            'width': 600,
            'height': 200,
            'margin_x': 50,
            'margin_top': 20,
            'margin_bottom': 20,
            'spacing': 10,
            'row_height': 40,
            'input_width': 150,
            'button_width': 100,
            'button_text': 'Añadir',
            'fields': [
                {'label': 'Campo 1', 'type': 'text'},
                {'label': 'Campo 2', 'type': 'text'},
                {'label': 'Campo 3', 'type': 'dropdown', 'options': ['Opción 1', 'Opción 2', 'Opción 3']}
            ]
        }
        
        if config:
            self.config.update(config)
        
        # Posición y dimensiones
        self.x = self.config['margin_x']
        self.y = container_bottom_y + self.config['margin_top']
        self.width = self.config['width']
        self.height = self.config['height']
        
        self.form_rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )
        
        # Crear elementos UI
        self.setup_form_elements()

    def setup_form_elements(self):
        self.fields = []
        field_spacing = (self.width - (3 * self.config['input_width'])) / 4
        
        # Crear encabezado
        header_surface = self.title_font.render("Añadir productos nuevos", True, COLORS['GREEN'])
        header_rect = header_surface.get_rect(center=(self.x + self.width // 2, self.y + 40))
        self.header = {'surface': header_surface, 'rect': header_rect}
        
        for i, field in enumerate(self.config['fields']):
            input_x = self.x + field_spacing + (i * (self.config['input_width'] + field_spacing))
            input_y = self.y + 100  # Ajustar para dejar espacio para el encabezado
            
            # Renderizar etiqueta
            label_surface = self.content_font.render(field['label'], True, COLORS['GREEN'])
            label_width = label_surface.get_width()
            label_x = input_x + (self.config['input_width'] - label_width) / 2
            label_y = input_y - 20
            label_rect = label_surface.get_rect(x=label_x, y=label_y)
            
            # Crear input o dropdown según el tipo
            if field['type'] == 'dropdown':
                input_element = pygame_gui.elements.UIDropDownMenu(
                    options_list=field['options'],
                    starting_option=field['options'][0],
                    relative_rect=pygame.Rect(input_x, input_y, self.config['input_width'], 30),
                    manager=self.ui_manager
                )
            else:
                input_element = pygame_gui.elements.UITextEntryLine(
                    relative_rect=pygame.Rect(input_x, input_y, self.config['input_width'], 30),
                    manager=self.ui_manager
                )
            
            self.fields.append({
                'label_surface': label_surface,
                'label_rect': label_rect,
                'input': input_element,
                'type': field['type']
            })
        
        # Botón configurable
        button_x = self.x + (self.width - self.config['button_width']) / 2
        button_y = self.y + self.height - 50
        
        self.submit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                button_x,
                button_y,
                self.config['button_width'],
                30
            ),
            text=self.config['button_text'],  # Usar texto del botón desde config
            manager=self.ui_manager
        )

    def get_values(self):
        values = []
        for field in self.fields:
            if field['type'] == 'dropdown':
                values.append(field['input'].selected_option[0])  # Extraer solo la cadena
            else:
                values.append(field['input'].get_text())
        return values

    def clear_inputs(self):
        for field in self.fields:
            if field['type'] == 'dropdown':
                field['input'].selected_option = field['input'].options_list[0]  # Resetear al primer valor
            else:
                field['input'].set_text("")  # Limpiar el texto

    def draw(self):
        # Dibujar fondo y borde del formulario
        pygame.draw.rect(self.surface, COLORS['WHITE'], self.form_rect)
        pygame.draw.rect(self.surface, COLORS['RED'], self.form_rect, 2)
        
        # Dibujar encabezado
        self.surface.blit(self.header['surface'], self.header['rect'])
        
        # Dibujar las etiquetas
        for field in self.fields:
            self.surface.blit(field['label_surface'], field['label_rect'])

    def update(self, time_delta):
        pass

    def handle_event(self, event, callback):
        """Maneja eventos si hay botones configurados"""
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.submit_button:
                    values = self.get_values()
                    callback(*values)
                    self.clear_inputs()
        return None
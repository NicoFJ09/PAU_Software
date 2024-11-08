import pygame
import pygame_gui
from Admin_Dashboard.constants import COLORS

class CraftForm:
    def __init__(self, container_bottom_y, ui_manager, surface, material=None, material_quantities=None, config=None):
        self.ui_manager = ui_manager
        self.surface = surface
        self.material = material
        self.material_quantities = material_quantities or {}

        self.title_font = pygame.font.SysFont("Georgia", 24)  # Fuente más pequeña para el encabezado
        self.content_font = pygame.font.SysFont("Georgia", 18)
        
        # Configuración por defecto
        self.config = {
            'width': 600,
            'height': 300,
            'margin_x': 50,
            'margin_top': 20,
            'margin_bottom': 20,
            'spacing': 10,
            'row_height': 40,
            'button_width': 100,
            'button_text': 'Fabricar',
            'Title_text': 'Craft Items',
            'material_text_formatter': lambda item, available: f"{item['Nombre']} ({item['unidadMedida']}): {item['cantidad']} | Disponible: {available['disponible']}{item['unidadMedida']}"
        }
        
        if config:
            self.config.update(config)
            
        if self.material:
            self.config['Title_text'] = f"Receta de {material['Nombre']}"
        
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
        
        # Inicializar el valor del contador
        self.counter_value = 0
        
        # Crear elementos UI solo si hay un elemento seleccionado
        if self.material:
            self.setup_form_elements()

    def setup_form_elements(self):
        # Crear encabezado
        header_surface = self.title_font.render(self.config['Title_text'], True, COLORS['GREEN'])
        header_rect = header_surface.get_rect(topleft=(self.x + 20, self.y + 20))
        self.header = {'surface': header_surface, 'rect': header_rect}
        
        # Crear lista de materiales si hay un elemento seleccionado
        self.materials = []
        if self.material and 'materiales' in self.material:
            start_y = self.y + 60  # Ajustar para dejar espacio para el encabezado
            for i, item in enumerate(self.material['materiales']):
                available = self.material_quantities.get(item['codigoProducto'], {'disponible': 0})
                item_text = self.config['material_text_formatter'](item, available)
                item_surface = self.content_font.render(item_text, True, COLORS['YELLOW'])
                item_rect = item_surface.get_rect(topleft=(self.x + 20, start_y + i * (self.config['row_height'] + self.config['spacing'])))
                self.materials.append({'surface': item_surface, 'rect': item_rect})
        
        # Crear contador con botones + y -
        counter_x = self.x + self.width - 150
        counter_y = self.y + 60
        
        self.decrement_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(counter_x, counter_y, 30, 30),
            text='-',
            manager=self.ui_manager
        )
        
        self.increment_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(counter_x + 70, counter_y, 30, 30),
            text='+',
            manager=self.ui_manager
        )
        
        self.counter_display = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(counter_x + 35, counter_y, 30, 30),
            text=str(self.counter_value),
            manager=self.ui_manager
        )
        
        # Botón configurable
        button_x = self.x + self.width - self.config['button_width'] - 50
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

    def destroy_form_elements(self):
        """Destruye los elementos UI existentes"""
        if hasattr(self, 'decrement_button'):
            self.decrement_button.kill()
        if hasattr(self, 'increment_button'):
            self.increment_button.kill()
        if hasattr(self, 'counter_display'):
            self.counter_display.kill()
        if hasattr(self, 'submit_button'):
            self.submit_button.kill()
        self.materials = []

    def get_values(self):
        return self.counter_value

    def clear_inputs(self):
        self.counter_value = 0
        self.counter_display.set_text(str(self.counter_value))

    def draw(self):
        # Dibujar fondo y borde del formulario
        pygame.draw.rect(self.surface, COLORS['WHITE'], self.form_rect)
        pygame.draw.rect(self.surface, COLORS['RED'], self.form_rect, 2)
        
        if not self.material:
            return
        
        # Dibujar encabezado
        self.surface.blit(self.header['surface'], self.header['rect'])
        
        # Dibujar la lista de materiales
        for item in self.materials:
            self.surface.blit(item['surface'], item['rect'])

    def update(self, time_delta):
        pass

    def handle_event(self, event, callback):
        if not self.material:
            return
        
        """Maneja eventos si hay botones configurados"""
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.submit_button:
                    counter_value = self.get_values()
                    print(f"Cantidad de productos a fabricar: {counter_value}")
                    callback(self.material, counter_value)
                    self.clear_inputs()
                elif event.ui_element == self.increment_button:
                    self.counter_value += 1
                    self.counter_display.set_text(str(self.counter_value))
                elif event.ui_element == self.decrement_button:
                    if self.counter_value > 0:
                        self.counter_value -= 1
                        self.counter_display.set_text(str(self.counter_value))
        return None

    def update_quantities(self, material_quantities=None):
        """Actualiza solo las cantidades sin recrear elementos UI"""
        if material_quantities:
            self.material_quantities = material_quantities

        # Actualizar solo las superficies de texto de los materiales
        if self.material and 'materiales' in self.material:
            self.materials = []
            start_y = self.y + 60
            for i, item in enumerate(self.material['materiales']):
                available = self.material_quantities.get(item['codigoProducto'], {'disponible': 0})
                item_text = self.config['material_text_formatter'](item, available)
                item_surface = self.content_font.render(item_text, True, COLORS['YELLOW'])
                item_rect = item_surface.get_rect(topleft=(self.x + 20, start_y + i * (self.config['row_height'] + self.config['spacing'])))
                self.materials.append({'surface': item_surface, 'rect': item_rect})
            
    def update_form(self, material=None, material_quantities=None, config=None):
        """Actualiza el formulario manteniendo elementos UI"""
        if material and material != self.material:
            # Solo destruir y recrear si cambia el material
            self.destroy_form_elements()
            self.material = material
            if config:
                self.config.update(config)
            self.setup_form_elements()
        elif material_quantities:
            # Si solo cambian las cantidades, actualizar sin recrear
            self.update_quantities(material_quantities)
        
        self.draw()
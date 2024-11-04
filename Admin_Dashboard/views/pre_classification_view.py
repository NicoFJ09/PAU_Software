# FILE: pre_classification_view.py

import pygame
import pygame_gui
from Admin_Dashboard.constants import COLORS
from Admin_Dashboard.controllers.Pre_clasification_controller import PreClassificationController
from Admin_Dashboard.views.components.Container import Container

class PreClassificationView:
    def __init__(self, surface, window_size):
        self.surface = surface
        self.window_size = window_size
        self.ui_manager = pygame_gui.UIManager(window_size)
        
        # Configuraciones iniciales
        self.setup_ui_theme()
        self.setup_fonts()
        
        # Controlador
        self.controller = PreClassificationController()
        
        # Configurar contenedor
        self.setup_container()

    def setup_container(self):
        """Configura el contenedor y sus productos"""
        container_config = {
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
            'margin_top': 5, 
            'margin_bottom': 5,
        }
        
        self.container = Container(
            surface=self.surface,
            ui_manager=self.ui_manager,
            position=(50, 100),
            width=self.window_size[0] - 100,  # Solo pasamos el ancho
            config=container_config
        )
        
        # Configurar productos
        products = self.controller.get_products()
        self.container.setup_rows(products)

    def setup_ui_theme(self):
        """Configura el tema de la interfaz"""
        self.default_theme = {
            "text_entry_line": {
                "colours": {
                    "dark_bg": "#FFFFFF",
                    "selected_bg": "#FFFFFF",
                    "normal_text": "#000000",
                    "selected_text": "#000000",
                    "border": "#B90518"
                }
            }
        }
        self.ui_manager.get_theme().load_theme(self.default_theme)

    def setup_fonts(self):
        """Configura las fuentes"""
        self.title_font = pygame.font.SysFont("Georgia", 45)

    def handle_event(self, event):
        """Maneja eventos de la vista"""
        self.ui_manager.process_events(event)
        self.container.handle_event(event, self.controller.order_product)

    def update(self):
        """Actualiza elementos de la UI"""
        time_delta = pygame.time.Clock().tick(60)/1000.0
        self.ui_manager.update(time_delta)

    def draw(self):
        """Dibuja todos los elementos de la vista"""
        # Fondo principal
        self.surface.fill(COLORS['WHITE'])
        
        # Título
        title_text = self.title_font.render("Pre-Classification Screen", True, COLORS['GREEN'])
        title_rect = title_text.get_rect(midtop=(self.window_size[0] // 2, 20))
        self.surface.blit(title_text, title_rect)
        
        # Contenedor y elementos UI
        self.container.draw()
        self.ui_manager.draw_ui(self.surface)
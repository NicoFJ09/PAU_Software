import pygame
import pygame_gui
from Admin_Dashboard.constants import PYGAME_CONFIG, COLORS
from Admin_Dashboard.controllers.Pre_clasification_controller import PreClassificationController

class PreClassificationView:

    # ------------------------
    # Constructor de la vista
    # ------------------------
    def __init__(self, surface, window_size):
        self.surface = surface
        self.window_size = window_size
        
        # UI Manager
        self.ui_manager = pygame_gui.UIManager(window_size)

        # Fuentes
        self.title_font = pygame.font.SysFont(
            PYGAME_CONFIG['font']['name'], 
            PYGAME_CONFIG['font']['size'] + 10
        )
        self.content_font = pygame.font.SysFont(
            PYGAME_CONFIG['font']['name'], 
            PYGAME_CONFIG['font']['size']
        )
        # Controlador
        self.controller = PreClassificationController()

        # Elementos UI
        self.setup_ui_elements()

    def setup_ui_elements(self):
        """Configuración inicial de elementos UI"""
        # Título
        self.title_text = self.title_font.render("Pre-Classification Screen", True, COLORS['BLACK'])
        self.title_rect = self.title_text.get_rect(midtop=(self.window_size[0] // 2, 20))
        
        # Área de contenido principal
        self.content_area = pygame.Rect(
            50, 100,
            self.window_size[0] - 100,
            200
        )
        
        # Botones
        button_width = 150
        button_height = 40
        spacing = 20
        
        self.add_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.content_area.right - button_width - spacing,
                 self.content_area.bottom + spacing),
                (button_width, button_height)
            ),
            text='Add Product',
            manager=self.ui_manager
        )

    # ------------------------a
    # Manejo de eventos
    # ------------------------
    def handle_event(self, event):
        pass
    # ------------------------
    # Muestra la vista
    # ------------------------
    def draw(self):
        # Fondo
        self.surface.fill(COLORS['WHITE'])
        
        # Título
        self.surface.blit(self.title_text, self.title_rect)
        
        # Área de contenido
        pygame.draw.rect(self.surface, COLORS['GRAY'], self.content_area, 2)
        
        # Elementos UI
        self.ui_manager.draw_ui(self.surface)
    # ------------------------
    # Actualizaciones según eventos
    # ------------------------
    def update(self):
        pass
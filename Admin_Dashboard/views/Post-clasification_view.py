import pygame
import pygame_gui
from Admin_Dashboard.constants import PYGAME_CONFIG, COLORS
from Admin_Dashboard.controllers.Post_clasification_controller import PostClassificationController

class PostClassificationView:

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
        self.controller = PostClassificationController()

    # ------------------------a
    # Manejo de eventos
    # ------------------------
    def handle_event(self, event):
        pass
    # ------------------------
    # Muestra la vista
    # ------------------------
    def draw(self):
        self.surface.fill(COLORS['WHITE'])
    # ------------------------
    # Actualizaciones según eventos
    # ------------------------
    def update(self):
        pass
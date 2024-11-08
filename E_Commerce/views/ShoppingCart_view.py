import pygame
import pygame_gui
from Admin_Dashboard.constants import COLORS
from E_Commerce.Screens_web import Screens

class ShoppingCartView:
    def __init__(self, window, change_screen_callback):
        pygame.init()
        self.change_screen_callback = change_screen_callback
        self.ancho, self.alto = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.window = window

        # Crear el administrador de la interfaz
        self.manager = pygame_gui.UIManager((self.ancho, self.alto - 50))

        self.clock = pygame.time.Clock()

    def handle_event(self, event):
        """Maneja eventos de la vista"""
        self.manager.process_events(event)
        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            pass

    def update(self):
        """Actualiza elementos de la UI"""
        time_delta = self.clock.tick(60) / 1000.0
        self.manager.update(time_delta)

    def draw(self):
        """Dibuja todos los elementos de la vista"""
        self.window.fill(COLORS['WHITE'])

        # Dibujar la interfaz de usuario
        self.manager.draw_ui(self.window)
        pygame.display.flip()
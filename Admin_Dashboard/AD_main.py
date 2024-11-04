import os
import sys
import pygame
from enum import Enum

from Admin_Dashboard.views.pre_classification_view import PreClassificationView
class Screens(Enum):
    PRE_CLASSIFICATION = "pre_classification"

class AdminDashboard:
    def __init__(self):
        pygame.init()
        self.window_size = (1280, 720)
        self.window_surface = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Admin Dashboard")
        
        self.clock = pygame.time.Clock()
        self.is_running = True
        
        self.current_screen = Screens.PRE_CLASSIFICATION
        self.views = {
            Screens.PRE_CLASSIFICATION: PreClassificationView(
                self.window_surface, 
                self.window_size
            )
        }

    def run(self):
        """Bucle principal de la aplicación"""
        while self.is_running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                self.views[self.current_screen].handle_event(event)
            
            self.views[self.current_screen].update()
            self.views[self.current_screen].draw()
            pygame.display.flip()

# Función para ser llamada desde main.py
def main():
    dashboard = AdminDashboard()
    dashboard.run()
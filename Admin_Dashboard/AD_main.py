import pygame
from Admin_Dashboard.Screens import Screens  # Importar Screens desde el nuevo módulo
from Admin_Dashboard.views.Pre_classification_view import PreClassificationView
from Admin_Dashboard.views.Classification_view import ClassificationView
from Admin_Dashboard.views.Recipe_creator_view import RecipeCreatorView
from Admin_Dashboard.views.Factory_view import FactoryView
from Admin_Dashboard.views.Preview_view import PreviewView


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
            Screens.PRE_CLASSIFICATION: PreClassificationView,
            Screens.CLASSIFICATION: ClassificationView,
            Screens.RECIPE_CREATOR: RecipeCreatorView,
            Screens.FACTORY: FactoryView,
            Screens.PREVIEW: PreviewView
        }
        self.current_view = self.views[self.current_screen](
            self.window_surface, 
            self.window_size,
            self.change_screen  # Pasar el callback para cambiar la pantalla
        )

    def change_screen(self, new_screen):
        """Cambia la pantalla al nuevo estado"""
        self.current_screen = new_screen
        self.current_view = self.views[self.current_screen](
            self.window_surface, 
            self.window_size,
            self.change_screen  # Pasar el callback para cambiar la pantalla
        )

    def run(self):
        """Bucle principal de la aplicación"""
        while self.is_running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                self.current_view.handle_event(event)
            
            self.current_view.update()
            self.current_view.draw()
            pygame.display.flip()

# Función para ser llamada desde main.py
def main():
    dashboard = AdminDashboard()
    dashboard.run()
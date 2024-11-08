import pygame
from E_Commerce.Screens_web import Screens  # Importar Screens desde el nuevo módulo
from E_Commerce.views.Sign_In_view import SignInView
from E_Commerce.views.Register_view import RegisterView
from E_Commerce.views.HomePage_view import HomePageView
from E_Commerce.views.ShoppingCart_view import ShoppingCartView


class ECommerce:
    def __init__(self):
        pygame.init()
        # Obtener las dimensiones de la pantalla
        self.window_size =(1280, 900)
        # Crear la ventana
        self.window_surface = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("E-Commerce")

        self.clock = pygame.time.Clock()
        self.is_running = True

        self.current_screen = Screens.SIGN_IN
        self.views = {
            Screens.SIGN_IN: SignInView,
            Screens.REGISTER: RegisterView,
            Screens.HOMEPAGE: HomePageView,
            Screens.SHOPPING_CART: ShoppingCartView,
        }
        self.current_view = self.views[self.current_screen](
            self.window_surface,
            self.change_screen  # Pasar el callback para cambiar la pantalla
        )

    def change_screen(self, new_screen):
        """Cambia la pantalla al nuevo estado"""
        self.current_screen = new_screen
        self.current_view = self.views[self.current_screen](
            self.window_surface,
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
    web = ECommerce()
    web.run()
import pygame
from E_Commerce.Screens_web import Screens  # Importar Screens desde el nuevo módulo
from E_Commerce.views.Sign_In_view import SignInView
from E_Commerce.views.Register_view import RegisterView
from E_Commerce.views.HomePage_view import HomePageView
from E_Commerce.views.ShoppingCart_view import ShoppingCartView
from E_Commerce.views.Payment_view import PaymentView
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

        # Configuración de la pantalla inicial y las vistas
        self.current_screen = Screens.SIGN_IN
        self.views = {
            Screens.SIGN_IN: SignInView,
            Screens.REGISTER: RegisterView,
            Screens.HOMEPAGE: HomePageView,
            Screens.SHOPPING_CART: ShoppingCartView,
            Screens.PAYMENT : PaymentView,
        }
        self.current_view = self.views[self.current_screen](
            self.window_surface, 
            self.window_size,
            self.change_screen  # Pasar el callback para cambiar la pantalla
        )

    def change_screen(self, new_screen, cartProducts=None, Products=None, totalprice=None):
        """Cambia la pantalla al nuevo estado"""
        self.current_screen = new_screen
        if new_screen == Screens.SHOPPING_CART:
            self.current_view = self.views[self.current_screen](
                self.window_surface,
                self.window_size,
                self.change_screen,
                cartProducts,
                Products
            )
        elif new_screen == Screens.PAYMENT:
            self.current_view = self.views[self.current_screen](
                self.window_surface,
                self.window_size,
                self.change_screen,
                totalprice
            )
        else:
            self.current_view = self.views[self.current_screen](
                self.window_surface,
                self.window_size, 
                self.change_screen  # Callback para cambiar la pantalla
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

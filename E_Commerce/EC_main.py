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
        self.ancho, self.alto = pygame.display.Info().current_w, pygame.display.Info().current_h
        # Crear la ventana
        self.window = pygame.display.set_mode((self.ancho, self.alto - 50))
        pygame.display.set_caption("")

        self.clock = pygame.time.Clock()
        self.is_running = True

        # Configuración de la pantalla inicial y las vistas
        self.current_screen = Screens.SIGN_IN
        self.views = {
            Screens.SIGN_IN: SignInView,
            Screens.REGISTER: RegisterView,
            Screens.HOMEPAGE: HomePageView,
            Screens.SHOPPING_CART: ShoppingCartView,
        }

        # Inicializa la vista actual
        self.set_current_view(self.current_screen)

    def set_current_view(self, screen):
        """Configura la vista actual según la pantalla seleccionada"""
        if screen == Screens.SHOPPING_CART:
            # Si es ShoppingCartView, pasa el argumento `surface` adicional
            self.current_view = ShoppingCartView(
                self.window,
                (self.ancho, self.alto - 50),
                self.change_screen
            )
        else:
            # Para otras vistas, pasa solo `self.window` y `self.change_screen`
            self.current_view = self.views[screen](
                self.window,
                self.change_screen
            )

    def change_screen(self, new_screen):
        """Cambia la pantalla al nuevo estado"""
        self.current_screen = new_screen
        self.set_current_view(new_screen)  # Llama a la función para cambiar la vista

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

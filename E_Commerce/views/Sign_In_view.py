import pygame
import pygame_gui
from Admin_Dashboard.constants import COLORS
from E_Commerce.Screens_web import Screens

class SignInView:
    def __init__(self, surface, window_size, change_screen_callback):
        self.surface = surface
        self.window_size = window_size
        self.ui_manager = pygame_gui.UIManager(window_size)
        self.change_screen_callback = change_screen_callback

        # Configuración de fuentes
        self.fuente = pygame.font.SysFont("Georgia", 18)
        self.fuente2 = pygame.font.SysFont("Georgia", 9)

        # Cargar la imagen del logo
        self.logo_image = pygame.image.load("images/logo.png")
        self.logo_image = pygame.transform.scale(self.logo_image, (100, 100))

        # Definir etiquetas de texto
        self.inicio_label = self.fuente.render("Iniciar sesión para continuar", True, COLORS['RED'])
        self.cuenta_label = self.fuente.render("¿No tiene una cuenta?", True, COLORS['RED'])
        self.restricciones_label = self.fuente2.render(
            "*Algunas funciones solo están disponibles para usuarios registrados", True, COLORS['RED']
        )

        # Configurar posiciones y tamaños usando window_size
        self.rect_ancho = self.window_size[0] // 3
        self.rect_alto = int(self.window_size[1] * 0.8)
        self.rect_x = (self.window_size[0] - self.rect_ancho) // 2
        self.rect_y = (self.window_size[1] - self.rect_alto) // 2 - 35

        self.setup_ui_elements()
        self.clock = pygame.time.Clock()

    def setup_ui_elements(self):
        # Calcular la posición de los textos
        self.text1_x = self.rect_x + (self.rect_ancho - self.inicio_label.get_width()) // 2
        self.text1_y = self.rect_y + 140
        self.text2_x = self.rect_x + (self.rect_ancho - self.cuenta_label.get_width()) // 2
        self.text2_y = self.rect_y + 375
        self.text3_x = self.rect_x + (self.rect_ancho - self.restricciones_label.get_width()) // 2
        self.text3_y = self.rect_y + 480

        # Crear campos de texto para correo y contraseña
        self.entrada_correo = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(
                (self.rect_x + (self.rect_ancho // 6), self.text1_y + 55), 
                (self.rect_ancho * 2 // 3, 30)
            ),
            manager=self.ui_manager
        )
        self.configurar_entrada(self.entrada_correo, "Ingresar correo electrónico")

        self.entrada_password = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(
                (self.rect_x + (self.rect_ancho // 6), self.text1_y + 95), 
                (self.rect_ancho * 2 // 3, 30)
            ),
            manager=self.ui_manager
        )
        self.configurar_entrada(self.entrada_password, "Contraseña")

        # Crear botones
        self.boton_continuar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.rect_x + (self.rect_ancho // 6), self.text1_y + 145),
                (self.rect_ancho * 2 // 3, 40)
            ),
            text="Continuar",
            manager=self.ui_manager
        )

        self.create_account_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.rect_x + (self.rect_ancho // 6), self.text1_y + 270),
                (self.rect_ancho * 2 // 3, 40)
            ),
            text="Crear cuenta",
            manager=self.ui_manager
        )

        self.ingresar_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.rect_x + (self.rect_ancho // 6), self.text1_y + 355),
                (self.rect_ancho * 2 // 3, 40)
            ),
            text="Ingresar sin cuenta",
            manager=self.ui_manager
        )

    def configurar_entrada(self, entrada, placeholder_text):
        entrada.placeholder_text = placeholder_text
        entrada.set_text("")
        entrada.background_colour = pygame.Color(COLORS['WHITE'])
        entrada.border_colour = pygame.Color(COLORS['YELLOW'])
        entrada.text_colour = pygame.Color(0, 0, 0)
        entrada.rebuild()

    def handle_event(self, event):
        """Maneja eventos de la vista"""
        self.ui_manager.process_events(event)
        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.ingresar_button:
                self.change_screen_callback(Screens.HOMEPAGE)
            elif event.ui_element == self.boton_continuar:
                self.change_screen_callback(Screens.HOMEPAGE)
            elif event.ui_element == self.create_account_button:
                self.change_screen_callback(Screens.REGISTER)

    def update(self):
        """Actualiza elementos de la UI"""
        time_delta = self.clock.tick(60) / 1000.0
        self.ui_manager.update(time_delta)

    def draw(self):
        """Dibuja todos los elementos de la vista"""
        self.surface.fill(COLORS['GREEN'])
        pygame.draw.rect(self.surface, COLORS['WHITE'],
                        (self.rect_x, self.rect_y, self.rect_ancho, self.rect_alto))

        # Dibujar la imagen del logo
        logo_x = self.rect_x + (self.rect_ancho - self.logo_image.get_width()) // 2
        logo_y = self.rect_y + 30
        self.surface.blit(self.logo_image, (logo_x, logo_y))

        # Dibujar las etiquetas de texto
        self.surface.blit(self.inicio_label, (self.text1_x, self.text1_y))
        self.surface.blit(self.cuenta_label, (self.text2_x, self.text2_y))
        self.surface.blit(self.restricciones_label, (self.text3_x, self.text3_y))

        # Dibujar la interfaz de usuario
        self.ui_manager.draw_ui(self.surface)
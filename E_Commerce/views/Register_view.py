import pygame
import pygame_gui
from E_Commerce.Screens_web import Screens
from E_Commerce.constants import COLORS

class RegisterView:
    def __init__(self, window, change_screen_callback):
        pygame.init()
        self.change_screen_callback = change_screen_callback
        self.ancho, self.alto = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.window = window

        # Crear el administrador de la interfaz
        self.manager = pygame_gui.UIManager((self.ancho, self.alto - 50))

        # Configuración de fuente
        self.fuente = pygame.font.SysFont("Georgia", 18)

        # Cargar la imagen del logo
        self.logo_image = pygame.image.load("images/logo.png")
        self.logo_image = pygame.transform.scale(self.logo_image, (85, 85))

        # Configurar etiqueta de texto
        self.crear_cuenta_label = self.fuente.render("Crear cuenta nueva", True, COLORS['RED'])

        # Definir posiciones y tamaños
        self.rect_ancho = self.ancho // 3
        self.rect_alto = int(self.alto * 0.8)
        self.rect_x = (self.ancho - self.rect_ancho) // 2
        self.rect_y = (self.alto - self.rect_alto) // 2 - 35

        self.setup_ui_elements()
        self.clock = pygame.time.Clock()

    def setup_ui_elements(self):
        # Posición del texto
        self.crear_x = self.rect_x + (self.rect_ancho - self.crear_cuenta_label.get_width()) // 2
        self.crear_y = self.rect_y + 110

        # Crear campos de entrada para nombre, correo, contraseña y teléfono
        self.entrada_nombre = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(
                (self.rect_x + (self.rect_ancho // 6), self.crear_y + 60),
                (self.rect_ancho * 2 // 3, 30)),
            manager=self.manager
        )
        self.configurar_entrada(self.entrada_nombre, "Nombre")

        self.entrada_correo = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(
                (self.rect_x + (self.rect_ancho // 6), self.crear_y + 130),
                (self.rect_ancho * 2 // 3, 30)),
            manager=self.manager
        )
        self.configurar_entrada(self.entrada_correo, "Correo electrónico")

        self.entrada_password = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(
                (self.rect_x + (self.rect_ancho // 6), self.crear_y + 200),
                (self.rect_ancho * 2 // 3, 30)),
            manager=self.manager
        )
        self.configurar_entrada(self.entrada_password, "Contraseña")

        self.entrada_telefono = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(
                (self.rect_x + (self.rect_ancho // 6), self.crear_y + 270),
                (self.rect_ancho * 2 // 3, 30)),
            manager=self.manager
        )
        self.configurar_entrada(self.entrada_telefono, "Número telefónico")

        # Botón de confirmación
        self.confirmar_crear = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.rect_x + (self.rect_ancho // 6), self.crear_y + 355),
                (self.rect_ancho * 2 // 3, 40)),
            text="Confirmar",
            manager=self.manager
        )

    def configurar_entrada(self, entrada, placeholder_text):
        """Configura cada entrada de texto"""
        entrada.placeholder_text = placeholder_text
        entrada.set_text("")
        entrada.background_colour = pygame.Color(COLORS['WHITE'])
        entrada.border_colour = pygame.Color(COLORS['YELLOW'])
        entrada.text_colour = pygame.Color(0, 0, 0)
        entrada.rebuild()

    def handle_event(self, event):
        """Maneja eventos de la vista"""
        self.manager.process_events(event)
        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.confirmar_crear:
                self.change_screen_callback(Screens.HOMEPAGE)  # Llamada de cambio de pantalla

    def update(self):
        """Actualiza los elementos de la UI"""
        time_delta = self.clock.tick(60) / 1000.0
        self.manager.update(time_delta)

    def draw(self):
        """Dibuja todos los elementos de la vista"""
        self.window.fill(COLORS['GREEN'])
        pygame.draw.rect(self.window, (COLORS['WHITE']), (self.rect_x, self.rect_y, self.rect_ancho, self.rect_alto))

        # Dibujar la imagen del logo
        logo_x = self.rect_x + (self.rect_ancho - self.logo_image.get_width()) // 2
        logo_y = self.rect_y + 20
        self.window.blit(self.logo_image, (logo_x, logo_y))

        # Dibujar etiquetas de texto
        self.window.blit(self.crear_cuenta_label, (self.crear_x, self.crear_y + 10))

        # Dibujar la interfaz de usuario
        self.manager.draw_ui(self.window)
        pygame.display.flip()

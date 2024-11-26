import pygame
import pygame_gui
import re
from E_Commerce.Screens_web import Screens
from E_Commerce.constants import COLORS

class RegisterView:
    def __init__(self, surface, window_size, change_screen_callback):
        self.surface = surface
        self.window_size = window_size
        self.ui_manager = pygame_gui.UIManager(window_size)
        self.change_screen_callback = change_screen_callback

        # Configuración de fuente
        self.fuente = pygame.font.SysFont("Georgia", 18)

        # Cargar la imagen del logo
        self.logo_image = pygame.image.load("images/logo.png")
        self.logo_image = pygame.transform.scale(self.logo_image, (85, 85))

        # Configurar etiqueta de texto
        self.crear_cuenta_label = self.fuente.render("Crear cuenta nueva", True, COLORS['RED'])

        # Definir posiciones y tamaños usando window_size
        self.rect_ancho = self.window_size[0] // 3
        self.rect_alto = int(self.window_size[1] * 0.8)
        self.rect_x = (self.window_size[0] - self.rect_ancho) // 2
        self.rect_y = (self.window_size[1] - self.rect_alto) // 2 - 35

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
            manager=self.ui_manager
        )
        self.configurar_entrada(self.entrada_nombre, "Nombre")

        self.entrada_correo = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(
                (self.rect_x + (self.rect_ancho // 6), self.crear_y + 130),
                (self.rect_ancho * 2 // 3, 30)),
            manager=self.ui_manager
        )
        self.configurar_entrada(self.entrada_correo, "Correo electrónico")

        self.entrada_password = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(
                (self.rect_x + (self.rect_ancho // 6), self.crear_y + 200),
                (self.rect_ancho * 2 // 3, 30)),
            manager=self.ui_manager
        )
        self.configurar_entrada(self.entrada_password, "Contraseña")

        self.entrada_telefono = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(
                (self.rect_x + (self.rect_ancho // 6), self.crear_y + 270),
                (self.rect_ancho * 2 // 3, 30)),
            manager=self.ui_manager
        )
        self.configurar_entrada(self.entrada_telefono, "Número telefónico")

        # Botón de confirmación
        self.confirmar_crear = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.rect_x + (self.rect_ancho // 6), self.crear_y + 355),
                (self.rect_ancho * 2 // 3, 40)),
            text="Confirmar",
            manager=self.ui_manager
        )
        self.confirmar_crear.disable()

        # Botón de regresar
        self.regresar_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.rect_x + (self.rect_ancho // 6), self.crear_y + 400),
                (self.rect_ancho * 2 // 3, 40)),
            text="Regresar",
            manager=self.ui_manager
        )

    def configurar_entrada(self, entrada, placeholder_text):
        """Configura cada entrada de texto"""
        entrada.placeholder_text = placeholder_text
        entrada.set_text("")
        entrada.background_colour = pygame.Color(COLORS['WHITE'])
        entrada.border_colour = pygame.Color(COLORS['YELLOW'])
        entrada.text_colour = pygame.Color(0, 0, 0)
        entrada.rebuild()


    def validar_campos(self):
        """Valida si los campos están llenos, si tienen formato correcto 
        y actualiza el estado del botón confirmar"""
        correo_texto = self.entrada_correo.get_text().strip()
        password_texto = self.entrada_password.get_text().strip()
        nombre_texto = self.entrada_nombre.get_text().strip()
        telefono_texto = self.entrada_telefono.get_text().strip()

        nombre_valido = bool(re.fullmatch(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]{2,50}$", nombre_texto))
        correo_valido = bool(re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', correo_texto))
        telefono_valido = bool(re.fullmatch(r"^\d{8}$", telefono_texto))

        if correo_texto and password_texto and nombre_texto and telefono_texto and nombre_valido and correo_valido and telefono_valido:
            self.confirmar_crear.enable()
        else:
            self.confirmar_crear.disable()

    def handle_event(self, event):
        """Maneja eventos de la vista"""
        self.ui_manager.process_events(event)
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                if event.ui_element in [self.entrada_correo, self.entrada_password, self.entrada_nombre, self.entrada_telefono]:
                    self.validar_campos()
            elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.confirmar_crear:
                    self.change_screen_callback(Screens.HOMEPAGE, paid=False)
                if event.ui_element == self.regresar_button:
                    self.change_screen_callback(Screens.SIGN_IN)

    def update(self):
        """Actualiza los elementos de la UI"""
        time_delta = self.clock.tick(60) / 1000.0
        self.ui_manager.update(time_delta)

    def draw(self):
        """Dibuja todos los elementos de la vista"""
        self.surface.fill(COLORS['GREEN'])
        pygame.draw.rect(self.surface, (COLORS['WHITE']), (self.rect_x, self.rect_y, self.rect_ancho, self.rect_alto))

        # Dibujar la imagen del logo
        logo_x = self.rect_x + (self.rect_ancho - self.logo_image.get_width()) // 2
        logo_y = self.rect_y + 20
        self.surface.blit(self.logo_image, (logo_x, logo_y))

        # Dibujar etiquetas de texto
        self.surface.blit(self.crear_cuenta_label, (self.crear_x, self.crear_y + 10))

        # Dibujar la interfaz de usuario
        self.ui_manager.draw_ui(self.surface)
        pygame.display.flip()

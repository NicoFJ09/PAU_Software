import pygame
import pygame_gui
from E_Commerce.constants import COLORS
from E_Commerce.Screens_web import Screens

class PaymentView:
    def __init__(self, surface, window_size, change_screen_callback, totalprice):
        self.surface = surface
        self.window_size = window_size
        self.ui_manager = pygame_gui.UIManager(window_size)
        self.change_screen_callback = change_screen_callback
        self.total_price = totalprice
        # Configuración inicial de los elementos de UI
        self.setup_ui()

    def setup_ui(self):
        """Configura los elementos de la interfaz de usuario"""
        screen_width = self.window_size[0]
        screen_height = self.window_size[1]

        # Ajustar contenedor principal proporcionalmente
        container_width = min(700, screen_width * 0.7)
        container_height = min(400, screen_height * 0.6)
        container_x = (screen_width - container_width) // 2
        container_y = (screen_height - container_height) // 2

        # Contenedor de elementos
        self.main_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((container_x, container_y), (container_width, container_height)),
            manager=self.ui_manager
        )
        # Ejemplo de etiqueta
        self.label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 10), (container_width - 20, 30)),
            text="Bienvenido a la nueva vista",
            manager=self.ui_manager,
            container=self.main_panel
        )

        # Ejemplo de botón (más pequeño)
        self.button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((150, 50), (60, 30)),
            text="Tarjeta",
            manager=self.ui_manager,
            container=self.main_panel
        )

        self.button2 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 50), (60, 30)),
            text="Sinpe",
            manager=self.ui_manager,
            container=self.main_panel
        )

        # Cajas de texto
        self.text_box1 = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((10, 100), (container_width - 20, 30)),
            manager=self.ui_manager,
            container=self.main_panel
        )

        self.text_box2 = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((10, 140), (container_width - 20, 30)),
            manager=self.ui_manager,
            container=self.main_panel
        )

        # Mostrar el total del carrito de compras
        self.total_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 180), (container_width - 20, 30)),
            text=f"Total del carrito: ${self.total_price}",
            manager=self.ui_manager,
            container=self.main_panel
        )
        self.button3 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((250, 220), (60, 30)),
            text="Pagar",
            manager=self.ui_manager,
            container=self.main_panel
        )

        self.button3 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 280), (60, 30)),
            text="volver",
            manager=self.ui_manager,
            container=self.main_panel
        )

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.button:
                print("Botón Tarjeta presionado. Habilitando cuadros de texto...")
                self.text_box1.enable()
                self.text_box2.enable()
            elif event.ui_element == self.button2:
                print("Botón Simpe presionado. Deshabilitando cuadros de texto...")
                self.text_box1.disable()
                self.text_box2.disable()
            elif event.ui_element == self.button3:
                print("Botón Pagar presionado. Cambiando a la vista de inicio...")
                self.change_screen_callback(Screens.SHOPPING_CART)

        self.ui_manager.process_events(event)

    def update(self):
        self.ui_manager.update(pygame.time.get_ticks() / 1000.0)

    def draw(self):
        self.surface.fill(COLORS['GREEN'])
        self.ui_manager.draw_ui(self.surface)
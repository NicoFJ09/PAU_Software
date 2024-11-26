import pygame
import pygame_gui
import re
from E_Commerce.constants import COLORS
from E_Commerce.Screens_web import Screens
from E_Commerce.controllers.Payment_controller import PaymentController
import globals  # Import the globals module

class PaymentView:
    def __init__(self, surface, window_size, change_screen_callback, items, products, totalprice):
        self.surface = surface
        self.window_size = window_size
        self.ui_manager = pygame_gui.UIManager(window_size)
        self.change_screen_callback = change_screen_callback
        self.items = items
        self.products = products
        self.total_price = totalprice

        self.selected_delivery_button = None
        self.selected_payment_button = None

        # Instanciar Controlador
        self.controller = PaymentController()

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
            text="Ingresa tu método de pago y entrega",
            manager=self.ui_manager,
            container=self.main_panel
        )

        # Centering the "Envio" and "Recoger" buttons
        button_width = 100  # Increased button width
        button_height = 30
        button_spacing = 20  # Space between the buttons
        total_button_width = (2 * button_width) + button_spacing
        button_x_start = (container_width - total_button_width) // 2

        self.envio_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x_start, 50), (button_width, button_height)),
            text="Envio",
            manager=self.ui_manager,
            container=self.main_panel
        )
        self.recoger_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x_start + button_width + button_spacing, 50), (button_width, button_height)),
            text="Recoger",
            manager=self.ui_manager,
            container=self.main_panel
        )

        # Conditionally enable or disable the "Envio" button
        if not globals.signed_in:
            self.envio_button.disable()

        # Centering the "Tarjeta" and "Sinpe" buttons
        self.button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x_start, 100), (button_width, button_height)),
            text="Tarjeta",
            manager=self.ui_manager,
            container=self.main_panel
        )

        self.button2 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x_start + button_width + button_spacing, 100), (button_width, button_height)),
            text="Sinpe",
            manager=self.ui_manager,
            container=self.main_panel
        )

        # Cajas de texto
        self.text_box1 = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((10, 150), (container_width - 20, 30)),
            manager=self.ui_manager,
            container=self.main_panel
        )
        self.text_box1.rebuild()
        self.text_box1.disable()  # Initially disable the card number input

        self.text_box2 = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((10, 190), (container_width - 20, 30)),
            manager=self.ui_manager,
            container=self.main_panel
        )
        self.text_box2.rebuild()
        self.text_box2.disable()  # Initially disable the security code input

        # Set placeholder text after disabling the text boxes
        self.text_box1.set_text("")
        self.text_box2.set_text("")

        # Mostrar el total del carrito de compras
        self.total_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 230), (container_width - 20, 30)),
            text=f"Total del carrito: {self.total_price} col",
            manager=self.ui_manager,
            container=self.main_panel
        )

        # Centering the "Pagar" button
        self.button3 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((container_width // 2 - button_width // 2, 270), (button_width, button_height)),
            text="Pagar",
            manager=self.ui_manager,
            container=self.main_panel
        )

        # Positioning the "Volver" button slightly lower
        self.button4 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((container_width // 2 - button_width // 2, 320), (button_width, button_height)),
            text="Volver",
            manager=self.ui_manager,
            container=self.main_panel
        )

        # Initially disable the "Pagar" button
        self.button3.disable()

    def handle_event(self, event):
        self.ui_manager.process_events(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.envio_button:
                print("Botón Envio presionado.")
                self.toggle_button(self.envio_button, "delivery")
            elif event.ui_element == self.recoger_button:
                print("Botón Recoger presionado.")
                self.toggle_button(self.recoger_button, "delivery")
            elif event.ui_element == self.button:
                print("Botón Tarjeta presionado. Habilitando cuadros de texto...")
                self.text_box1.enable()
                self.text_box2.enable()
                self.text_box1.set_text("")
                self.text_box2.set_text("")
                self.text_box1.placeholder_text = "Número de tarjeta"
                self.text_box2.placeholder_text = "Código de seguridad"
                self.text_box1.rebuild()
                self.text_box2.rebuild()
                self.toggle_button(self.button, "payment")
                self.validate_card_details()
            elif event.ui_element == self.button2:
                print("Botón Sinpe presionado. Deshabilitando cuadros de texto...")
                self.text_box1.disable()
                self.text_box2.disable()
                self.text_box1.set_text("")
                self.text_box2.set_text("")
                self.toggle_button(self.button2, "payment")
                self.button3.enable()  # Enable "Pagar" button for Sinpe
            elif event.ui_element == self.button3:
                for item in self.items:
                    self.controller.sell_products(item["CodigoProducto"], item["cantidad"])
                self.change_screen_callback(Screens.HOMEPAGE, paid=True)
            elif event.ui_element == self.button4:
                self.change_screen_callback(Screens.SHOPPING_CART, self.items, self.products)

        if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
            if event.ui_element == self.text_box1 or event.ui_element == self.text_box2:
                self.validate_card_details()

        if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
            if event.ui_element == self.text_box1:
                self.format_card_number()
            elif event.ui_element == self.text_box2:
                self.limit_security_code()

    def validate_card_details(self):
        card_number = self.text_box1.get_text().strip().replace(" ", "")
        security_code = self.text_box2.get_text().strip()
        card_number_valid = bool(re.fullmatch(r'^\d{16}$', card_number))
        security_code_valid = bool(re.fullmatch(r'^\d{3,}$', security_code))

        if card_number_valid and security_code_valid:
            self.button3.enable()
        else:
            self.button3.disable()

    def format_card_number(self):
        card_number = self.text_box1.get_text().strip().replace(" ", "")
        if not card_number.isdigit():
            card_number = re.sub(r'\D', '', card_number)  # Remove non-digit characters

        if len(card_number) > 16:
            card_number = card_number[:16]

        formatted_card_number = ' '.join([card_number[i:i+4] for i in range(0, len(card_number), 4)])
        self.text_box1.set_text(formatted_card_number)

    def limit_security_code(self):
        security_code = self.text_box2.get_text().strip()
        if not security_code.isdigit():
            security_code = re.sub(r'\D', '', security_code)  # Remove non-digit characters

        if len(security_code) > 3:
            security_code = security_code[:3]

        self.text_box2.set_text(security_code)

    def toggle_button(self, button, group):
        if group == "delivery":
            if self.selected_delivery_button:
                self.selected_delivery_button.set_text(self.selected_delivery_button.text.replace("[", "").replace("]", ""))
            self.selected_delivery_button = button
        elif group == "payment":
            if self.selected_payment_button:
                self.selected_payment_button.set_text(self.selected_payment_button.text.replace("[", "").replace("]", ""))
            self.selected_payment_button = button

        button.set_text(f"[{button.text.replace('[', '').replace(']', '')}]")

    def update(self):
        # Use a fixed time delta for updating the UI manager
        time_delta = 1 / 60.0  # 60 FPS
        self.ui_manager.update(time_delta)

    def draw(self):
        self.surface.fill(COLORS['GREEN'])
        self.ui_manager.draw_ui(self.surface)
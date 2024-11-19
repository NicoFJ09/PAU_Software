import pygame
import pygame_gui
from E_Commerce.constants import COLORS

class ShoppingCartView:
    def __init__(self, surface, window_size, change_screen_callback):
        self.surface = surface
        self.window_size = window_size
        self.ui_manager = pygame_gui.UIManager(window_size)
        self.change_screen_callback = change_screen_callback
        signedin = True

        # Configuración inicial de los elementos de UI
        self.items = ["Item 1 - $10", "Item 2 - $15", "Item 3 - $20", "Item 4 - $25"]
        self.setup_ui()

    def setup_ui(self):
        """Configura los elementos de la interfaz de usuario"""
        # Usar dimensiones de window_size
        screen_width = self.window_size[0]
        screen_height = self.window_size[1]
        
        # Ajustar contenedor principal proporcionalmente
        container_width = min(700, screen_width * 0.7)  # 70% del ancho de pantalla, máximo 700
        container_height = min(400, screen_height * 0.6)  # 60% del alto de pantalla, máximo 400
        container_x = (screen_width - container_width) // 2
        container_y = (screen_height - container_height) // 2

        # Contenedor de elementos
        self.item_containers = []
        y_offset = container_y
        for item in self.items:
            item_panel = pygame_gui.elements.UIPanel(
                relative_rect=pygame.Rect((container_x, y_offset), (container_width, 50)),
                manager=self.ui_manager
            )

            # Ajustar ancho del label proporcionalmente
            label_width = container_width * 0.7  # 70% del contenedor
            button_width = (container_width - label_width - 30) // 2  # Dividir espacio restante

            item_label = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((10, 10), (label_width, 30)),
                text=item,
                manager=self.ui_manager,
                container=item_panel
            )
            
            # Posicionar botones
            button_x = label_width + 20
            add_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((button_x, 10), (button_width, 30)),
                text='Add',
                manager=self.ui_manager,
                container=item_panel
            )
            
            remove_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((button_x + button_width + 10, 10), (button_width, 30)),
                text='Remove',
                manager=self.ui_manager,
                container=item_panel
            )
            
            self.item_containers.append((item, item_panel, add_button, remove_button))
            y_offset += 60

        # Elemento de total
        total_y_position = y_offset + 20
        self.total_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((container_x, total_y_position), (container_width, 40)),
            text="Total: $0",
            manager=self.ui_manager
        )

        # Botón y label de opción de entrega
        delivery_y_position = total_y_position + 60
        delivery_label_width = container_width * 0.3  # 30% del contenedor
        delivery_button_width = container_width * 0.3  # 30% del contenedor
        
        self.delivery_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((container_x, delivery_y_position), (delivery_label_width, 40)),
            text="Entrega: Delivery",
            manager=self.ui_manager
        )
        
        self.change_delivery_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((container_x + delivery_label_width + 10, delivery_y_position), 
                                    (delivery_button_width, 40)),
            text="Cambiar entrega",
            manager=self.ui_manager
        )

        # Botón de "Siguiente"
        next_button_y_position = delivery_y_position + 60
        self.next_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((container_x, next_button_y_position), (container_width, 50)),
            text="Siguiente",
            manager=self.ui_manager
        )

        # Variables de control
        self.total_price = 0
        self.cart_items = []
        self.delivery_option = "Delivery"

    def handle_event(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                for item, item_panel, add_button, remove_button in self.item_containers:
                    if event.ui_element == add_button:
                        item_price = int(item.split('$')[-1])
                        self.total_price += item_price
                        self.cart_items.append(item)
                        self.total_label.set_text(f"Total: ${self.total_price}")
                    elif event.ui_element == remove_button:
                        if item in self.cart_items:
                            item_price = int(item.split('$')[-1])
                            self.total_price -= item_price
                            self.cart_items.remove(item)
                            self.total_label.set_text(f"Total: ${self.total_price}")

                if event.ui_element == self.change_delivery_button:
                    self.delivery_option = "Retiro" if self.delivery_option == "Delivery" else "Delivery"
                    self.delivery_label.set_text(f"Entrega: {self.delivery_option}")

                if event.ui_element == self.next_button:
                    print("Botón 'Siguiente' presionado. Pasando a la siguiente pantalla...")
        
        self.ui_manager.process_events(event)

    def update(self):
        self.ui_manager.update(pygame.time.get_ticks() / 1000.0)

    def draw(self):
        self.surface.fill(COLORS['WHITE'])
        self.ui_manager.draw_ui(self.surface)
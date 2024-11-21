import pygame
import pygame_gui
from E_Commerce.constants import COLORS
from E_Commerce.Screens_web import Screens

class ShoppingCartView:
    def __init__(self, surface, window_size, change_screen_callback):
        self.surface = surface
        self.window_size = window_size
        self.ui_manager = pygame_gui.UIManager(window_size)
        self.change_screen_callback = change_screen_callback
        
        self.atras_image = pygame.image.load("Images/atras.png").convert_alpha()
        self.atras_image = pygame.transform.scale(self.atras_image, (50, 50))
        self.logo_image = pygame.image.load("Images/logo.png").convert_alpha()
        self.logo_image = pygame.transform.scale(self.logo_image, (90, 90))
        self.letras_image = pygame.image.load("Images/letras.png").convert_alpha()
        self.letras_image = pygame.transform.scale(self.letras_image, (100, 100))

        # Diccionario de productos
        self.items = [
            {"codigoProducto": "MPP", "Nombre": "Malla de papas", "Precio": 1500, "cantidad": 4},
            {"codigoProducto": "CHPP", "Nombre": "Chips (200g)", "Precio": 500, "cantidad": 2},
            {"codigoProducto": "CHPG", "Nombre": "Chips (500g)", "Precio": 1000, "cantidad": 3},
            {"codigoProducto": "SALP", "Nombre": "Salsa de tomate (500ml)", "Precio": 1000, "cantidad": 2},
            {"codigoProducto": "SLTP", "Nombre": "Salsa de tomate en lata (400g)", "Precio": 1000, "cantidad": 2},
            {"codigoProducto": "SLTG", "Nombre": "Salsa de tomate en lata (1kg)", "Precio": 1800, "cantidad": 1},
            {"codigoProducto": "MTM", "Nombre": "Malla de tomates", "Precio": 2000, "cantidad": 0},
            {"codigoProducto": "SALG", "Nombre": "Salsa de tomate (1L)", "Precio": 1800, "cantidad": 0}
        ]

        self.setup_ui()

    def setup_ui(self):
        """Configura los elementos de la interfaz de usuario"""
        screen_width = self.window_size[0]
        screen_height = self.window_size[1]
        
        container_width = min(700, screen_width * 0.7)
        container_height = min(400, screen_height * 0.6)
        container_x = (screen_width - container_width) // 2
        container_y = (screen_height - container_height) // 2

        self.item_containers = []
        y_offset = container_y
        for item in self.items:
            item_panel = pygame_gui.elements.UIPanel(
                relative_rect=pygame.Rect((container_x, y_offset), (container_width, 50)),
                manager=self.ui_manager
            )

            label_width = container_width * 0.5  # Reducimos el ancho para dejar espacio para la cantidad
            button_width = (container_width - label_width - 30) // 3

            # Etiqueta del producto
            item_label = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((10, 10), (label_width, 30)),
                text=f"{item['Nombre']} - ${item['Precio']}",
                manager=self.ui_manager,
                container=item_panel
            )
            
            button_x = label_width + 10
            add_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((button_x, 10), (button_width, 30)),
                text='+',
                manager=self.ui_manager,
                container=item_panel
            )
            
            remove_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((button_x + 2 * button_width, 10), (button_width, 30)),
                text='-',
                manager=self.ui_manager,
                container=item_panel
            )
            
                # Crear un label para la cantidad entre los botones
            quantity_label = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((button_x + button_width, 10), (button_width, 30)),
                text=str(item['cantidad']),
                manager=self.ui_manager,
                container=item_panel
            )
            
            self.item_containers.append((item, item_panel, add_button, remove_button, quantity_label))
            y_offset += 60

        # Total
        total_y_position = y_offset + 20
        self.total_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((container_x, total_y_position), (container_width, 40)),
            text=f"Total: ${int(self.calculate_total())}",
            manager=self.ui_manager
        )

        # Botones y labels
        self.atras_b = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((1170, 20), (50, 50)),
            text="",
            manager=self.ui_manager
        )
        self.atras_b.set_image(self.atras_image)

        self.next_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((container_x, total_y_position + 60), (container_width, 50)),
            text="Siguiente",
            manager=self.ui_manager
        )

    def handle_event(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.atras_b:
                    self.change_screen_callback(Screens.HOMEPAGE)
                for item, item_panel, add_button, remove_button, quantity_label in self.item_containers:
                    if event.ui_element == add_button:
                        if item['cantidad'] < 20:  # Límite máximo
                            item['cantidad'] += 1
                            quantity_label.set_text(f"{item['cantidad']}")
                            self.total_label.set_text(f"Total: ${self.calculate_total()}")
                    elif event.ui_element == remove_button:
                        if item['cantidad'] > 0:  # Evitar cantidad negativa
                            item['cantidad'] -= 1
                            quantity_label.set_text(f"{item['cantidad']}")
                            self.total_label.set_text(f"Total: ${self.calculate_total()}")
                if event.ui_element == self.next_button:
                    self.change_screen_callback(Screens.PAYMENT)
        
        self.ui_manager.process_events(event)

    def calculate_total(self):
        """Calcula el total del carrito"""
        total = sum(item['Precio'] * item['cantidad'] for item in self.items)
        return total

    def update(self):
        self.ui_manager.update(pygame.time.get_ticks() / 1000.0)
        print(self.items)
        

    def draw(self):
        self.surface.fill(COLORS['GREEN'])
        self.ui_manager.draw_ui(self.surface)
        self.surface.blit(self.atras_image, (1170, 20))
        self.surface.blit(self.logo_image, (30, 18))
        self.surface.blit(self.letras_image, (130, 18))
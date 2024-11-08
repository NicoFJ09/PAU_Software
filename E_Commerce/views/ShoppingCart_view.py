import pygame
import pygame_gui
#from E_Commerce.constants import COLORS
#from E_Commerce.controllers.ShoppingCart_controller import Shoppingcartcontroller

class ShoppingCartView:
    def __init__(self, surface, window_size, change_screen_callback):
        self.surface = surface
        self.window_size = window_size
        self.ui_manager = pygame_gui.UIManager(window_size)
        self.change_screen_callback = change_screen_callback
        
        # Configuraciones iniciales
        self.setup_ui_theme()
        self.setup_fonts()
        
# Inicializar pygame
pygame.init()

# Dimensiones de la pantalla
screen_width = 800
screen_height = 700  # Aumentamos la altura para hacer espacio para los nuevos elementos
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Shopping Cart")

# Inicializar el gestor de la interfaz
manager = pygame_gui.UIManager((screen_width, screen_height))

# Lista de items simulada
items = ["Item 1 - $10", "Item 2 - $15", "Item 3 - $20", "Item 4 - $25"]

# Crear contenedor de elementos de la interfaz
item_containers = []
y_offset = 50
for item in items:
    item_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((50, y_offset), (700, 50)),
                                                manager=manager)
    item_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 10), (500, 30)),
                                            text=item,
                                            manager=manager,
                                            container=item_panel)
    add_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((520, 10), (80, 30)),
                                            text='Add',
                                            manager=manager,
                                            container=item_panel)
    remove_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((610, 10), (80, 30)),
                                                text='Remove',
                                                manager=manager,
                                                container=item_panel)
    item_containers.append((item, item_panel, add_button, remove_button))
    y_offset += 60

# Elemento de total
total_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, y_offset + 20), (700, 40)),
                                        text="Total: $0",
                                        manager=manager)

# Botón y label de opción de entrega
delivery_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, y_offset + 80), (200, 40)),
                                            text="Entrega: Delivery",
                                            manager=manager)
change_delivery_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((260, y_offset + 80), (150, 40)),
                                                    text="Cambiar entrega",
                                                    manager=manager)

# Botón de "Siguiente"
next_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, y_offset + 140), (700, 50)),
                                        text="Siguiente",
                                        manager=manager)

# Variables de control de carrito y entrega
total_price = 0
cart_items = []
delivery_option = "Delivery"

# Bucle principal
clock = pygame.time.Clock()
running = True
while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                for item, item_panel, add_button, remove_button in item_containers:
                    if event.ui_element == add_button:
                        # Agregar el artículo al carrito
                        item_price = int(item.split('$')[-1])
                        total_price += item_price
                        cart_items.append(item)
                        total_label.set_text(f"Total: ${total_price}")
                    elif event.ui_element == remove_button:
                        # Remover el artículo si está en el carrito
                        if item in cart_items:
                            item_price = int(item.split('$')[-1])
                            total_price -= item_price
                            cart_items.remove(item)
                            total_label.set_text(f"Total: ${total_price}")
                
                # Manejar el botón de cambio de entrega
                if event.ui_element == change_delivery_button:
                    if delivery_option == "Delivery":
                        delivery_option = "Retiro"
                    else:
                        delivery_option = "Delivery"
                    delivery_label.set_text(f"Entrega: {delivery_option}")
                
                # Manejar el botón de "Siguiente"
                if event.ui_element == next_button:
                    print("Botón 'Siguiente' presionado. Pasando a la siguiente pantalla...")
                    # Aquí se podría añadir la lógica para cambiar de pantalla o estado

        manager.process_events(event)

    # Actualizar la interfaz
    manager.update(time_delta)

    # Dibujar la pantalla
    screen.fill((255, 255, 255))
    manager.draw_ui(screen)

    pygame.display.flip()

# Salir de pygame
pygame.quit()

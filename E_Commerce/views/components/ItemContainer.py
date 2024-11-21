import pygame
import pygame_gui
from E_Commerce.constants import COLORS

class ItemContainer:
    def __init__(self, surface, window_size, producto, ui_manager):
        self.surface = surface
        self.window_size = window_size
        self.producto = producto
        self.manager = ui_manager

        # Configurar el tamaño y la posición del contenedor
        self.width = self.window_size[0] // 2
        self.height = self.window_size[1] // 2
        self.x = (self.window_size[0] - self.width) // 2
        self.y = (self.window_size[1] - self.height) // 2

        # Crear botones "Añadir a carrito" y "Cancelar"
        self.boton_añadir = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.x + 50, self.y + self.height - 60),
                (150, 50)  # Ajustar el ancho del botón
            ),
            text="Añadir a carrito",
            manager=self.manager
        )
        self.boton_cancelar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.x + self.width - 150, self.y + self.height - 60),
                (100, 50)
            ),
            text="Cancelar",
            manager=self.manager
        )

        # Crear entrada de texto para la cantidad a ordenar
        self.cantidad_ordenar_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(
                (self.x + 20, self.y + 200),
                (self.width - 40, 30)
            ),
            manager=self.manager
        )

    def draw(self):
        """Dibuja el contenedor emergente con la información del producto"""
        # Dibujar fondo del contenedor
        pygame.draw.rect(
            self.surface,
            COLORS['WHITE'],
            (self.x, self.y, self.width, self.height),
            border_radius=10
        )

        # Dibujar borde del contenedor
        pygame.draw.rect(
            self.surface,
            COLORS['RED'],
            (self.x, self.y, self.width, self.height),
            width=2,
            border_radius=10
        )

        # Dibujar información del producto
        font = pygame.font.Font(None, 30)
        nombre_text = font.render(f"Nombre: {self.producto['Nombre']}", True, COLORS['BLACK'])
        self.surface.blit(nombre_text, (self.x + 20, self.y + 20))

        precio_text = font.render(f"Precio: {self.producto['Precio']}", True, COLORS['BLACK'])
        self.surface.blit(precio_text, (self.x + 20, self.y + 60))

        cantidad_text = font.render(f"Inventario Disponible: {self.producto['cantidad']}", True, COLORS['BLACK'])
        self.surface.blit(cantidad_text, (self.x + 20, self.y + 100))

        descuento_text = font.render(f"Descuento: {self.producto['Descuento']}%", True, COLORS['BLACK'])
        self.surface.blit(descuento_text, (self.x + 20, self.y + 140))

        # Dibujar texto "Cantidad a ordenar"
        cantidad_ordenar_text = font.render("Cantidad a ordenar:", True, COLORS['BLACK'])
        self.surface.blit(cantidad_ordenar_text, (self.x + 20, self.y + 170))

        # Dibujar la interfaz de usuario
        self.manager.draw_ui(self.surface)

    def handle_event(self, event):
        """Maneja eventos del contenedor emergente"""
        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.boton_añadir:
                cantidad_ordenar = self.cantidad_ordenar_input.get_text()
                if cantidad_ordenar.isdigit() and int(cantidad_ordenar) <= self.producto['cantidad']:
                    print(f"Producto añadido al carrito: {self.producto['CodigoProducto']}, Cantidad: {cantidad_ordenar}")
                    return "añadir", self.producto['CodigoProducto'], int(cantidad_ordenar)
                else:
                    print("Cantidad a ordenar excede el inventario disponible")
            elif event.ui_element == self.boton_cancelar:
                print("Operación cancelada")
                return "cancelar"
        return None

    def hide(self):
        """Oculta los botones del contenedor emergente"""
        self.boton_añadir.hide()
        self.boton_cancelar.hide()
        self.cantidad_ordenar_input.hide()
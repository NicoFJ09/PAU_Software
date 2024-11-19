import pygame
import pygame_gui
from E_Commerce.constants import COLORS
from E_Commerce.views.components.ScrollBar import Scrollbar

class WebContainer:
    def __init__(self, surface, window_size, productos, imagenes, ui_manager):
        self.surface = surface
        self.window_size = window_size
        self.productos = productos
        self.imagenes = imagenes
        self.manager = ui_manager
        self.padding = 50

        # Configurar el tamaño y la posición del contenedor
        self.width = self.window_size[0] - 2 * self.padding
        self.height = 3 * self.window_size[1] // 4
        self.x = self.padding
        self.y = self.window_size[1] - self.height - self.padding

        # Configuración de los paneles de productos
        self.panel_margin = 20
        self.panel_size = (self.width - 5 * self.panel_margin) // 4
        self.total_panels = len(self.productos)
        self.panels_per_row = 4
        self.rows = (self.total_panels + self.panels_per_row - 1) // self.panels_per_row

        # Inicializar scroll_index
        self.scroll_index = 0

        # Crear scrollbar si hay más de dos filas
        self.scrollbar = None
        if self.rows > 2:
            self.scrollbar = Scrollbar(
                x=self.x + self.width + 2,
                y=self.y,
                width=10,
                height=self.height,
                total_items=self.rows,
                visible_items=2
            )

        # Crear botones "Ver más" para cada producto
        self.botones_ver_mas = []
        for i in range(len(self.productos)):
            boton_rect = pygame.Rect(0, 0, 70, 25)
            boton_ver_mas = pygame_gui.elements.UIButton(
                relative_rect=boton_rect,
                text="Ver más",
                manager=self.manager,
                object_id=f"ver_mas_{i}"
            )
            boton_ver_mas.hide()  # Ocultar todos los botones inicialmente
            self.botones_ver_mas.append(boton_ver_mas)

        # Cargar imagen predeterminada
        self.default_image = pygame.image.load("Images/PaperBag.png").convert_alpha()
        self.default_image = pygame.transform.scale(self.default_image, (150, 150))

    def draw(self):
        """Dibuja el contenedor con un borde y fondo transparente"""
        # Dibujar borde del contenedor
        pygame.draw.rect(
            self.surface,
            COLORS['RED'],
            (self.x, self.y, self.width, self.height),
            width=2
        )

        # Ocultar todos los botones primero
        for boton in self.botones_ver_mas:
            boton.hide()

        # Dibujar productos en sus paneles
        start_row = self.scroll_index
        start_index = start_row * self.panels_per_row
        end_index = min(start_index + 2 * self.panels_per_row, self.total_panels)
        visible_productos = self.productos[start_index:end_index]

        for i, producto in enumerate(visible_productos):
            row = (start_index + i) // self.panels_per_row
            col = (start_index + i) % self.panels_per_row
            x = self.x + self.panel_margin + col * (self.panel_size + self.panel_margin)
            y = self.y + self.panel_margin + (row - start_row) * (self.panel_size + self.panel_margin)
            panel_rect = pygame.Rect(x, y, self.panel_size, self.panel_size)
            pygame.draw.rect(self.surface, COLORS['WHITE'], panel_rect, border_radius=10)

            # Cargar y dibujar la imagen del producto si existe
            codigo_producto = producto["CodigoProducto"]
            imagen_path = next((img[codigo_producto] for img in self.imagenes if codigo_producto in img), None)
            if imagen_path:
                imagen_producto = pygame.image.load(imagen_path).convert_alpha()
                imagen_producto = pygame.transform.scale(imagen_producto, (150, 150))
                self.surface.blit(imagen_producto, (panel_rect.x + 10, panel_rect.y + 10))
            else:
                # Dibujar imagen predeterminada si no hay imagen específica
                self.surface.blit(self.default_image, (panel_rect.x + 10, panel_rect.y + 10))

            # Dibujar nombre y precio debajo de la imagen
            font = pygame.font.Font(None, 20)
            nombre_lines = self.split_text(producto["Nombre"], font, self.panel_size * 3 // 4)
            for j, line in enumerate(nombre_lines):
                self.surface.blit(line, (panel_rect.x + 10, panel_rect.y + 170 + j * 25))

            precio_text = font.render(f"Precio: {producto['Precio']}", True, COLORS['BLACK'])
            self.surface.blit(precio_text, (panel_rect.x + 10, panel_rect.y + 220))

            # Aplicar descuento si existe
            descuento = producto.get("Descuento", 0)
            if descuento > 0:
                # Dibujar línea roja sobre el precio original
                precio_rect = precio_text.get_rect(topleft=(panel_rect.x + 10, panel_rect.y + 220))
                pygame.draw.line(self.surface, COLORS['RED'], (precio_rect.left, precio_rect.centery), (precio_rect.right, precio_rect.centery), 2)

                # Calcular y dibujar el nuevo precio con descuento
                precio_original = int(producto['Precio'])
                nuevo_precio = precio_original * (1 - descuento / 100)
                nuevo_precio_text = font.render(f"Nuevo Precio: {int(nuevo_precio)}", True, COLORS['BLACK'])
                self.surface.blit(nuevo_precio_text, (panel_rect.x + 10, panel_rect.y + 240))

                # Dibujar el texto de descuento junto al precio original
                descuento_text = font.render(f"-{descuento}%", True, COLORS['RED'])
                descuento_text_rect = descuento_text.get_rect(topleft=(precio_rect.right + 10, panel_rect.y + 220))
                self.surface.blit(descuento_text, descuento_text_rect.topleft)

            # Actualizar y mostrar botón correspondiente
            boton = self.botones_ver_mas[i]
            boton.set_position((x + self.panel_size - 80, y + self.panel_size - 35))
            boton.show()

        # Dibujar la interfaz de usuario
        self.manager.draw_ui(self.surface)

        # Dibujar scrollbar si existe
        if self.scrollbar:
            self.scrollbar.draw(self.surface)

    def handle_event(self, event):
        """Maneja eventos del contenedor"""
        if self.scrollbar:
            new_index = self.scrollbar.handle_event(event)
            if new_index is not None:
                self.scroll_index = new_index
                return

        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            start_index = self.scroll_index * self.panels_per_row
            for i, boton in enumerate(self.botones_ver_mas):
                if event.ui_element == boton:
                    real_index = start_index + i
                    if real_index < len(self.productos):
                        producto = self.productos[real_index]
                        print(f"Producto {real_index}: {producto}")

    def split_text(self, text, font, max_width):
        """Divide el texto en varias líneas si es demasiado largo"""
        words = text.split(' ')
        lines = []
        current_line = words[0]
        for word in words[1:]:
            if font.size(current_line + ' ' + word)[0] <= max_width:
                current_line += ' ' + word
            else:
                lines.append(font.render(current_line, True, COLORS['BLACK']))
                current_line = word
        lines.append(font.render(current_line, True, COLORS['BLACK']))
        return lines
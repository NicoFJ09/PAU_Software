import pygame
import pygame_gui
from E_Commerce.constants import COLORS
from E_Commerce.Screens_web import Screens
from E_Commerce.views.components.WebContainer import WebContainer
from E_Commerce.controllers.HomePage_controller import HomePageController
from E_Commerce.views.components.ItemContainer import ItemContainer  # Importar el nuevo componente

class HomePageView:
    productos_carrito = []  # Variable de clase
    vaciar_carrito_flag = False  # Flag para vaciar el carrito

    def __init__(self, surface, window_size, change_screen_callback):
        self.surface = surface
        self.window_size = window_size
        self.change_screen_callback = change_screen_callback

        # Crear el administrador de la interfaz
        self.manager = pygame_gui.UIManager(self.window_size)

        # Instanciar Controlador
        self.controller = HomePageController()

        # Cargar imágenes de "encabezado"
        self.logo_image = pygame.image.load("Images/logo.png").convert_alpha()
        self.logo_image = pygame.transform.scale(self.logo_image, (90, 90))
        self.carrito_image = pygame.image.load("Images/carrito.png").convert_alpha()
        self.carrito_image = pygame.transform.scale(self.carrito_image, (65, 65))
        self.letras_image = pygame.image.load("Images/letras.png").convert_alpha()
        self.letras_image = pygame.transform.scale(self.letras_image, (100, 100))

        # Crear entry que simula barra de búsqueda
        self.entrada_busqueda_rect = pygame.Rect(
            (self.window_size[0] // 4, 60),
            (self.window_size[0] // 2, 30)
        )
        self.entrada_busqueda = pygame_gui.elements.UITextEntryLine(
            relative_rect=self.entrada_busqueda_rect,
            manager=self.manager
        )
        self.entrada_busqueda.placeholder_text = "¿Qué estás buscando?"
        self.entrada_busqueda.background_colour = pygame.Color(245, 245, 220)
        self.entrada_busqueda.border_colour = pygame.Color(156, 26, 21)
        self.entrada_busqueda.text_colour = pygame.Color(0, 0, 0)
        self.entrada_busqueda.rebuild()

        # Botón para el carrito
        self.carrito_b = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.window_size[0] // 2 + 550, 60),
                (self.window_size[0] // 35, 35)
            ),
            text="",
            manager=self.manager
        )

        # Lista de productos(define nombre, precio e imagen representativa)
        self.productos = self.controller.get_products()

        # Actualizar productos si hay algo en el carrito
        if HomePageView.productos_carrito:
            self.actualizar_productos()

        self.imagenes = [
            {"MPP": "Images/papas.png"},
            {"MTM": "Images/tomate.png"},
            {"CHPG": "Images/chips500.png"},
            {"CHPP": "Images/chips200.png"},
            {"SALP": "Images/botella500.png"},
            {"SALG": "Images/botella1L.png"},
            {"SLTP": "Images/lata.png"},
            {"SLTG": "Images/lata.png"},
        ]

        # Crear el contenedor web con los productos
        self.web_container = WebContainer(self.surface, self.window_size, self.productos, self.imagenes, self.manager)

        self.clock = pygame.time.Clock()
        self.previous_text = ""
        self.item_container = None  # Inicializar el contenedor emergente como None
        self.producto = None  # Inicializar el producto como None

    def actualizar_productos(self):
        """Actualiza los productos con la información más reciente del carrito"""
        for item in HomePageView.productos_carrito:
            for producto in self.productos:
                if producto["CodigoProducto"] == item["CodigoProducto"]:
                    producto["cantidad"] -= item["cantidad"]
                    break

    @classmethod
    def vaciar_carrito(cls):
        """Vacía el carrito de compras si el flag está activado"""
        if cls.vaciar_carrito_flag:
            cls.productos_carrito.clear()
            cls.vaciar_carrito_flag = False

    def handle_event(self, event):
        """Maneja eventos de la vista"""
        producto = self.manager.process_events(event)
        if not producto:
            producto = self.web_container.handle_event(event)
        if producto and isinstance(producto, dict) and not self.item_container:
            self.producto = producto
            self.item_container = ItemContainer(self.surface, self.window_size, self.producto, self.manager)

        if self.item_container:
            result = self.item_container.handle_event(event)
            if result:
                if result[0] == "añadir":
                    codigo_producto, cantidad_ordenar = result[1], result[2]
                    print(f"Producto añadido al carrito: {codigo_producto}, Cantidad: {cantidad_ordenar}")

                    # Reducir la cantidad del producto en self.productos
                    for producto in self.productos:
                        if producto["CodigoProducto"] == codigo_producto:
                            producto["cantidad"] -= cantidad_ordenar
                            # Crear una copia del producto sin la propiedad Descuento
                            producto_carrito = {k: v for k, v in producto.items() if k != "Descuento"}
                            producto_carrito["cantidad"] = cantidad_ordenar
                            # Aplicar descuento si existe
                            if producto.get("Descuento", 0) > 0:
                                producto_carrito["Precio"] = int(producto["Precio"]) * (1 - producto["Descuento"] / 100)
                            # Verificar si el producto ya está en el carrito
                            for item in HomePageView.productos_carrito:
                                if item["CodigoProducto"] == codigo_producto:
                                    item["cantidad"] += cantidad_ordenar
                                    break
                            else:
                                HomePageView.productos_carrito.append(producto_carrito)
                            break

                    # Imprimir el contenido del carrito
                    print("Productos en el carrito:")
                    for producto in HomePageView.productos_carrito:
                        print(producto)

                    self.producto = None  # Restablecer producto
                    self.item_container.hide()  # Ocultar botones
                    self.item_container = None  # Cerrar el contenedor emergente
                elif result == "cancelar":
                    self.producto = None  # Restablecer producto
                    self.item_container.hide()  # Ocultar botones
                    self.item_container = None  # Cerrar el contenedor emergente

        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.carrito_b:
                self.change_screen_callback(Screens.SHOPPING_CART, HomePageView.productos_carrito, self.productos)

    def update(self):
        """Actualiza elementos de la UI"""
        time_delta = self.clock.tick(60) / 1000.0
        self.manager.update(time_delta)

        # Verificar si la entrada de búsqueda está seleccionada y actualizar su contenido
        current_text = self.entrada_busqueda.get_text()
        if self.entrada_busqueda.is_focused:
            if current_text != self.previous_text:
                print(current_text)
                self.previous_text = current_text
                self.web_container.draw(search_text=current_text, item_container_active=bool(self.item_container))
        else:
            if current_text != self.previous_text:
                self.previous_text = current_text
                self.web_container.draw(search_text=current_text, item_container_active=bool(self.item_container))

    def draw(self):
        """Dibuja todos los elementos de la vista"""
        self.surface.fill(COLORS['GREEN'])

        # Dibujar el contenedor web
        self.web_container.draw(search_text=self.previous_text, item_container_active=bool(self.item_container))
        # Dibujar la interfaz de usuario
        self.manager.draw_ui(self.surface)
        # Dibujar elementos de encabezado
        self.surface.blit(self.logo_image, (30, 18))
        self.surface.blit(self.letras_image, (130, 18))
        self.surface.blit(self.carrito_image, (1170, 45))

        # Dibujar el contenedor emergente si existe
        if self.item_container:
            self.item_container.draw()
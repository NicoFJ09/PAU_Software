import pygame
import pygame_gui
from E_Commerce.constants import COLORS
from E_Commerce.Screens_web import Screens

class HomePageView:
    def __init__(self, window_home, change_screen_callback):
        pygame.init()
        self.change_screen_callback = change_screen_callback
        self.ancho, self.alto = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.window_home = window_home

        # Crear el administrador de la interfaz
        self.manager = pygame_gui.UIManager((self.ancho, self.alto - 50))

        # Configuración del rectángulo de referencia
        self.rect_ancho = self.ancho - 50
        self.rect_alto = int(self.alto * 0.8)
        self.rect_x = (self.ancho - self.rect_ancho) // 2
        self.rect_y = (self.alto - self.rect_alto) // 2 + 50

        # Cargar imágenes de "encabezado"
        self.logo_image = pygame.image.load("Images/logo.png").convert_alpha()
        self.logo_image = pygame.transform.scale(self.logo_image, (90, 90))
        self.carrito_image = pygame.image.load("Images/carrito.png").convert_alpha()
        self.carrito_image = pygame.transform.scale(self.carrito_image, (65, 65))
        self.letras_image = pygame.image.load("Images/letras.png").convert_alpha()
        self.letras_image = pygame.transform.scale(self.letras_image, (100, 100))

        # Crear entry que simula barra de búsqueda
        self.entrada_busqueda_rect = pygame.Rect((self.rect_x + (self.rect_ancho // 4), 60), (self.rect_ancho // 2, 30))
        self.entrada_busqueda = pygame_gui.elements.UITextEntryLine(relative_rect=self.entrada_busqueda_rect, manager=self.manager)
        self.entrada_busqueda.placeholder_text = "¿Qué estás buscando?"
        self.entrada_busqueda.background_colour = pygame.Color(245, 245, 220)
        self.entrada_busqueda.border_colour = pygame.Color(156, 26, 21)
        self.entrada_busqueda.text_colour = pygame.Color(0, 0, 0)
        self.entrada_busqueda.rebuild()

        # Botón para el carrito
        self.carrito_b = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.rect_x + (self.rect_ancho // 2 + 550), 60), (self.rect_ancho // 35, 35)),
            text="",
            manager=self.manager
        )

        # Lista de productos(define nombre, precio e imagen representativa)
        self.productos = [
            {"nombre": "Tomate", "precio": "$ 100", "imagen": "Images/tomate.png"},
            {"nombre": "Papas mini en malla", "precio": "$ 100", "imagen": "Images/papas.png"},
            {"nombre": "Chips de papa (Paquete de 500g)", "precio": "$ 100", "imagen": "Images/chips500.png"},
            {"nombre": "Chips de papa (Paquete de 200g)", "precio": "$ 100", "imagen": "Images/chips200.png"},
            {"nombre": "Salsa de tomate envasada (Botella 500ml)", "precio": "$ 100", "imagen": "Images/botella500.png"},
            {"nombre": "Salsa de tomate envasada (Botella 1L)", "precio": "$ 100", "imagen": "Images/botella1L.png"},
            {"nombre": "Salsa de tomate enlatada (Lata 400g)", "precio": "$ 100", "imagen": "Images/lata.png"},
            {"nombre": "Salsa de tomate enlatada (Lata 1kg)", "precio": "$ 100", "imagen": "Images/lata.png"},
        ]

        # Configuración de los paneles de productos
        self.panel_margin = 20
        self.panel_size = (self.rect_ancho - 5 * self.panel_margin) // 4
        self.total_panels = len(self.productos)
        self.panel_positions = [
            (self.rect_x + self.panel_margin + (i % 4) * (self.panel_size + self.panel_margin),
             self.rect_y + self.panel_margin + (i // 4) * (self.panel_size + self.panel_margin))
            for i in range(self.total_panels)
        ]

        # Crear botones "Ver más" para cada producto
        self.botones_ver_mas = []
        for i, producto in enumerate(self.productos):
            x, y = self.panel_positions[i]
            boton_rect = pygame.Rect((x - self.rect_x + 200, y - self.rect_y + 325), (70, 25))
            boton_ver_mas = pygame_gui.elements.UIButton(
                relative_rect=boton_rect,
                text="Ver más",
                manager=self.manager
            )
            self.botones_ver_mas.append(boton_ver_mas)

        self.clock = pygame.time.Clock()

    def handle_event(self, event):
        """Maneja eventos de la vista"""
        self.manager.process_events(event)
        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.carrito_b:
                self.change_screen_callback(Screens.SHOPPING_CART)  # Redirige a pantalla de carrito de compra

    def update(self):
        """Actualiza elementos de la UI"""
        time_delta = self.clock.tick(60) / 1000.0
        self.manager.update(time_delta)

    def draw(self):
        """Dibuja todos los elementos de la vista"""
        self.window_home.fill(COLORS['GREEN'])
        panel_surface = pygame.Surface((self.rect_ancho, self.rect_alto))
        panel_surface.fill(COLORS['GREEN'])

        # Dibujar productos en sus paneles
        for i, producto in enumerate(self.productos):
            x, y = self.panel_positions[i]
            panel_rect = pygame.Rect(x - self.rect_x, y - self.rect_y, self.panel_size, self.panel_size)
            pygame.draw.rect(panel_surface, COLORS['WHITE'], panel_rect, border_radius=10)

            # Cargar y dibujar la imagen del producto
            imagen_producto = pygame.image.load(producto["imagen"]).convert_alpha()
            imagen_producto = pygame.transform.scale(imagen_producto, (185, 185))
            panel_surface.blit(imagen_producto, (panel_rect.x + 10, panel_rect.y + 10))

            # Dibujar nombre y precio
            font = pygame.font.Font(None, 20)
            nombre_text = font.render(producto["nombre"], True, COLORS['BLACK'])
            precio_text = font.render(producto["precio"], True, COLORS['BLACK'])
            panel_surface.blit(nombre_text, (panel_rect.x + 10, panel_rect.y + 230))
            panel_surface.blit(precio_text, (panel_rect.x + 10, panel_rect.y + 260))

        # Dibujar elementos de encabezado
        self.window_home.blit(panel_surface, (self.rect_x, self.rect_y))
        self.window_home.blit(self.logo_image, (30, 18))
        self.window_home.blit(self.letras_image, (130, 18))
        # Dibujar la interfaz de usuario
        self.manager.draw_ui(self.window_home)
        self.window_home.blit(self.carrito_image, (1170, 45))


import pygame
import pygame_gui
from Admin_Dashboard.constants import COLORS
from Admin_Dashboard.controllers.Discount_controller import DiscountController
from Admin_Dashboard.views.components.Container import Container
from Admin_Dashboard.Screens import Screens 


class DiscountView:
    def __init__(self, surface, window_size, change_screen_callback):
        self.surface = surface
        self.window_size = window_size
        self.ui_manager = pygame_gui.UIManager(window_size)
        self.change_screen_callback = change_screen_callback  # Callback para cambiar la pantalla
        
        # Configuraciones iniciales
        self.setup_ui_theme()
        self.setup_fonts()

        # Instanciar Controlador
        self.controller = DiscountController()

        #Llamar configuración contenedor
        self.setup_container()

        #Llamar configuración Botón Regresar
        self.setup_return_button()

    def setup_container(self):
        """Configura el contenedor y sus productos"""
        container_config = {
            'row_height': 40,
            'spacing': 10,
            'show_input': True,
            'show_button': True,
            'show_dividers': True,
            'input_width': 180,
            'button_width': 80,
            'button_text': 'Actualizar',
            'text_formatter': lambda item: f"{item['Nombre']} - ({item['codigoProducto']}) | Precio:{item['Precio']} | Descuento: {item['Descuento']} %",
            'item_id_field': 'codigoProducto',
            'margin_top': 5, 
            'margin_bottom': 5,
            'visible_rows': 10,
            'enable_row_selection': False,
            'enable_multiple_row_selection': False,
            'allow_zero_discount': True, 
            "placeholder_text": "Porcentaje de descuento"
        }

        self.container = Container(
            surface=self.surface,
            ui_manager=self.ui_manager,
            position=(50, 100),
            width=self.window_size[0] - 100,
            config=container_config
        )
        self.controller.initialize_discount_file()
        # Configurar productos en contenedor
        products = self.controller.get_discounts()
        self.container.setup_rows(products)

    def setup_return_button(self):
        """Configura el botón 'Regresar'"""
        button_x = self.container.x + (self.container.width - 150) / 2  # Centrar el botón en X
        button_y = self.container.y + self.container.height + 20  # Debajo del contenedor
        self.return_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(button_x, button_y, 150, 40),  # Centrar el botón en X
            text='Regresar',
            manager=self.ui_manager
        )


    def setup_ui_theme(self):
        """Configura el tema de la interfaz"""
        self.default_theme = {
            "text_entry_line": {
                "colours": {
                    "dark_bg": "#FFFFFF",
                    "selected_bg": "#F0F0F0",
                    "selected_text": "#F0F0F0",
                    "normal_text": "#000000",
                    "border": "#B90518",
                    "normal_border": "#B90518",
                    "disabled_border": "#B90518",
                    "text_cursor": "#000000"
                }
            },
            "button": {
                "colours": {
                    "normal_bg": "#FCC509",
                    "hovered_bg": "#FFD43B",
                    "selected_bg": "#FFDB4D",
                    "active_bg": "#FCC509",
                    "normal_text": "#000000",
                    "selected_text": "#000000",
                    "border": "#B90518",
                    "normal_border": "#B90518",
                    "disabled_border": "#B90518"
                }
            }
        }
        self.ui_manager.get_theme().load_theme(self.default_theme)

    def setup_fonts(self):
        """Configura las fuentes"""
        self.title_font = pygame.font.SysFont("Georgia", 45)

    def handle_event(self, event):
        """Maneja eventos de la vista"""
        self.ui_manager.process_events(event)
        self.container.handle_event(event, self.Set_discount_and_update)
        # Manejar evento del botón "Regresar"
        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.return_button:
                self.change_screen_callback(Screens.SALE)

    def Set_discount_and_update(self, codigo, descuento):
        # Cambiar descuento al producto
        self.controller.set_discount(codigo, descuento)
        
        # Obtener la lista actualizada de productos
        updated_products = self.controller.get_discounts()
        
        # Actualizar el contenedor con los nuevos productos
        self.container.update(updated_products)

    def update(self):
        """Actualiza elementos de la UI"""
        time_delta = pygame.time.Clock().tick(60)/1000.0
        self.ui_manager.update(time_delta)

    def draw(self):
        """Dibuja todos los elementos de la vista"""
        # Fondo principal
        self.surface.fill(COLORS['WHITE'])
        
        # Título
        title_text = self.title_font.render("Pantalla de Descuentos", True, COLORS['GREEN'])
        title_rect = title_text.get_rect(midtop=(self.window_size[0] // 2, 20))
        self.surface.blit(title_text, title_rect)
        
        # Dibujar elementos UI
        self.container.draw()
        self.ui_manager.draw_ui(self.surface)
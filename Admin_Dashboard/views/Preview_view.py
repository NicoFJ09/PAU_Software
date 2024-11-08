
import pygame
import pygame_gui
from Admin_Dashboard.constants import COLORS
from Admin_Dashboard.controllers.Preview_controller import PreviewController
from Admin_Dashboard.views.components.Container import Container
from Admin_Dashboard.Screens import Screens 


class PreviewView:
    def __init__(self, surface, window_size, change_screen_callback):
        self.surface = surface
        self.window_size = window_size
        self.ui_manager = pygame_gui.UIManager(window_size)
        self.change_screen_callback = change_screen_callback  # Callback para cambiar la pantalla
        
        # Configuraciones iniciales
        self.setup_ui_theme()
        self.setup_fonts()

        # Instanciar Controlador
        self.controller = PreviewController()

        # Llamar configuración contenedor
        self.setup_container_1()
        self.setup_container_2()

        #Llamar configuración Botón Continuar y Regresar
        self.setup_continue_button()
        self.setup_return_button()

    # ------------------------
    # Configurar Contenedores
    # ------------------------
    def setup_container_1(self):
        """Configura el contenedor y sus productos"""
        container_config = {
            'row_height': 40,
            'spacing': 10,
            'show_input': False,
            'show_button': False,
            'show_dividers': True,
            'input_width': 100,
            'button_width': 80,
            'button_text': 'Pedir',
            'text_formatter': lambda item: f"{item['Nombre']} | {item['codigoProducto']}_{item['Date']}_{item['Id']} ({item['cantidad']}{item['unidadMedida']})",
            'item_id_field': 'codigoProducto',
            'margin_top': 5, 
            'margin_bottom': 5,
            'visible_rows': 5,
            'enable_row_selection': False,
            'enable_multiple_row_selection': False
        }

        self.container_1 = Container(
            surface=self.surface,
            ui_manager=self.ui_manager,
            position=(50, 100),
            width=self.window_size[0] - 100,
            config=container_config
        )

        # Configurar productos en contenedor
        products = self.controller.get_products()
        self.container_1.setup_rows(products)  # Corregido: self.container -> self.container_1

    def setup_container_2(self):
        """Configura el contenedor y sus productos"""
        container_config = {
            'row_height': 40,
            'spacing': 10,
            'show_input': False,
            'show_button': False,
            'show_dividers': True,
            'input_width': 100,
            'button_width': 80,
            'button_text': 'Pedir',
            'text_formatter': lambda item: f"{item['Nombre']} | {item['codigoProducto']}_{item['Date']}_{item['Id']} ({item['cantidad']}{item['unidadMedida']}), | Precio: {item['Precio']} col",
            'item_id_field': 'codigoProducto',
            'margin_top': 5, 
            'margin_bottom': 5,
            'visible_rows': 5,
            'enable_row_selection': False,
            'enable_multiple_row_selection': False
        }

        # Calcular posición Y basada en container_1
        position_y = self.container_1.y + self.container_1.height + 20  # 20 pixels de espacio entre contenedores

        self.container_2 = Container(
            surface=self.surface,
            ui_manager=self.ui_manager,
            position=(50, position_y),  # Misma X, nueva Y calculada
            width=self.window_size[0] - 100,
            config=container_config
        )

        # Configurar productos en contenedor
        products = self.controller.get_presale_products()
        self.container_2.setup_rows(products)  # Corregido: self.container -> self.container_2

    def setup_continue_button(self):
        """Configura el botón 'Continuar'"""
        button_x = self.container_1.x + (self.container_1.width - 150) / 2  # Centrar el botón en X
        button_y = self.container_2.y + self.container_2.height + 20  # Debajo del formulario
        self.continue_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(button_x + 200, button_y, 150, 40),  # Ajustar la posición para centrar respecto a los bordes
            text='Continuar',
            manager=self.ui_manager
        )

    def setup_return_button(self):
        """Configura el botón 'Regresar'"""
        button_x = self.container_1.x + (self.container_1.width - 150) / 2  # Centrar el botón en X
        button_y = self.container_2.y + self.container_2.height + 20  # Debajo del formulario
        self.return_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(button_x - 200, button_y, 150, 40),  # Ajustar la posición para centrar respecto a los bordes
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
        self.container_1.handle_event(event, None)
        self.container_2.handle_event(event, None)

        # Manejar evento del botón "Continuar" y "Regresar"
        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.continue_button:
                self.change_screen_callback(Screens.SALE)
            elif event.ui_element == self.return_button:
                self.change_screen_callback(Screens.FACTORY)

    def update(self):
        """Actualiza elementos de la UI"""
        time_delta = pygame.time.Clock().tick(60)/1000.0
        self.ui_manager.update(time_delta)

    def draw(self):
        """Dibuja todos los elementos de la vista"""
        # Fondo principal
        self.surface.fill(COLORS['WHITE'])
        
        # Título
        title_text = self.title_font.render("Materia prima | productos en preventa", True, COLORS['GREEN'])
        title_rect = title_text.get_rect(midtop=(self.window_size[0] // 2, 20))
        self.surface.blit(title_text, title_rect)
        
        # Dibujar elementos UI
        self.container_1.draw()
        self.container_2.draw()
        self.ui_manager.draw_ui(self.surface)
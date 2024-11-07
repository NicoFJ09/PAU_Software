import pygame
import pygame_gui
from Admin_Dashboard.constants import COLORS
from Admin_Dashboard.controllers.Pre_clasification_controller import PreClassificationController
from Admin_Dashboard.views.components.Container import Container
from Admin_Dashboard.views.components.Form import Form
from Admin_Dashboard.Screens import Screens 

class PreClassificationView:
    def __init__(self, surface, window_size, change_screen_callback):
        self.surface = surface
        self.window_size = window_size
        self.ui_manager = pygame_gui.UIManager(window_size)
        self.change_screen_callback = change_screen_callback  # Callback para cambiar la pantalla
        
        # Configuraciones iniciales
        self.setup_ui_theme()
        self.setup_fonts()
        
        # Instanciar Controlador
        self.controller = PreClassificationController()
        
        #Llamar configuración contenedor
        self.setup_container()

        #Llamar configuración formulario
        self.setup_Form()

        #Llamar configuración Botón Continuar
        self.setup_continue_button()

    # ------------------------
    # Configurar Contenedor
    # ------------------------
    def setup_container(self):
        """Configura el contenedor y sus productos"""
        container_config = {
            'row_height': 40,
            'spacing': 10,
            'show_input': True,
            'show_button': True,
            'show_dividers': True,
            'input_width': 100,
            'button_width': 80,
            'button_text': 'Pedir',
            'text_formatter': lambda item: f"{item['nombre']} ({item['unidadMedida']})",
            'item_id_field': 'codigoProducto',
            'margin_top': 5, 
            'margin_bottom': 5,
            'visible_rows': 5,
            'enable_row_selection': False,
            
        }
        
        self.container = Container(
            surface=self.surface,
            ui_manager=self.ui_manager,
            position=(50, 100),
            width=self.window_size[0] - 100,  # Solo pasamos el ancho
            config=container_config
        )

        # Configurar productos en contenedor
        products = self.controller.get_products()
        self.container.setup_rows(products)

    # ------------------------
    # Configurar Formulario
    # ------------------------
    def setup_Form(self):
        self.form = Form(
            container_bottom_y=self.container.y + self.container.height,
            ui_manager=self.ui_manager,
            surface=self.surface,
            config={
                'width': self.container.width,  # Mismo ancho que el container
                'height': self.container.height,  # Mismo alto que el container
                'margin_x': self.container.x,   # Mismo margen que el container
                'dropdown_width': 200,  # Ancho del menú desplegable
                'fields': [
                    {'label': 'Código de producto', 'type': 'text'},
                    {'label': 'Nombre', 'type': 'text'},
                    {'label': 'Unidad de medida', 'type': 'dropdown', 'options': ['Kg', 'U', 'L', 'mL']}
                ],
                'Title_text': 'Añadir productos nuevos'
            }
        )

    def setup_continue_button(self):
        """Configura el botón 'Continuar'"""
        button_x = self.container.x + (self.container.width - 150) / 2  # Centrar el botón en X
        button_y = self.form.y + self.form.height + 20  # Debajo del formulario
        self.continue_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(button_x, button_y, 150, 40),
            text='Continuar',
            manager=self.ui_manager
        )

    def setup_ui_theme(self):
        """Configura el tema de la interfaz"""
        self.default_theme = {
            "text_entry_line": {
                "colours": {
                    "dark_bg": "#FFFFFF",          # Color de fondo base del campo de texto
                    "selected_bg": "#F0F0F0",      # Color de fondo cuando el campo está seleccionado
                    "selected_text": "#F0F0F0",    # Color del texto cuando está seleccionado
                    "normal_text": "#000000",      # Color del texto en estado normal
                    "border": "#B90518",           # Color del borde general
                    "normal_border": "#B90518",    # Color del borde en estado normal
                    "disabled_border": "#B90518",  # Color del borde cuando está deshabilitado
                    "text_cursor": "#000000"       # Color del cursor vertical de escritura
                }
            },
            "drop_down_menu": {
                "colours": {
                    "dark_bg": "#FFFFFF",          # Fondo base blanco
                    "selected_bg": "#FCC509",      # Amarillo al seleccionar (como botón)
                    "normal_bg": "#FFFFFF",        # Fondo normal blanco
                    "hovered_bg": "#F0F0F0",      # Gris claro al hover
                    "normal_text": "#000000",      # Texto negro
                    "selected_text": "#000000",    # Texto negro al seleccionar
                    "hovered_text": "#000000",     # Texto negro al hover
                    "border": "#B90518",           # Borde rojo
                    "normal_border": "#B90518",    # Borde rojo normal
                    "disabled_border": "#B90518",  # Borde rojo deshabilitado
                    "link_text": "#000000",        # Color del texto del menú desplegable
                    "link_hover": "#000000",       # Color del texto al hover en menú
                    "link_selected": "#000000"     # Color del texto seleccionado en menú
                }
            },
            "button": {
                "colours": {
                    "normal_bg": "#FCC509",      # Amarillo normal
                    "hovered_bg": "#FFD43B",     # Amarillo más claro al hover
                    "selected_bg": "#FFDB4D",    # Amarillo más claro al seleccionar
                    "active_bg": "#FCC509",      # Amarillo normal al estar activo
                    "normal_text": "#000000",    # Texto negro
                    "selected_text": "#000000",  # Texto negro al seleccionar
                    "border": "#B90518",         # Borde rojo
                    "normal_border": "#B90518",  # Borde rojo normal
                    "disabled_border": "#B90518" # Borde rojo deshabilitado
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
        self.container.handle_event(event, self.controller.order_product)
        self.form.handle_event(event, self.create_and_update_product)
        
        # Manejar evento del botón "Continuar"
        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.continue_button:
                self.change_screen_callback(Screens.CLASSIFICATION)

    def create_and_update_product(self, codigo, nombre, unidad):
        """Crea un nuevo producto y actualiza el contenedor"""
        # Crear el nuevo producto
        self.controller.create_template(codigo, nombre, unidad)
        
        # Obtener la lista actualizada de productos
        updated_products = self.controller.get_products()
        
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
        title_text = self.title_font.render("Pantalla de pedidos", True, COLORS['GREEN'])
        title_rect = title_text.get_rect(midtop=(self.window_size[0] // 2, 20))
        self.surface.blit(title_text, title_rect)
        
        # Contenedor y elementos UI
        self.container.draw()
        self.form.draw()
        self.ui_manager.draw_ui(self.surface)
import pygame
import pygame_gui
from Admin_Dashboard.constants import COLORS
from Admin_Dashboard.controllers.Classification_controller import ClassificationController
from Admin_Dashboard.views.components.Container import Container
from Admin_Dashboard.views.components.Form import Form
from Admin_Dashboard.Screens import Screens 


class ClassificationView:
    def __init__(self, surface, window_size, change_screen_callback):
        self.surface = surface
        self.window_size = window_size
        self.ui_manager = pygame_gui.UIManager(window_size)
        self.change_screen_callback = change_screen_callback  # Callback para cambiar la pantalla
        
        # Configuraciones iniciales
        self.setup_ui_theme()
        self.setup_fonts()

        # Instanciar Controlador
        self.controller = ClassificationController()

        #Llamar configuración contenedor
        self.setup_container()

        #Llamar configuración formulario
        self.setup_Form()

        self.selected_item = None # Variable para almacenar el item seleccionado
        self.classified_produce = None #Variable temporal que clona selected para llamar controller

        #Llamar configuración Botón Continuar y Regresar
        self.setup_continue_button()
        self.setup_return_button()
        
    # ------------------------
    # Configurar Contenedor
    # ------------------------
    def setup_container(self):
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
            'text_formatter': lambda item: f"{item['codigoProducto']}_{item['Date']}_{item['Id']} ({item['cantidad']}{item['unidadMedida']})",
            'item_id_field': 'codigoProducto',
            'margin_top': 5, 
            'margin_bottom': 5,
            'visible_rows': 5,
            'enable_row_selection': True,
            'enable_multiple_row_selection': False
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
    def setup_Form(self, dropdown_options=None):
        if dropdown_options is None:
            dropdown_options = ['']
        
        # Eliminar el formulario antiguo si existe
        if hasattr(self, 'form'):
            for field in self.form.fields:
                field['input'].kill()
            self.form.submit_button.kill()
        
        self.form = Form(
            container_bottom_y=self.container.y + self.container.height,
            ui_manager=self.ui_manager,
            surface=self.surface,
            config={
                'width': self.container.width,  # Mismo ancho que el container
                'height': self.container.height,  # Mismo alto que el container
                'margin_x': self.container.x,   # Mismo margen que el container
                'dropdown_width': 300,  # Ancho del menú desplegable
                'fields': [
                    {'label': 'Cantidad', 'type': 'number'},
                    {'label': 'Tipo de producto', 'type': 'dropdown', 'options': dropdown_options}
                ],
                'Title_text': 'Escoge y clasifica tus productos'
            }
        )

    def update_form_options(self):
        if self.selected_item:
            codigo_producto = self.selected_item['codigoProducto']
            if codigo_producto == 'PAP':
                dropdown_options = ['Papa pequeña', 'Papa grande', 'Papa dañada']
            elif codigo_producto == 'TOM':
                dropdown_options = ['Tomate verde', 'Tomate maduro', 'Tomate muy maduro grande', 'Tomate muy maduro pequeño', 'Tomate dañado']
            else:
                dropdown_options = ['']  # Opciones por defecto

            # Actualizar el formulario con las nuevas opciones
            self.setup_Form(dropdown_options)
            self.classified_produce = self.selected_item

    def setup_continue_button(self):
        """Configura el botón 'Continuar'"""
        button_x = self.container.x + (self.container.width - 150) / 2  # Centrar el botón en X
        button_y = self.form.y + self.form.height + 20  # Debajo del formulario
        self.continue_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(button_x + 200, button_y, 150, 40),  # Ajustar la posición para centrar respecto a los bordes
            text='Continuar',
            manager=self.ui_manager
        )

    def setup_return_button(self):
        """Configura el botón 'Regresar'"""
        button_x = self.container.x + (self.container.width - 150) / 2  # Centrar el botón en X
        button_y = self.form.y + self.form.height + 20  # Debajo del formulario
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
        selected_item = self.container.handle_event(event, None)
        if selected_item:
            self.selected_item = selected_item
        self.form.handle_event(event, self.classify_and_update_product)

        # Manejar evento del botón "Continuar" y "Regresar"
        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.continue_button:
                self.change_screen_callback(Screens.RECIPE_CREATOR)
            elif event.ui_element == self.return_button:
                self.change_screen_callback(Screens.PRE_CLASSIFICATION)

    def classify_and_update_product(self, cantidad, nombre):
        """Maneja la sumisión del formulario"""
        if self.classified_produce:
            print("Item seleccionado:", self.classified_produce)
            product_id = self.classified_produce['Id']
            date = self.classified_produce['Date']
            unidadMedida = self.classified_produce['unidadMedida']
            codigoProducto = self.classified_produce['codigoProducto']
            try:
                self.controller.classify_product(product_id, float(cantidad), nombre, unidadMedida, date, codigoProducto)
                print(product_id, cantidad, nombre, unidadMedida, date)
                print(f"Producto clasificado: {cantidad} de {nombre}")
                # Obtener la lista actualizada de productos
                updated_products = self.controller.get_products()
                # Actualizar el contenedor con los nuevos productos
                self.container.update(updated_products)
            except ValueError as e:
                print(f"Error al clasificar producto: {e}")
            self.classified_produce = None

    def update(self):
        """Actualiza elementos de la UI"""
        time_delta = pygame.time.Clock().tick(60)/1000.0
        self.ui_manager.update(time_delta)
        
        # Actualizar opciones del formulario si hay un item seleccionado
        if self.selected_item:
            self.update_form_options()
            self.selected_item = None  # Resetear el item seleccionado después de actualizar el formulario

    def draw(self):
        """Dibuja todos los elementos de la vista"""
        # Fondo principal
        self.surface.fill(COLORS['WHITE'])
        
        # Título
        title_text = self.title_font.render("Pantalla de Clasificación", True, COLORS['GREEN'])
        title_rect = title_text.get_rect(midtop=(self.window_size[0] // 2, 20))
        self.surface.blit(title_text, title_rect)
        
        # Dibujar elementos UI
        self.container.draw()
        self.form.draw()
        self.ui_manager.draw_ui(self.surface)
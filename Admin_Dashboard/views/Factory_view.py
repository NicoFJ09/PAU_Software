import pygame
import pygame_gui
from Admin_Dashboard.constants import COLORS
from Admin_Dashboard.controllers.Factory_controller import FactoryController
from Admin_Dashboard.views.components.Container import Container
from Admin_Dashboard.views.components.Craft_form import CraftForm
from Admin_Dashboard.Screens import Screens

class FactoryView:
    def __init__(self, surface, window_size, change_screen_callback):
        self.surface = surface
        self.window_size = window_size
        self.ui_manager = pygame_gui.UIManager(window_size)
        self.change_screen_callback = change_screen_callback
        
        # Configuraciones iniciales
        self.setup_ui_theme()
        self.setup_fonts()

        # Instanciar Controlador
        self.controller = FactoryController()

        # Inicializar variable para almacenar el item seleccionado
        self.material = None

        # Llamar configuración contenedor
        self.setup_container()

        # Llamar configuración formulario
        self.setup_Form()

        #Llamar configuración Botón Continuar y Regresar
        self.setup_continue_button()
        self.setup_return_button()

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
            'text_formatter': lambda item: f"{item['Nombre']} ({item['codigoProducto']})",
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
            width=self.window_size[0] - 100,
            config=container_config
        )

        # Configurar productos en contenedor
        products = self.controller.get_available_recipes()
        self.container.setup_rows(products)

    def setup_Form(self, material=None):
        """Configura el formulario de fabricación"""
        if material:
            material_quantities = self.controller.get_material_quantities(material['Nombre'])
        else:
            material_quantities = {}

        self.craftform = CraftForm(
            container_bottom_y=self.container.y + self.container.height,
            ui_manager=self.ui_manager,
            surface=self.surface,
            material=material,
            material_quantities=material_quantities,
            config={
                'width': self.container.width,
                'height': self.container.height,
                'margin_x': self.container.x,
                'margin_top': 20,
                'margin_bottom': 20,
                'spacing': -20,
                'row_height': 40,
                'button_width': 100,
                'button_text': 'Craft',
                'Title_text': 'Craft Items',
                'material_text_formatter': lambda material, available: f"{material['Nombre']} - {material['cantidad']}{material['unidadMedida']} | Disponible: {available['disponible']}{material['unidadMedida']}"
            }
        )

    def setup_continue_button(self):
        """Configura el botón 'Continuar'"""
        button_x = self.container.x + (self.container.width - 150) / 2  # Centrar el botón en X
        button_y = self.craftform.y + self.craftform.height + 20  # Debajo del formulario
        self.continue_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(button_x + 200, button_y, 150, 40),  # Ajustar la posición para centrar respecto a los bordes
            text='Continuar',
            manager=self.ui_manager
        )

    def setup_return_button(self):
        """Configura el botón 'Regresar'"""
        button_x = self.container.x + (self.container.width - 150) / 2  # Centrar el botón en X
        button_y = self.craftform.y + self.craftform.height + 20  # Debajo del formulario
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
        material = self.container.handle_event(event, None)
        self.craftform.handle_event(event, self.craft_product)
        
        if material and material != self.material:  # Solo actualizar si es un material diferente
            self.material = material
            # Obtener cantidades actualizadas
            material_quantities = self.controller.get_material_quantities(material['Nombre'])
            # Recrear el formulario con el nuevo material
            self.craftform.destroy_form_elements()
            self.craftform = CraftForm(
                container_bottom_y=self.container.y + self.container.height,
                ui_manager=self.ui_manager,
                surface=self.surface,
                material=material,
                material_quantities=material_quantities,
                config={
                    'width': self.container.width,
                    'height': self.container.height,
                    'margin_x': self.container.x,
                    'margin_top': 20,
                    'margin_bottom': 20,
                    'spacing': -20,
                    'row_height': 40,
                    'button_width': 100,
                    'button_text': 'Fabricar',
                    'Title_text': f"Receta de {material['Nombre']}",
                    'material_text_formatter': lambda item, available: f"{item['Nombre']} - {item['cantidad']}{item['unidadMedida']} | Disponible: {available['disponible']}{item['unidadMedida']}"
                }
            )

        # Manejar evento del botón "Continuar" y "Regresar"
        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.continue_button:
                self.change_screen_callback(Screens.PREVIEW)
            elif event.ui_element == self.return_button:
                self.change_screen_callback(Screens.RECIPE_CREATOR)

    def craft_product(self, material, cantidad):
        """Llama a la función del controlador para crear el producto"""
        try:
            new_product = self.controller.craft_product(material['Nombre'], cantidad)
            # Obtener las nuevas cantidades
            material_quantities = self.controller.get_material_quantities(material['Nombre'])
            # Actualizar solo las cantidades en el formulario existente
            self.craftform.update_quantities(material_quantities)
            print(f"Producto creado exitosamente: {new_product}")
        except ValueError as e:
            print(f"Error al crear el producto: {e}")

    def update(self):
        """Actualiza elementos de la UI"""
        time_delta = pygame.time.Clock().tick(60)/1000.0
        self.ui_manager.update(time_delta)

    def draw(self):
        """Dibuja todos los elementos de la vista"""
        # Fondo principal
        self.surface.fill(COLORS['WHITE'])
        
        # Título
        title_text = self.title_font.render("Pantalla de Fabricación", True, COLORS['GREEN'])
        title_rect = title_text.get_rect(midtop=(self.window_size[0] // 2, 20))
        self.surface.blit(title_text, title_rect)
        
        # Dibujar elementos UI
        self.container.draw()
        self.craftform.draw()
        self.ui_manager.draw_ui(self.surface)
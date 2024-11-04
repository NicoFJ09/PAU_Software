import pygame
import pygame_gui
from Admin_Dashboard.constants import COLORS
from Admin_Dashboard.controllers.Pre_clasification_controller import PreClassificationController

class PreClassificationView:

    # ------------------------
    # Constructor de la vista
    # ------------------------
    def __init__(self, surface, window_size):
        self.surface = surface
        self.window_size = window_size
        
        # UI Manager con tema personalizado
        self.ui_manager = pygame_gui.UIManager(window_size)
        
        # Configurar colores personalizados para todos los text entries
        self.default_theme = {
            "text_entry_line": {
                "colours": {
                    "dark_bg": "#FFFFFF",          # Fondo blanco
                    "selected_bg": "#FFFFFF",      # Fondo blanco cuando seleccionado
                    "normal_text": "#000000",      # Texto negro
                    "selected_text": "#000000",    # Texto negro cuando seleccionado
                    "border": "#B90518"           # Borde rojo 
                }
            }
        }
        
        self.ui_manager.get_theme().load_theme(self.default_theme)

        # Fuentes
        self.title_font = pygame.font.SysFont("Georgia", 45)
        self.content_font = pygame.font.SysFont("Georgia", 18)
        
        # Controlador
        self.controller = PreClassificationController()

        # Dimensiones del contenedor
        self.container_width = self.window_size[0] - 100  # Margen de 50px a cada lado
        self.container_height = self.window_size[1] // 2
        self.container_x = 50
        self.container_y = 100

        # Inicializar lista de productos
        self.product_rows = []
        
        # Configurar lista de productos
        self.setup_product_list()


    def setup_product_list(self):
        """Configura lista de productos con sus elementos UI"""
        products = self.controller.get_products()
        
        # Configuración de dimensiones
        row_height = 40
        spacing = 10
        input_width = 100
        button_width = 80
        
        for i, product in enumerate(products):
            y_pos = self.container_y + 20 + (i * (row_height + spacing))
            
            # Texto del producto
            product_text = f"{product['nombre']} ({product['unidadMedida']})"
            text_surface = self.content_font.render(product_text, True, COLORS['YELLOW'])
            text_rect = text_surface.get_rect(
                topleft=(self.container_x + 20, y_pos + row_height//4)
            )
            
            # Input box
            input_rect = pygame.Rect(
                self.container_x + self.container_width - button_width - input_width - 40,
                y_pos,
                input_width,
                row_height
            )
            input_box = pygame_gui.elements.UITextEntryLine(
                relative_rect=input_rect,
                manager=self.ui_manager,
                initial_text="0"  # Texto inicial
            )
            input_box.set_allowed_characters('numbers')  # Solo permite números
            input_box.set_text_length_limit(5)  # Límite de 5 caracteres

            # Botón de orden
            button_rect = pygame.Rect(
                self.container_x + self.container_width - button_width - 20,
                y_pos,
                button_width,
                row_height
            )
            order_button = pygame_gui.elements.UIButton(
                relative_rect=button_rect,
                text='Order',
                manager=self.ui_manager
            )
            
            # Guardar elementos de la fila
            self.product_rows.append({
                'text': text_surface,
                'text_rect': text_rect,
                'input': input_box,
                'button': order_button,
                'product_code': product['codigoProducto']
                
            })

    # ------------------------
    # Manejo de eventos
    # ------------------------
    def handle_event(self, event):
        """Maneja eventos de la vista"""
        self.ui_manager.process_events(event)
        
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                for row in self.product_rows:
                    if event.ui_element == row['button']:
                        amount = int(row['input'].get_text() or "0")
                        if amount > 0:
                            product_code = row['product_code']
                            added_product = self.controller.create_product(product_code, amount)
                            print(f"Producto agregado: {added_product}")
                            row['input'].set_text("0")

    # ------------------------
    # Actualizaciones según eventos
    # ------------------------
    def update(self):
        time_delta = pygame.time.Clock().tick(60)/1000.0
        self.ui_manager.update(time_delta)

    # ------------------------
    # Muestra la vista
    # ------------------------
    def draw(self):

    # Crear título
        self.title_text = self.title_font.render(
            "Pre-Classification Screen", 
            True, 
            COLORS['GREEN']
        )
        self.title_rect = self.title_text.get_rect(
            midtop=(self.window_size[0] // 2, 20)
        )

        # Fondo principal
        self.surface.fill(COLORS['WHITE'])
        
        # Contenedor principal
        pygame.draw.rect(
            self.surface,
            (COLORS['GREEN']),
            (self.container_x, self.container_y, self.container_width, self.container_height)
        )
        
        # Borde
        pygame.draw.rect(
            self.surface,
            (COLORS['RED']),
            (self.container_x, self.container_y, self.container_width, self.container_height),
            2
        )
        
        # Título
        self.surface.blit(self.title_text, self.title_rect)
        
        # Dibujar filas de productos
        for row in self.product_rows:
            self.surface.blit(row['text'], row['text_rect'])
        
        # Dibujar elementos UI
        self.ui_manager.draw_ui(self.surface)
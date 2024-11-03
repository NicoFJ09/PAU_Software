import pygame
from utils.screen_config import PYGAME_CONFIG, COLORS
from .Components.Button import Button
from .Components.Input_box import InputBox
from .Components.Form import Form  
from Admin_Dashboard.controllers.Pre_clasification_controller import PreClassificationController

class PreClassificationView:
    def __init__(self, surface, window_size):
        self.surface = surface
        self.window_size = window_size
        
        # Fuentes
        self.title_font = pygame.font.SysFont(
            PYGAME_CONFIG['font']['name'], 
            PYGAME_CONFIG['font']['size'] + 10
        )
        self.content_font = pygame.font.SysFont(
            PYGAME_CONFIG['font']['name'], 
            PYGAME_CONFIG['font']['size']
        )
        
        # Título
        self.title_text = self.title_font.render(
            "Pre-Classification Screen", 
            True, 
            COLORS['BLACK']
        )
        self.title_rect = self.title_text.get_rect(
            midtop=(self.window_size[0] // 2, 20)
        )
        
        # Área de contenido
        self.content_area = pygame.Rect(
            50,  # x
            100, # y
            self.window_size[0] - 100,  # ancho
            200 # altura fija más pequeña
        )

        # Área del formulario con más espacio
        spacing = 30  # Aumentar el espaciado entre contenedores

        self.form_header = self.title_font.render(
            "Add New Products",
            True,
            COLORS['BLACK']
        )
        self.form_header_rect = self.form_header.get_rect(
            topleft=(50, self.content_area.bottom + spacing -15)
        )

        self.form_area = pygame.Rect(
            50,  # x
            self.content_area.bottom + 30 + spacing,  # y (30px debajo del content_area)
            self.window_size[0] - 100,  # ancho
            250  # altura para el formulario
        )


        form_fields = ['Código Producto', 'Nombre', 'Unidad Medida']
        self.product_form = Form(
            self.form_area.left + 10,
            self.form_area.top + 10,
            self.form_area.width - 20,
            self.form_area.height - 20,
            form_fields
        )

        
        # Inicializar listas vacías para UI elements
        self.input_boxes = []
        self.buttons = []
        self.product_texts = []
        
        # Controlador y productos
        self.controller = PreClassificationController()
        self.products = self.controller.get_products()
        self.create_product_texts()
    

    def create_product_texts(self):
        y_offset = self.content_area.top + 10
        
        for product in self.products:
            # Texto del producto
            product_text = f"{product['nombre']} ({product['unidadMedida']})"
            text = self.content_font.render(product_text, True, COLORS['BLACK'])
            rect = text.get_rect(topleft=(self.content_area.left + 10, y_offset))
            self.product_texts.append((text, rect))
            
            # Input box más ancho (120 en lugar de 60)
            input_box = InputBox(rect.right + 20, y_offset, 120, 30)
            self.input_boxes.append(input_box)
            
            # Botón
            button = Button(input_box.rect.right + 20, y_offset, 100, 30, "ORDER")
            self.buttons.append(button)
            
            y_offset += 40
    
    def handle_event(self, event):
        # Manejar eventos existentes
        for input_box, button in zip(self.input_boxes, self.buttons):
            input_box.handle_event(event)
            if button.handle_event(event):
                text = input_box.get_text()
                print(f"Texto capturado: {text}")
                input_box.clear()

        # Manejar eventos del formulario
        result = self.product_form.handle_event(event)
        if result:  # result es una lista de valores
            print(f"Valores del formulario: {result}")
    
    def draw(self):
        self.surface.fill(COLORS['WHITE'])
        
        # Dibujar área de contenido existente
        pygame.draw.rect(self.surface, COLORS['GRAY'], self.content_area, 2)
        self.surface.blit(self.title_text, self.title_rect)
        
        for (text, rect), input_box, button in zip(self.product_texts, self.input_boxes, self.buttons):
            self.surface.blit(text, rect)
            input_box.draw(self.surface)
            button.draw(self.surface)

        # Dibujar área del formulario
        pygame.draw.rect(self.surface, COLORS['GRAY'], self.form_area, 2)
        self.surface.blit(self.form_header, self.form_header_rect)
        self.product_form.draw(self.surface)

    def update(self):
        """Actualizar elementos de la vista"""
    pass

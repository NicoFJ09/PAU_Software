import pygame
import pygame_gui
from Admin_Dashboard.constants import COLORS
from Admin_Dashboard.views.components.ScrollBar import Scrollbar

class Container:
    def __init__(self, surface, ui_manager, position, width, config=None):
        self.surface = surface
        self.ui_manager = ui_manager
        self.x, self.y = position
        self.width = width
        
        # Configuración por defecto
        self.config = {
            'row_height': 40,
            'spacing': 10,
            'show_input': True,
            'show_button': True,
            'show_dividers': True,
            'input_width': 100,
            'button_width': 80,
            'button_text': 'Order',
            'text_formatter': lambda item: f"{item['Nombre']} ({item['unidadMedida']})",
            'item_id_field': 'codigoProducto',
            'margin_top': 20,
            'margin_bottom': 20,
            'visible_rows': 5,
            'enable_row_selection': True,
            'enable_multiple_row_selection': False
        }
        if config:
            self.config.update(config)
        
        # Calcular altura inicial del contenedor
        self.height = ( 
            self.config['margin_top'] +
            (self.config['visible_rows'] * self.config['row_height']) +
            ((self.config['visible_rows'] - 1) * self.config['spacing']) +
            self.config['margin_bottom']
        )
        
        self.content_font = pygame.font.SysFont("Georgia", 18)
        self.rows = []
        self.scrollbar = None
        self.scroll_index = 0
        self.selected_items = []  # Lista de elementos seleccionados

    def create_row(self, item, index):
        """Crea una fila con elementos configurables"""
        y_pos = self.y + self.config['margin_top'] + (index * (self.config['row_height'] + self.config['spacing']))
        row_data = {
            'selected': False  # Estado de selección
        }
        
        # Texto del item - centrado verticalmente en la fila
        text = self.config['text_formatter'](item)
        text_surface = self.content_font.render(text, True, COLORS['YELLOW'])
        text_rect = text_surface.get_rect(
            topleft=(self.x + 20, y_pos + (self.config['row_height'] - text_surface.get_height()) // 2)
        )
        row_data.update({
            'text': text_surface,
            'text_rect': text_rect,
            'item': item,  # Guardar el item completo
            'row_rect': pygame.Rect(self.x, y_pos, self.width, self.config['row_height'])  # Área clicable de la fila
        })
        
        # Input box (opcional)
        if self.config['show_input']:
            input_rect = pygame.Rect(
                self.x + self.width - self.config['button_width'] - self.config['input_width'] - 40,
                y_pos,
                self.config['input_width'],
                self.config['row_height']
            )
            input_box = pygame_gui.elements.UITextEntryLine(
                relative_rect=input_rect,
                manager=self.ui_manager,
                placeholder_text="Cantidad de producto"
            )
            row_data['input'] = input_box
        
        # Botón (opcional)
        if self.config['show_button']:
            button_rect = pygame.Rect(
                self.x + self.width - self.config['button_width'] - 20,
                y_pos,
                self.config['button_width'],
                self.config['row_height']
            )
            button = pygame_gui.elements.UIButton(
                relative_rect=button_rect,
                text=self.config['button_text'],
                manager=self.ui_manager
            )
            row_data['button'] = button
        
        return row_data

    def handle_row_click(self, event):
        """Maneja el clic en una fila para cambiar su color de fondo y mostrar sus propiedades"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            container_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            
            # Verificar si el clic ocurrió dentro del área del contenedor
            if not container_rect.collidepoint(mouse_pos):
                return None  # No hacer nada si el clic fue fuera del contenedor
            
            for i, row in enumerate(self.rows):
                # Calcular la posición Y de la fila teniendo en cuenta el desplazamiento
                y_pos = self.y + self.config['margin_top'] + ((i - self.scroll_index) * (self.config['row_height'] + self.config['spacing']))
                row_rect = pygame.Rect(self.x, y_pos, self.width, self.config['row_height'])
                
                # Verificar si el clic ocurrió dentro del área del input
                if 'input' in row and row['input'].relative_rect.collidepoint(mouse_pos):
                    return None  # No hacer nada si el clic fue en el input
                
                if row_rect.collidepoint(mouse_pos):
                    if self.config['enable_multiple_row_selection']:
                        row['selected'] = not row['selected']
                    else:
                        # Deseleccionar todas las filas
                        for r in self.rows:
                            r['selected'] = False
                        # Seleccionar la fila actual
                        row['selected'] = True
                    return row['item']  # Retornar propiedades del producto
        return None

    def get_selected_items(self):
        """Actualiza y retorna la lista de elementos seleccionados con sus cantidades"""
        self.selected_items = []
        for row in self.rows:
            if row['selected']:
                try:
                    cantidad = float(row['input'].get_text() or "0") if 'input' in row else 0.0
                except ValueError:
                    cantidad = 0.0  # Valor por defecto si la conversión falla
                item_with_cantidad = row['item'].copy()
                item_with_cantidad['cantidad'] = cantidad
                self.selected_items.append(item_with_cantidad)
        print("Elementos seleccionados:", self.selected_items)
        return self.selected_items

    def setup_rows(self, items):
        """Configura todas las filas y ajusta la altura del contenedor"""
        # Crear todas las filas
        self.rows = [
            self.create_row(item, i) 
            for i, item in enumerate(items)
        ]
        
        # Altura fija para las filas visibles
        self.height = (
            self.config['margin_top'] +
            (self.config['visible_rows'] * self.config['row_height']) +
            ((self.config['visible_rows'] - 1) * self.config['spacing']) +
            self.config['margin_bottom']
        )
        
        # Crear scrollbar si hay más filas que el límite visible
        if len(self.rows) > self.config['visible_rows']:
            self.scrollbar = Scrollbar(
                x=self.x + self.width + 2,  # 5px de separación del contenedor
                y=self.y,
                width=10,  # Scrollbar más delgado
                height=self.height,
                total_items=len(self.rows),
                visible_items=self.config['visible_rows']
            )
            
            # Simular scroll inicial para forzar actualización
            self.scroll_index = 1
            self.update_visible_elements()
            self.scroll_index = 0
            self.update_visible_elements()

    def update(self, items):
        """Actualiza las filas del contenedor con nuevos elementos"""
        # Eliminar filas existentes
        for row in self.rows:
            if 'input' in row:
                row['input'].kill()
            if 'button' in row:
                row['button'].kill()
        
        # Configurar filas nuevamente con la lista actualizada de productos
        self.setup_rows(items)

    def reset(self):
        """Reinicia las filas del contenedor utilizando los mismos elementos actuales"""
        # Obtener los elementos actuales
        items = [row['item'] for row in self.rows]
        
        # Eliminar filas existentes
        for row in self.rows:
            if 'input' in row:
                row['input'].kill()
            if 'button' in row:
                row['button'].kill()
        
        # Configurar filas nuevamente con los mismos elementos
        self.setup_rows(items)

    def update_visible_elements(self):
        """Actualiza la posición de los elementos según el scroll sin ocultarlos"""
        for i, row in enumerate(self.rows):
            y_pos = self.y + self.config['margin_top'] + ((i - self.scroll_index) * (self.config['row_height'] + self.config['spacing']))
            
            # Determinar si el elemento está visible
            is_visible = (y_pos >= self.y and 
                        y_pos + self.config['row_height'] <= self.y + self.height)
            
            # Actualizar posición de elementos UI solo si son visibles
            if is_visible:
                if 'input' in row:
                    row['input'].set_relative_position((
                        row['input'].relative_rect.x,
                        y_pos
                    ))
                if 'button' in row:
                    row['button'].set_relative_position((
                        row['button'].relative_rect.x,
                        y_pos
                    ))
            else:
                # Mover elementos fuera de la vista en lugar de ocultarlos
                if 'input' in row:
                    row['input'].set_relative_position((
                        row['input'].relative_rect.x,
                        -1000  # Fuera de la vista
                    ))
                if 'button' in row:
                    row['button'].set_relative_position((
                        row['button'].relative_rect.x,
                        -1000  # Fuera de la vista
                    ))

    def draw_dividers(self):
        """Dibuja líneas divisorias centradas entre las filas"""
        if not self.config['show_dividers'] or len(self.rows) <= 1:
            return
            
        visible_rows = self.rows[self.scroll_index:self.scroll_index + self.config['visible_rows']]
        for i in range(len(visible_rows) - 1):
            # Calcular posición Y del elemento actual y siguiente
            current_row_y = self.y + self.config['margin_top'] + (i + 1) * (self.config['row_height'] + self.config['spacing']) - self.config['spacing'] // 2
            
            # Dibujar línea divisoria
            pygame.draw.line(
                self.surface,
                COLORS['RED'],
                (self.x, current_row_y),
                (self.x + self.width - 1, current_row_y),
                2
            )

    def draw(self):
        """Dibuja el contenedor y sus elementos"""
        pygame.draw.rect(
            self.surface,
            COLORS['GREEN'],
            (self.x, self.y, self.width, self.height)
        )
        pygame.draw.rect(
            self.surface,
            COLORS['RED'],
            (self.x, self.y, self.width, self.height),
            2
        )
        
        self.update_visible_elements()
        
        visible_rows = self.rows[self.scroll_index:self.scroll_index + self.config['visible_rows']]
        for i, row in enumerate(visible_rows):
            y_pos = self.y + self.config['margin_top'] + (i * (self.config['row_height'] + self.config['spacing']))
            
            if y_pos >= self.y and y_pos + self.config['row_height'] <= self.y + self.height:
                if row['selected']:
                    pygame.draw.rect(
                        self.surface,
                        COLORS['LIGHT_GREEN'],  # Color de fondo para la fila seleccionada
                        (self.x, y_pos, self.width, self.config['row_height'])
                    )
                text_rect = row['text_rect'].copy()
                text_rect.y = y_pos + (self.config['row_height'] - row['text'].get_height()) // 2
                self.surface.blit(row['text'], text_rect)
        
        self.draw_dividers()
        
        if self.scrollbar:
            self.scrollbar.draw(self.surface)

    def handle_event(self, event, callback):
        """Maneja eventos si hay botones configurados"""
        if self.scrollbar:
            new_index = self.scrollbar.handle_event(event)
            if new_index is not None:
                self.scroll_index = new_index
                return
        
        if self.config['enable_row_selection'] or self.config['enable_multiple_row_selection']:
            selected_item = self.handle_row_click(event)
            if selected_item:
                return selected_item
        
        if not self.config['show_button']:
            return
            
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                for row in self.rows:
                    if event.ui_element == row['button']:
                        if self.config['show_input']:
                            try:
                                amount = float(row['input'].get_text() or "0")
                            except ValueError:
                                amount = 0.0
                            if amount > 0:
                                callback(row['item'][self.config['item_id_field']], amount)
                                row['input'].set_text("0")
                        else:
                            callback(row['item'][self.config['item_id_field']])
            elif event.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                for row in self.rows:
                    if event.ui_element == row.get('input'):
                        break
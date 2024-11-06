from datetime import datetime
from Admin_Dashboard.utils.file_handler import FileHandler

class ClassifiedProductService:
    
    def __init__(self):
        """Inicializa el servicio con manejadores de archivos"""
        self.product_handler = FileHandler("products")
        self.template_handler = FileHandler("produce_templates")
    
    def classify_product(self, lote_id: int, cantidad: float, new_codigo: str, date: str) -> dict:
        """
        Clasifica una cantidad de un lote específico en un nuevo tipo de producto.
        """
        products = self.product_handler.read_file()
        templates = self.template_handler.read_file()

        # Buscar el lote específico primero
        lote = next((p for p in products if p['Id'] == lote_id and p['Date'] == date and p['codigoProducto'] in ('TOM', 'PAP')), None)
        if not lote:
            raise ValueError(f"Lote con ID {lote_id}, fecha {date} y código de producto TOM o PAP no encontrado.")

        if lote['cantidad'] < cantidad:
            raise ValueError(f"Cantidad insuficiente en el lote. Disponible: {lote['cantidad']}, Solicitado: {cantidad}")

        # Buscar la plantilla del nuevo producto
        template = next((t for t in templates if t['codigoProducto'] == new_codigo), None)
        if not template:
            raise ValueError(f"Plantilla con código {new_codigo} no encontrada.")

        # Actualizar la cantidad del lote original
        lote['cantidad'] -= cantidad

        # Verificar si ya existe un lote con el mismo Id, Date y codigoProducto
        current_date = datetime.now().strftime('%Y-%m-%d')
        existing_lote = next((p for p in products 
                            if p['Id'] == lote_id 
                            and p['codigoProducto'] == new_codigo 
                            and p['Date'] == current_date), None)
        
        if existing_lote:
            # Sumar la cantidad al lote existente
            existing_lote['cantidad'] += cantidad
        else:
            # Crear el nuevo lote clasificado
            new_lote = {
                "codigoProducto": new_codigo,
                "nombre": template['nombre'],
                "unidadMedida": template['unidadMedida'],
                "Date": current_date,
                "cantidad": cantidad,
                "Id": lote_id
            }
            # Añadir el nuevo lote al archivo de productos
            products.append(new_lote)

        # Guardar los cambios en los archivos JSON
        self.product_handler.write_file(products)

        return existing_lote if existing_lote else new_lote

    def get_lotes(self):
        """
        Retorna todos los lotes con código TOM o PAP y cantidad mayor a 0.
        """
        products = self.product_handler.read_file()
        filtered_products = [p for p in products if p['codigoProducto'] in ('TOM', 'PAP') and p['cantidad'] > 0]
        return filtered_products

    def get_new_product_types(self, insumo: str):
        """
        Retorna todos los tipos de productos basados en el insumo.
        """
        templates = self.template_handler.read_file()
        filtered_templates = [t for t in templates if t['insumo'] == insumo]
        return filtered_templates

    def select_lote(self, lote_id: int, date: str, codigo_producto: str):
        """
        Selecciona un lote específico basado en ID, fecha y código de producto.
        """
        products = self.product_handler.read_file()
        selected_lote = next((p for p in products if p['Id'] == lote_id and p['Date'] == date and p['codigoProducto'] == codigo_producto), None)
        if not selected_lote:
            raise ValueError(f"Lote con ID {lote_id}, fecha {date} y código de producto {codigo_producto} no encontrado.")
        return selected_lote
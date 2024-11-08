from datetime import datetime
from Admin_Dashboard.utils.file_handler import FileHandler

class ClassifyProductService:
    
    def __init__(self):
        """Inicializa el servicio con manejadores de archivos"""
        self.product_handler = FileHandler("products")
        self.template_handler = FileHandler("produce_templates")
    
    def classify_product(self, product_id: int, cantidad: float, nombre: str, unidadMedida:str, date: str, codigo_Producto: str) -> dict:
        """
        Clasifica una cantidad de un producto específico en un nuevo tipo de producto.
        """
        products = self.product_handler.read_file()
        templates = self.template_handler.read_file()

        # Buscar el producto específico primero
        product = next((p for p in products if p['Id'] == product_id and p['Date'] == date and p['codigoProducto']==codigo_Producto in ('TOM', 'PAP')), None)
        if not product:
            raise ValueError(f"Producto con ID {product_id}, fecha {date} y código de producto TOM o PAP no encontrado.")

        if product['cantidad'] < cantidad:
            raise ValueError(f"Cantidad insuficiente en el producto. Disponible: {product['cantidad']}, Solicitado: {cantidad}")

        # Buscar la plantilla del nuevo producto utilizando el nombre
        template = next((t for t in templates if t["Nombre"] == nombre), None)
        if not template:
            raise ValueError(f"Plantilla con nombre {nombre} no encontrada.")

        # Obtener el codigoProducto desde la plantilla
        new_codigo = template['codigoProducto']

        # Actualizar la cantidad del producto original
        product['cantidad'] -= cantidad

        # Verificar si ya existe un producto con el mismo Id, Date y codigoProducto
        current_date = datetime.now().strftime('%Y-%m-%d')
        existing_product = next((p for p in products 
                            if p['Id'] == product_id 
                            and p['codigoProducto'] == new_codigo 
                            and p['Date'] == current_date), None)
        
        if existing_product:
            # Sumar la cantidad al producto existente
            existing_product['cantidad'] += cantidad
        else:
            # Crear el nuevo producto clasificado
            new_product = {
                "codigoProducto": new_codigo,
                "Nombre": nombre,
                "unidadMedida": unidadMedida,
                "Date": current_date,
                "cantidad": cantidad,
                "Id": product_id
            }
            # Añadir el nuevo producto al archivo de productos
            products.append(new_product)

        # Eliminar productos con cantidad 0
        products = [p for p in products if p['cantidad'] > 0]

        # Guardar los cambios en los archivos JSON
        self.product_handler.write_file(products)

        return existing_product if existing_product else new_product

    def get_products(self):
        """
        Retorna todos los productos con código TOM o PAP y cantidad mayor a 0.
        """
        products = self.product_handler.read_file()
        filtered_products = [p for p in products if p['codigoProducto'] in ('TOM', 'PAP') and p['cantidad'] > 0]
        return filtered_products
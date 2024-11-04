from Admin_Dashboard.utils.file_handler import FileHandler
from datetime import datetime
from Admin_Dashboard.models.Product import REQUIRED_PRODUCT_FIELDS

class ProductService:
    
    # ------------------------
    # Constructor de servicio (acceso a carpeta)
    # ------------------------
    def __init__(self):
        """Inicializa el servicio con manejadores de archivos"""
        self.product_handler = FileHandler("products")
        self.template_handler = FileHandler("product_templates")
    
    # ------------------------
    # Generación de IDs según fecha y lote
    # ------------------------
    def _generate_id(self, products: list, new_product: dict) -> int:
        """
        Genera ID único basado en fecha y código de producto
        El ID se incrementa si ya existen productos con la misma fecha y código
        """
        matching_products = [
            p for p in products 
            if p["codigoProducto"] == new_product["codigoProducto"] 
            and p["Date"] == new_product["Date"]
        ]
        return 1 if not matching_products else max(p["Id"] for p in matching_products) + 1

    # ------------------------
    # Validaciones
    # ------------------------
    def validate_date(self, date_str: str) -> bool:
        """Valida formato de fecha"""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD")
    
    def validate_quantity(self, cantidad: float) -> bool:
        """Valida que la cantidad sea positiva"""
        if not isinstance(cantidad, (int, float)) or cantidad <= 0:
            raise ValueError("La cantidad debe ser un número positivo")
        return True

    # ------------------------
    # Operaciones de templates
    # ------------------------
    def get_available_templates(self) -> list:
        """Obtiene lista de templates disponibles"""
        templates = self.template_handler.read_file()
        if not templates:
            raise ValueError("No hay templates disponibles")
        return templates
    
    def get_template_by_code(self, codigo: str) -> dict:
        """Obtiene template por código de producto"""
        templates = self.template_handler.read_file()
        template = next((t for t in templates if t["codigoProducto"] == codigo.upper()), None)
        if not template:
            raise ValueError(f"No existe template con código {codigo}")
        return template

    # ------------------------
    # Operaciones de productos
    # ------------------------
    def get_product_by_id(self, product_id: int) -> dict:
        """Busca un producto específico por ID"""
        products = self.product_handler.read_file()
        return next((p for p in products if p["Id"] == product_id), None)

    def order_product(self, codigo: str, cantidad: float) -> dict:
        """
        Crea un nuevo producto a partir de template y parámetros
        :param codigo: Código del producto
        :param cantidad: Cantidad del producto
        :return: Producto creado
        """
        fecha = datetime.now().strftime("%Y-%m-%d")
        self.validate_date(fecha)
        self.validate_quantity(cantidad)
        template = self.get_template_by_code(codigo)
        
        product_data = {
            "codigoProducto": template["codigoProducto"],
            "nombre": template["nombre"],
            "unidadMedida": template["unidadMedida"],
            "Date": fecha,
            "cantidad": float(cantidad)
        }
        
        return self.add_product(product_data)

    def add_product(self, product_data: dict) -> dict:
        """
        Agrega un nuevo producto al archivo
        Valida campos requeridos y genera ID único
        :param product_data: Diccionario con datos del producto
        :return: Producto agregado con ID generado
        """
        products = self.product_handler.read_file()
        
        # Validación de campos requeridos
        if not all(field in product_data for field in REQUIRED_PRODUCT_FIELDS):
            raise ValueError("Faltan campos requeridos: codigoProducto, nombre, unidadMedida, Date, cantidad")
        
        # Generación de ID y agregado del producto
        product_data["Id"] = self._generate_id(products, product_data)
        products.append(product_data)
        self.product_handler.write_file(products)
        
        return product_data
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.file_handler import FileHandler
from datetime import datetime
from constants import REQUIRED_PRODUCT_FIELDS

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
        
        if not matching_products:
            return 1
        
        max_id = max(p["Id"] for p in matching_products)
        return max_id + 1

    # ------------------------
    # Operaciones públicas
    # ------------------------
    def get_all_products(self) -> list:
        """Obtiene lista de todos los productos"""
        return self.product_handler.read_file()

    def get_product_by_id(self, product_id: int) -> dict:
        """
        Busca un producto específico por ID
        :param product_id: ID del producto a buscar
        :return: Producto encontrado o None
        """
        products = self.product_handler.read_file()
        return next((p for p in products if p["Id"] == product_id), None)

    def add_product_interactive(self):
        """Proceso interactivo de creación de producto"""
        try:
            print("\n=== Agregar Nuevo Producto ===")
            
            # Mostrar templates disponibles
            templates = self.template_handler.read_file()
            if not templates:
                print("No hay templates disponibles. Cree algunos primero.")
                return
            
            print("\nProductos disponibles:")
            for template in templates:
                print(f"- {template['codigoProducto']}: {template['descripcion']} ({template['unidadMedida']})")
            
            # Seleccionar template
            codigo = input("\nIngrese código del producto: ").strip().upper()
            template = next((t for t in templates if t["codigoProducto"] == codigo), None)
            if not template:
                raise ValueError(f"No existe template con código {codigo}")
            
            # Solicitar datos adicionales
            fecha = input("Fecha (YYYY-MM-DD): ").strip()
            try:
                datetime.strptime(fecha, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD")
            
            cantidad = input("Cantidad: ").strip()
            try:
                cantidad = float(cantidad)
                if cantidad <= 0:
                    raise ValueError()
            except ValueError:
                raise ValueError("La cantidad debe ser un número positivo")
            
            # Crear producto
            product_data = {
                "codigoProducto": template["codigoProducto"],
                "descripcion": template["descripcion"],
                "unidadMedida": template["unidadMedida"],
                "Date": fecha,
                "cantidad": cantidad
            }
            
            # Agregar producto
            added_product = self.add_product(product_data)
            print(f"\nProducto agregado exitosamente:")
            print(f"ID: {added_product['Id']}")
            print(f"Producto: {added_product['descripcion']}")
            print(f"Cantidad: {added_product['cantidad']} {added_product['unidadMedida']}")
            print(f"Fecha: {added_product['Date']}")
            
        except ValueError as e:
            print(f"\nError: {str(e)}")
        except Exception as e:
            print(f"\nError inesperado: {str(e)}")

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
            raise ValueError("Faltan campos requeridos: codigoProducto, descripcion, unidadMedida, Date, cantidad")
        
        # Generación de ID y agregado del producto
        product_data["Id"] = self._generate_id(products, product_data)
        products.append(product_data)
        self.product_handler.write_file(products)
        
        return product_data

# Ejemplo de uso actualizado
if __name__ == "__main__":
    service = ProductService()
    while True:
        service.add_product_interactive()
        
        continuar = input("\n¿Desea agregar otro producto? (s/n): ").lower()
        if continuar != 's':
            break
    
    print("\nProductos guardados. ¡Hasta luego!")
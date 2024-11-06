import os
import sys

# Obtener la ruta absoluta del directorio raíz del proyecto
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(PROJECT_ROOT)
from datetime import datetime
from Admin_Dashboard.utils.file_handler import FileHandler

class ClassifiedProductServiceTest:
    
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
        lote = next((p for p in products if p['Id'] == lote_id and p['Date'] == date), None)
        if not lote:
            raise ValueError(f"Lote con ID {lote_id} y fecha {date} no encontrado.")

        # Verificar que el lote sea de tipo TOM o PAP
        if lote['codigoProducto'] not in ('TOM', 'PAP'):
            raise ValueError(f"El lote debe ser de tipo TOM o PAP. Tipo actual: {lote['codigoProducto']}")

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

    def select_lote(self):
        """
        Permite al usuario seleccionar un lote con código TOM o PAP.
        """
        products = self.product_handler.read_file()
        filtered_products = [p for p in products if p['codigoProducto'] in ('TOM', 'PAP')]
        if not filtered_products:
            print("No hay lotes disponibles con código TOM o PAP.")
            return None

        # Mostrar opciones al usuario
        print("\nSeleccione un lote:")
        for idx, product in enumerate(filtered_products, start=1):
            print(f"{idx}. ID: {product['Id']}, Código: {product['codigoProducto']}, "
                  f"Nombre: {product['nombre']}, Cantidad: {product['cantidad']} {product['unidadMedida']}, Fecha: {product['Date']}")

        # Pedir al usuario que seleccione un lote
        try:
            selected_idx = int(input("\nIngrese el número del lote que desea seleccionar: ")) - 1
            if selected_idx < 0 or selected_idx >= len(filtered_products):
                print("Selección inválida.")
                return None
            selected_lote = filtered_products[selected_idx]
            # Asegurarnos de que el ID del lote seleccionado se use correctamente
            return {
                'Id': selected_lote['Id'],
                'codigoProducto': selected_lote['codigoProducto'],
                'nombre': selected_lote['nombre'],
                'cantidad': selected_lote['cantidad'],
                'unidadMedida': selected_lote['unidadMedida'],
                'Date': selected_lote['Date']
            }
        except ValueError:
            print("Por favor ingrese un número válido.")
            return None

    def select_new_product_type(self, insumo: str):
        """
        Permite al usuario seleccionar un nuevo tipo de producto basado en el insumo.
        """
        templates = self.template_handler.read_file()
        filtered_templates = [t for t in templates if t['insumo'] == insumo]
        if not filtered_templates:
            print(f"No hay plantillas disponibles para el insumo {insumo}.")
            return None

        # Mostrar opciones al usuario
        print(f"\nSeleccione un nuevo tipo de producto para el insumo {insumo}:")
        for idx, template in enumerate(filtered_templates, start=1):
            print(f"{idx}. Código: {template['codigoProducto']}, Nombre: {template['nombre']}")

        # Pedir al usuario que seleccione un nuevo tipo de producto
        try:
            selected_idx = int(input("\nIngrese el número del nuevo tipo de producto que desea seleccionar: ")) - 1
            if selected_idx < 0 or selected_idx >= len(filtered_templates):
                print("Selección inválida.")
                return None
            return filtered_templates[selected_idx]['codigoProducto']
        except ValueError:
            print("Por favor ingrese un número válido.")
            return None

# Ejemplo de uso
if __name__ == "__main__":
    handler = ClassifiedProductServiceTest()
    selected_lote = handler.select_lote()
    if selected_lote:
        try:
            # Usamos el ID correcto del lote seleccionado
            lote_id = selected_lote['Id']
            date = selected_lote['Date']
            cantidad = float(input(f"\nIngrese la cantidad a clasificar del lote ID {lote_id}: "))
            new_codigo = handler.select_new_product_type(selected_lote['codigoProducto'])
            if new_codigo:
                new_lote = handler.classify_product(lote_id=lote_id, cantidad=cantidad, new_codigo=new_codigo, date=date)
                print("\nNuevo lote clasificado:", new_lote)
        except ValueError as e:
            print("\nError:", e)
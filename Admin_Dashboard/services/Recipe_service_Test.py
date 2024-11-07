import os
import sys

# Obtener la ruta absoluta del directorio raíz del proyecto
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(PROJECT_ROOT)
from datetime import datetime
from Admin_Dashboard.utils.file_handler import FileHandler

class RecipeServiceTest:
    
    def __init__(self):
        """Inicializa el servicio con manejador de archivos"""
        self.product_templates_handler = FileHandler("Product_Templates.json")
        self.produce_templates_handler = FileHandler("Produce_Templates.json")
        self.recipes_handler = FileHandler("recipes.json")
    
    def get_available_products(self) -> list:
        """Obtiene todos los productos de ambos templates excepto los que tienen CodigoProducto igual a PAP o TOM"""
        product_templates = self.product_templates_handler.read_file()
        produce_templates = self.produce_templates_handler.read_file()
        
        combined_products = product_templates + produce_templates
        return [p for p in combined_products if p["codigoProducto"] not in ["PAP", "TOM"]]
    
    def create_recipe(self):
        """Crea una nueva receta y la guarda en Recipes.json"""
        available_products = self.get_available_products()
        
        print("Seleccione los productos para la receta:")
        selected_products = []
        while True:
            for i, product in enumerate(available_products):
                print(f"{i + 1}. {product['Nombre']} ({product['codigoProducto']})")
            
            choice = input("Ingrese el número del producto (o 'done' para finalizar): ")
            if choice.lower() == 'done':
                break
            
            try:
                index = int(choice) - 1
                if 0 <= index < len(available_products):
                    cantidad = float(input(f"Ingrese la cantidad para {available_products[index]['Nombre']}: "))
                    selected_product = available_products[index].copy()
                    selected_product["cantidad"] = cantidad
                    selected_products.append(selected_product)
                else:
                    print("Selección inválida, intente nuevamente.")
            except ValueError:
                print("Entrada inválida, intente nuevamente.")
        
        codigo_producto = input("Ingrese el código del nuevo producto: ")
        nombre = input("Ingrese el nombre del nuevo producto: ")
        precio = float(input("Ingrese el precio del nuevo producto: "))
        
        new_recipe = {
            "codigoProducto": codigo_producto,
            "Nombre": nombre,
            "Precio": precio,
            "materiales": [
                {
                    "codigoMaterial": p["codigoProducto"],
                    "descripcion": p["Nombre"],
                    "cantidad": p["cantidad"],
                    "unidadMedida": p["unidadMedida"]
                } for p in selected_products
            ]
        }
        
        recipes = self.recipes_handler.read_file()
        recipes.append(new_recipe)
        self.recipes_handler.write_file(recipes)
        
        print("Receta creada y guardada exitosamente.")

def main():
    service = RecipeServiceTest()
    service.create_recipe()

if __name__ == "__main__":
    main()
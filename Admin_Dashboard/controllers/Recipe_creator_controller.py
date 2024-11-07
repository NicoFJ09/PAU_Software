import os
import sys

# Obtener la ruta absoluta del directorio raíz del proyecto
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(PROJECT_ROOT)

from Admin_Dashboard.services.Recipe_creator_service import RecipeCreatorService

class RecipeCreatorController:
    def __init__(self):
        self.ClassifyProductService = RecipeCreatorService()

    def get_products(self):
        return self.ClassifyProductService.get_products()
    
    def create_recipe(self, selected_products: list, codigo_producto: str,nombre:str, precio: float):
        return self.ClassifyProductService.create_recipe(selected_products, codigo_producto, nombre, precio)
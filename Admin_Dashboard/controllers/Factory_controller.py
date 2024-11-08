from Admin_Dashboard.utils.file_handler import FileHandler
from Admin_Dashboard.services.Factory_service import FactoryService

class FactoryController:
    def __init__(self):
        self.file_handler = FileHandler('Product_Templates')
        self.FactoryService = FactoryService()

    def get_available_recipes(self):
        return self.FactoryService.get_available_recipes()
    
    def get_recipe_by_name(self, nombre: str):
        return self.FactoryService.get_recipe_by_name(nombre)

    def get_material_quantities(self, recipe_name: str):
        return self.FactoryService.get_material_quantities(recipe_name)

    def get_product_by_code(self, codigo: str):
        return self.FactoryService.get_product_by_code(codigo)
    
    def craft_product(self, nombre: str, cantidad: float):
        return self.FactoryService.craft_product(nombre, cantidad)
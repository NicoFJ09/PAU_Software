from Admin_Dashboard.utils.file_handler import FileHandler

class RecipeCreatorService:
    
    def __init__(self):
        """Inicializa el servicio con manejador de archivos"""
        self.product_templates_handler = FileHandler("Product_Templates.json")
        self.produce_templates_handler = FileHandler("Produce_Templates.json")
        self.recipes_handler = FileHandler("recipes.json")
    
    def get_products(self) -> list:
        """Obtiene todos los productos de ambos templates excepto los que tienen CodigoProducto igual a PAP o TOM"""
        product_templates = self.product_templates_handler.read_file()
        produce_templates = self.produce_templates_handler.read_file()
        
        combined_products = product_templates + produce_templates
        return [p for p in combined_products if p["codigoProducto"] not in ["PAP", "TOM", "PAP_DA", "TOM_DA"]]
    
    def create_recipe(self, selected_products: list, codigo_producto: str, nombre: float, precio: float):
        """Crea una nueva receta a partir de los productos seleccionados y sus cantidades, y la añade al archivo Recipes.json"""
        new_recipe = {
            "codigoProducto": codigo_producto,
            "Nombre": nombre,
            "Precio": precio,
            "materiales": [
                {
                    "codigoProducto": p["codigoProducto"],
                    "Nombre": p["Nombre"],
                    "cantidad": p["cantidad"],
                    "unidadMedida": p["unidadMedida"]
                } for p in selected_products
            ]
        }
        
        recipes = self.recipes_handler.read_file()
        recipes.append(new_recipe)
        self.recipes_handler.write_file(recipes)
        print("Receta creada y guardada exitosamente.")
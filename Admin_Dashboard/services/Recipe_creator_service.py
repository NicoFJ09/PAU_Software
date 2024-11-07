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
    
    def create_recipe(self, selected_products: list, codigo_producto: str, nombre: str, precio: float):
        """Crea una nueva receta a partir de los productos seleccionados y sus cantidades, y la añade al archivo Recipes.json"""
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
    service = RecipeCreatorService()
    
    # Obtener productos disponibles
    available_products = service.get_available_products()
    print("Productos disponibles para la receta:")
    for product in available_products:
        print(f"{product['codigoProducto']}: {product['Nombre']}")
    
    # Ejemplo de productos seleccionados y sus cantidades
    selected_products = [
        {"codigoProducto": "PAP-001", "Nombre": "Papa fresca", "cantidad": 1.2, "unidadMedida": "Kilogramos"},
        {"codigoProducto": "SAL-003", "Nombre": "Sal", "cantidad": 10, "unidadMedida": "Gramos"}
    ]
    
    # Parámetros del nuevo producto
    codigo_producto = "CHP"
    nombre = "Chips de papa (Paquete de 500g)"
    precio = 2500
    
    # Crear receta
    new_recipe = service.create_recipe(selected_products, codigo_producto, nombre, precio)
    
    # Añadir receta al archivo
    service.add_recipe_to_file(new_recipe)

if __name__ == "__main__":
    main()
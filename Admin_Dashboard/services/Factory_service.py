
from datetime import datetime
from Admin_Dashboard.utils.file_handler import FileHandler

class FactoryService:
    
    def __init__(self):
        """Inicializa el servicio con manejadores de archivos"""
        self.product_handler = FileHandler("products.json")
        self.recipe_handler = FileHandler("recipes.json")
    
    def _generate_id(self, products: list, new_product: dict) -> int:
        """Genera ID único basado en fecha y código de producto"""
        matching_products = [
            p for p in products 
            if p["codigoProducto"] == new_product["codigoProducto"] 
            and p["Date"] == new_product["Date"]
        ]
        return 1 if not matching_products else max(p["Id"] for p in matching_products) + 1

    def get_available_recipes(self) -> list:
        """Obtiene lista de recetas disponibles"""
        recipes = self.recipe_handler.read_file()
        if not recipes:
            raise ValueError("No hay recetas disponibles")
        return recipes
    
    def get_recipe_by_name(self, nombre: str) -> dict:
        """Obtiene receta por nombre de producto"""
        recipes = self.recipe_handler.read_file()
        recipe = next((r for r in recipes if r["Nombre"].lower() == nombre.lower()), None)
        if not recipe:
            raise ValueError(f"No existe receta con nombre {nombre}")
        return recipe

    def get_material_quantities(self, recipe_name: str) -> dict:
        """
        Obtiene las cantidades disponibles de los materiales requeridos para una receta
        :param recipe_name: Nombre de la receta
        :return: Diccionario con cantidades disponibles por material
        """
        recipe = self.get_recipe_by_name(recipe_name)
        material_quantities = {}
        
        for material in recipe["materiales"]:
            available_products = self.get_product_by_code(material["codigoProducto"])
            total_quantity = sum(p["cantidad"] for p in available_products)
            material_quantities[material["codigoProducto"]] = {
                "nombre": material["Nombre"],
                "disponible": total_quantity,
                "requerido": material["cantidad"],
                "unidadMedida": material["unidadMedida"]
            }
        
        return material_quantities

    def get_product_by_code(self, codigo: str) -> list:
        """Busca todos los productos específicos por código"""
        products = self.product_handler.read_file()
        return [p for p in products if p["codigoProducto"] == codigo]

    def craft_product(self, nombre: str, cantidad: float) -> dict:
        """
        Crea un nuevo producto a partir de una receta y materiales disponibles
        :param nombre: Nombre del producto a crear
        :param cantidad: Cantidad del producto a crear
        :return: Producto creado
        """
        fecha = datetime.now().strftime("%Y-%m-%d")
        recipe = self.get_recipe_by_name(nombre)
        all_products = self.product_handler.read_file()
        
        # Verificar materiales disponibles
        for material in recipe["materiales"]:
            required_quantity = material["cantidad"] * cantidad
            available_products = [p for p in all_products if p["codigoProducto"] == material["codigoProducto"]]
            total_available = sum(p["cantidad"] for p in available_products)
            if total_available < required_quantity:
                raise ValueError(f"Material insuficiente: {material['Nombre']}. Disponible: {total_available}, Requerido: {required_quantity}")

        # Reducir materiales
        for material in recipe["materiales"]:
            required_quantity = material["cantidad"] * cantidad
            available_products = sorted(
                [p for p in all_products if p["codigoProducto"] == material["codigoProducto"]], 
                key=lambda x: x["cantidad"]
            )
            
            for product in available_products:
                if required_quantity <= 0:
                    break
                
                product_to_modify = next(
                    (p for p in all_products 
                     if p["Id"] == product["Id"] 
                     and p["codigoProducto"] == product["codigoProducto"]),
                    None
                )
                
                if product_to_modify:
                    if product_to_modify["cantidad"] <= required_quantity:
                        required_quantity -= product_to_modify["cantidad"]
                        product_to_modify["cantidad"] = 0
                    else:
                        product_to_modify["cantidad"] -= required_quantity
                        required_quantity = 0

        # Limpiar productos con cantidad 0
        all_products = [p for p in all_products if p["cantidad"] > 0]
        
        # Crear nuevo producto
        new_product = {
            "codigoProducto": recipe["codigoProducto"],
            "Nombre": recipe["Nombre"],
            "Precio": recipe["Precio"],
            "Date": fecha,
            "cantidad": cantidad,
            "Id": self._generate_id(all_products, {"codigoProducto": recipe["codigoProducto"], "Date": fecha})
        }
        
        all_products.append(new_product)
        self.product_handler.write_file(all_products)
        
        return new_product
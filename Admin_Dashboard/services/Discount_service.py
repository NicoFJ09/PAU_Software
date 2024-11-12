from Admin_Dashboard.utils.file_handler import FileHandler

class DiscountService:
    
    def __init__(self):
        """Initialize the service with file handlers"""
        self.recipe_handler = FileHandler("recipes.json")
        self.discount_handler = FileHandler("discountProducts.json")
        self.initialize_discount_file()

    def initialize_discount_file(self):
        """Initialize the discount file with products from recipes if not already present"""
        recipes = self.recipe_handler.read_file()
        discounts = self.discount_handler.read_file() or []

        discount_codes = {d["codigoProducto"] for d in discounts}
        new_discounts = [
            {
                "codigoProducto": r["codigoProducto"],
                "Nombre": r["Nombre"],
                "Precio": r["Precio"],
                "Descuento": 0
            }
            for r in recipes if r["codigoProducto"] not in discount_codes
        ]

        if new_discounts:
            discounts.extend(new_discounts)
            self.discount_handler.write_file(discounts)

    def get_discounts(self) -> list:
        """Get the list of discounts"""
        return self.discount_handler.read_file()

    def set_discount(self, codigo_producto: str, discount_value: float):
        """Set a discount value for a specific product"""
        discounts = self.discount_handler.read_file()
        for discount in discounts:
            if discount["codigoProducto"] == codigo_producto:
                discount["Descuento"] = discount_value
                self.discount_handler.write_file(discounts)
                return
        raise ValueError(f"No product found with codigoProducto {codigo_producto}")

    def get_products(self) -> list:
        """Get the list of products from recipes"""
        return self.recipe_handler.read_file()
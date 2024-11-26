from E_Commerce.utils.file_handler import FileHandler

class SaleProductsService:
    
    def __init__(self):
        self.sale_handler = FileHandler("saleproducts.json")
        self.discount_handler = FileHandler("discountproducts.json")
        self.added_products = self.add_products()
    
    def add_products(self):
        sale_products = self.sale_handler.read_file() or []
        discount_products = self.discount_handler.read_file() or []
        
        # Crear un diccionario de descuentos basado en codigoProducto
        discount_dict = {product["codigoProducto"]: product["Descuento"] for product in discount_products}
        
        added_products_dict = {}
        
        for product in sale_products:
            codigo_producto = product["codigoProducto"]
            if codigo_producto not in added_products_dict:
                added_products_dict[codigo_producto] = {
                    "CodigoProducto": codigo_producto,
                    "Nombre": product["Nombre"],
                    "unidadMedida": product["unidadMedida"],
                    "Precio": product["Precio"],
                    "cantidad": 0,
                    "Descuento": discount_dict.get(codigo_producto, 0.0)  # Añadir descuento si existe, sino 0.0
                }
            added_products_dict[codigo_producto]["cantidad"] += product["cantidad"]
        
        # Convertir el diccionario en una lista de productos
        added_products = list(added_products_dict.values())
        
        return added_products

    def sell_products(self, codigo_producto, cantidad):
        sale_products = self.sale_handler.read_file() or []
        
        # Filtrar los productos por codigoProducto
        filtered_products = [p for p in sale_products if p["codigoProducto"] == codigo_producto]
        
        # Ordenar los productos por fecha y luego por ID
        filtered_products.sort(key=lambda x: (x["Date"], x["Id"]))
        
        total_available = sum(p["cantidad"] for p in self.added_products if p["CodigoProducto"] == codigo_producto)
        
        if cantidad > total_available:
            return "insumos insuficientes"
        
        remaining_quantity = cantidad
        
        for product in filtered_products:
            if remaining_quantity <= 0:
                break
            
            if product["cantidad"] <= remaining_quantity:
                remaining_quantity -= product["cantidad"]
                product["cantidad"] = 0
            else:
                product["cantidad"] -= remaining_quantity
                remaining_quantity = 0
        
        # Guardar los cambios en el archivo
        self.sale_handler.write_file(sale_products)
        
        # Actualizar la cantidad en added_products
        for p in self.added_products:
            if p["CodigoProducto"] == codigo_producto:
                if remaining_quantity > 0:
                    if p["cantidad"] <= remaining_quantity:
                        remaining_quantity -= p["cantidad"]
                        p["cantidad"] = 0
                    else:
                        p["cantidad"] -= remaining_quantity
                        remaining_quantity = 0
        
        return "venta realizada con éxito"

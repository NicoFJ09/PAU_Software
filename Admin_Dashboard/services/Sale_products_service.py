from Admin_Dashboard.utils.file_handler import FileHandler

class SaleProductsService:
    
    def __init__(self):
        self.presale_handler = FileHandler("presaleproducts.json")
        self.sale_handler = FileHandler("saleproducts.json")
    
    def move_product_to_sale(self, codigo_producto: str, fecha: str, product_id: int, cantidad: int):
        presale_products = self.presale_handler.read_file()
        sale_products = self.sale_handler.read_file() or []
        
        # Filtrar productos por codigoProducto, fecha y ID
        matching_products = [
            p for p in presale_products 
            if p["codigoProducto"] == codigo_producto and p["Date"] == fecha and p["Id"] == product_id
        ]
        
        if not matching_products:
            raise ValueError(f"No se encontraron productos con el código {codigo_producto}, fecha {fecha} e ID {product_id}")
        
        for product in matching_products:
            if cantidad <= 0:
                break
            
            if product["cantidad"] <= cantidad:
                cantidad -= product["cantidad"]
                product_to_move = product.copy()
                presale_products.remove(product)
            else:
                product["cantidad"] -= cantidad
                product_to_move = product.copy()
                product_to_move["cantidad"] = cantidad
                cantidad = 0
            
            product_to_move["discount"] = False
            
            # Verificar si el producto ya existe en sale_products
            existing_product = next(
                (p for p in sale_products 
                 if p["codigoProducto"] == codigo_producto and p["Date"] == fecha and p["Id"] == product_id),
                None
            )
            
            if existing_product:
                existing_product["cantidad"] += product_to_move["cantidad"]
            else:
                sale_products.append(product_to_move)
        
        self.presale_handler.write_file(presale_products)
        self.sale_handler.write_file(sale_products)
        print("Productos movidos exitosamente.")
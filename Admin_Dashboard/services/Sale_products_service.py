from Admin_Dashboard.utils.file_handler import FileHandler

class SaleProductsService:
    
    def __init__(self):
        self.presale_handler = FileHandler("presaleproducts.json")
        self.sale_handler = FileHandler("saleproducts.json")
    
    def move_product_to_sale(self, codigo_producto: str, fecha: str, product_id: int, cantidad: int):
        presale_products = self.presale_handler.read_file()
        sale_products = self.sale_handler.read_file() or []
        
        # Imprimir valores de entrada
        print(f"Entradas: codigo_producto={codigo_producto}, fecha={fecha}, product_id={product_id}, cantidad={cantidad}")
        
        # Filtrar productos por codigoProducto, fecha y ID en presale
        matching_products = [
            p for p in presale_products 
            if p["codigoProducto"] == codigo_producto and p["Date"] == fecha and p["Id"] == product_id
        ]
        
        # Imprimir productos coincidentes
        print(f"Productos coincidentes en presale: {matching_products}")
        
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
            
            # Verificar si el producto ya existe en sale_products
            existing_product = next(
                (p for p in sale_products 
                 if p["codigoProducto"] == codigo_producto and p["Date"] == fecha and p["Id"] == product_id),
                None
            )
            
            # Imprimir producto existente en sale_products
            print(f"Producto existente en sale_products: {existing_product}")
            
            if existing_product:
                existing_product["cantidad"] += product_to_move["cantidad"]
            else:
                sale_products.append(product_to_move)
        
        # Limpiar productos con cantidad 0 en presale
        presale_products = [p for p in presale_products if p["cantidad"] > 0]
        
        self.presale_handler.write_file(presale_products)
        self.sale_handler.write_file(sale_products)
        print("Productos movidos exitosamente.")
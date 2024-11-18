import os
import sys
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
        
        added_products = {}
        
        for product in sale_products:
            codigo_producto = product["codigoProducto"]
            if codigo_producto not in added_products:
                added_products[codigo_producto] = {
                    "Nombre": product["Nombre"],
                    "unidadMedida": product["unidadMedida"],
                    "Precio": product["Precio"],
                    "cantidad": 0,
                    "Descuento": discount_dict.get(codigo_producto, 0.0)  # Añadir descuento si existe, sino 0.0
                }
            added_products[codigo_producto]["cantidad"] += product["cantidad"]
        
        # Imprimir la estructura resultante
        for codigo, data in added_products.items():
            print(f"CodigoProducto: {codigo}, Datos: {data}")
        
        return added_products

    def sell_product(self, codigo_producto, cantidad):
        sale_products = self.sale_handler.read_file() or []
        
        # Filtrar los productos por codigoProducto
        filtered_products = [p for p in sale_products if p["codigoProducto"] == codigo_producto]
        
        # Ordenar los productos por fecha y luego por ID
        filtered_products.sort(key=lambda x: (x["Date"], x["Id"]))
        
        total_available = self.added_products.get(codigo_producto, {}).get("cantidad", 0)
        
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
        self.added_products[codigo_producto]["cantidad"] -= cantidad
        
        return "venta realizada con éxito"

from Admin_Dashboard.utils.file_handler import FileHandler
from Admin_Dashboard.services.Sale_products_service import SaleProductsService

class SaleController:
    def __init__(self):
        self.file_handler = FileHandler('presaleproducts.json')
        self.SaleProductsService = SaleProductsService()

    def get_products(self):
        """Obtener productos del archivo JSON"""
        return self.file_handler.read_file()

    def move_product_to_sale(self, codigo_producto: str, fecha: str, product_id: int, cantidad: int):
        return self.SaleProductsService.move_product_to_sale(codigo_producto, fecha, product_id, cantidad)
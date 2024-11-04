from Admin_Dashboard.utils.file_handler import FileHandler
from Admin_Dashboard.services.Product_service import ProductService

class PreClassificationController:
    def __init__(self):
        self.file_handler = FileHandler('Product_Templates')
        self.ProductService = ProductService()
    
    def get_products(self):
        """Obtener productos del archivo JSON"""
        return self.file_handler.read_file()
    
    def create_product(self, codigo, cantidad):
        return self.ProductService.create_product(codigo, cantidad)

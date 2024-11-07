from Admin_Dashboard.utils.file_handler import FileHandler
from Admin_Dashboard.services.Product_service import ProductService
from Admin_Dashboard.services.Product_template_service import ProductTemplateService
class PreClassificationController:
    def __init__(self):
        self.file_handler = FileHandler('Product_Templates')
        self.ProductService = ProductService()
        self.ProductTemplateService = ProductTemplateService()
    
    def get_products(self):
        """Obtener productos del archivo JSON"""
        return self.file_handler.read_file()
    
    def order_product(self, codigo: str, cantidad: int):
        return self.ProductService.order_product(codigo, cantidad)
    
    def create_template(self, codigo: str, nombre: str, unidad: str):
        return self.ProductTemplateService.create_template(codigo, nombre, unidad)

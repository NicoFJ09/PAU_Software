from Admin_Dashboard.utils.file_handler import FileHandler
from Admin_Dashboard.services.Classify_product_service import ClassifyProductService
class ClassificationController:
    def __init__(self):
        self.file_handler = FileHandler('Product_Templates')
        self.ClassifyProductService = ClassifyProductService()

    def get_products(self):
        """Obtener Tomates y Papas del archivo JSON"""
        return self.ClassifyProductService.get_products()
    
    def classify_product(self, product_id: int, cantidad: float, nombre: str,unidadMedida:str, date: str):
        return self.ClassifyProductService.classify_product(product_id, cantidad, nombre, unidadMedida, date)
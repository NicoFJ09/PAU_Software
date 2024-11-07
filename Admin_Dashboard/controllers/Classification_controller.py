from Admin_Dashboard.utils.file_handler import FileHandler
from Admin_Dashboard.services.Classified_product_service import ClassifiedProductService
class ClassificationController:
    def __init__(self):
        self.file_handler = FileHandler('Product_Templates')
        self.ClassifiedProductService = ClassifiedProductService()

    def get_products(self):
        """Obtener Tomates y Papas del archivo JSON"""
        return self.ClassifiedProductService.get_products()
    
    def classify_product(self, product_id: int, cantidad: float, nombre: str,unidadMedida:str, date: str):
        return self.ClassifiedProductService.classify_product(product_id, cantidad, nombre, unidadMedida, date)

from utils.file_handler import FileHandler

class PreClassificationController:
    def __init__(self):
        self.file_handler = FileHandler('Product_Templates')
    
    def get_products(self):
        """Obtener productos del archivo JSON"""
        return self.file_handler.read_file()
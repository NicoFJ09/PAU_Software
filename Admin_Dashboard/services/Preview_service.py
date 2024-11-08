from Admin_Dashboard.utils.file_handler import FileHandler

class PreviewService:
    
    def __init__(self):
        """Inicializa el servicio con manejadores de archivos"""
        self.products_handler = FileHandler("products.json")
        self.presale_handler = FileHandler("presaleproducts.json")
    
    def get_products(self) -> list:
        """Obtiene todos los productos del archivo products.json"""
        return self.products_handler.read_file() or []
    
    def get_presale_products(self) -> list:
        """Obtiene todos los productos del archivo presaleproducts.json"""
        return self.presale_handler.read_file() or []
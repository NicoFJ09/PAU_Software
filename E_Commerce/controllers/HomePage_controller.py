from E_Commerce.services.Sale_products_service import SaleProductsService
class HomePageController:
    def __init__(self):
        self.SaleProductsService = SaleProductsService()

    def get_products(self):
        """Obtener productos web"""
        return self.SaleProductsService.add_products()
    
from E_Commerce.services.Sale_products_service import SaleProductsService
class PaymentController:
    def __init__(self):
        self.SaleProductsService = SaleProductsService()

    def sell_products(self, codigo_producto: str, cantidad: int):
        """Obtener productos web"""
        return self.SaleProductsService.sell_products(codigo_producto,cantidad)
    
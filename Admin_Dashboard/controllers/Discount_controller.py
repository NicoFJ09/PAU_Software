from Admin_Dashboard.utils.file_handler import FileHandler
from Admin_Dashboard.services.Discount_service import DiscountService

class DiscountController:
    def __init__(self):
        self.file_handler = FileHandler('discountProducts')
        self.DiscountService = DiscountService()

    def get_discounts(self):
        return self.file_handler.read_file()

    def initialize_discount_file(self):
        return self.DiscountService.initialize_discount_file()
    
    def set_discount(self, codigo_producto: str, discount_value: int):
        return self.DiscountService.set_discount(codigo_producto, discount_value)
    

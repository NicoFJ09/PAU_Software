from Admin_Dashboard.services.Preview_service import PreviewService

class PreviewController:
    def __init__(self):
        self.PreviewService = PreviewService()

    def get_products(self):
        return self.PreviewService.get_products()
    
    def get_presale_products(self):
        return self.PreviewService.get_presale_products()
from Admin_Dashboard.utils.file_handler import FileHandler
from Admin_Dashboard.models.Product import REQUIRED_TEMPLATE_FIELDS

class ProductTemplateService:
    
    # ------------------------
    # Constructor de servicio
    # ------------------------
    def __init__(self):
        """Inicializa el servicio con manejador de archivos"""
        self.file_handler = FileHandler("product_templates")
    
    # ------------------------
    # Operaciones de búsqueda
    # ------------------------
    def get_all_templates(self) -> list:
        """Obtiene todas las plantillas disponibles"""
        return self.file_handler.read_file()

    def get_template_by_code(self, code: str) -> dict:
        """Busca plantilla por código de producto"""
        templates = self.file_handler.read_file()
        return next((t for t in templates if t["codigoProducto"] == code.upper()), None)
    
    # ------------------------
    # Validaciones
    # ------------------------
    def validate_template_data(self, codigo: str, nombre: str, unidad: str) -> bool:
        """
        Valida los datos de la plantilla
        :param codigo: Código del producto
        :param nombre: Nombre del producto
        :param unidad: Unidad de medida
        :return: True si los datos son válidos
        """
        if not codigo:
            raise ValueError("El código no puede estar vacío")
        
        if self.get_template_by_code(codigo):
            raise ValueError(f"Ya existe un producto con el código {codigo}")
            
        if not nombre:
            raise ValueError("El nombre no puede estar vacío")
            
        if not unidad:
            raise ValueError("La unidad de medida no puede estar vacía")
            
        return True
    
    # ------------------------
    # Operaciones de plantillas
    # ------------------------
    def create_template(self, codigo: str, nombre: str, unidad: str) -> dict:
        """
        Crea una nueva plantilla de producto
        :param codigo: Código del producto
        :param nombre: Nombre del producto
        :param unidad: Unidad de medida
        :return: Plantilla creada
        """
        self.validate_template_data(codigo, nombre, unidad)
        
        template_data = {
            "codigoProducto": codigo.upper(),
            "Nombre": nombre.strip(),
            "unidadMedida": unidad.strip().lower()
        }
        
        return self.add_template(template_data)

    def add_template(self, template_data: dict) -> dict:
        """
        Agrega nueva plantilla de producto
        :param template_data: Diccionario con datos de la plantilla
        :return: Plantilla agregada
        """
        templates = self.file_handler.read_file()
        
        if not all(field in template_data for field in REQUIRED_TEMPLATE_FIELDS):
            raise ValueError(f"Faltan campos requeridos: {', '.join(REQUIRED_TEMPLATE_FIELDS)}")
        
        templates.append(template_data)
        self.file_handler.write_file(templates)
        
        return template_data
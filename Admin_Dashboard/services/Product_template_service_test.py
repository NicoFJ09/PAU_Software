import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.file_handler import FileHandler
from models.Product import REQUIRED_TEMPLATE_FIELDS

class ProductTemplateService:
    """Servicio para manejar plantillas de productos"""
    
    def __init__(self):
        self.file_handler = FileHandler("product_templates")
    
    def get_all_templates(self) -> list:
        """Obtiene todas las plantillas de productos"""
        return self.file_handler.read_file()
    
    def get_template_by_code(self, code: str) -> dict:
        """Busca plantilla por código de producto"""
        templates = self.file_handler.read_file()
        return next((t for t in templates if t["codigoProducto"] == code), None)
    
    def add_template_interactive(self):
        """Solicita datos del template por consola"""
        try:
            print("\n=== Agregar Nueva Plantilla de Producto ===")
            
            # Solicitar datos
            codigo = input("Código de ítem: ").strip().upper()
            if not codigo:
                raise ValueError("El código no puede estar vacío")
                
            # Verificar si ya existe
            if self.get_template_by_code(codigo):
                raise ValueError(f"Ya existe un producto con el código {codigo}")
            
            nombre = input("Nombre de producto: ").strip()
            if not nombre:
                raise ValueError("El nombre no puede estar vacío")
            
            unidad = input("Unidad de medida: ").strip().lower()
            if not unidad:
                raise ValueError("La unidad de medida no puede estar vacía")
            
            # Crear template
            template = {
                "codigoProducto": codigo,
                "nombre": nombre,
                "unidadMedida": unidad
            }
            
            # Guardar template
            self.add_template(template)
            print(f"\nPlantilla agregada exitosamente: {codigo} - {nombre}")
            
        except ValueError as e:
            print(f"\nError: {str(e)}")
        except Exception as e:
            print(f"\nError inesperado: {str(e)}")

    def add_template(self, template_data: dict) -> dict:
        """Agrega nueva plantilla de producto"""
        templates = self.file_handler.read_file()
        
        if not all(field in template_data for field in REQUIRED_TEMPLATE_FIELDS):
            raise ValueError(f"Faltan campos requeridos: {', '.join(REQUIRED_TEMPLATE_FIELDS)}")
        
        templates.append(template_data)
        self.file_handler.write_file(templates)
        return template_data

# Ejemplo de uso
if __name__ == "__main__":
    service = ProductTemplateService()
    while True:
        service.add_template_interactive()
        
        continuar = input("\n¿Desea agregar otro producto? (s/n): ").lower()
        if continuar != 's':
            break
    
    print("\nTemplates guardados. ¡Hasta luego!")
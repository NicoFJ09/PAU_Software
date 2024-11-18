import os
import json
from typing import Any, List

class FileHandler:
    """Manejador genérico de archivos JSON"""
    
    def __init__(self, file_name: str):
        """
        Constructor del manejador de archivos
        :param file_name: Nombre del archivo JSON
        """
        if not file_name.endswith('.json'):
            file_name = f"{file_name}.json"
            
        # Obtener ruta al directorio data
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        main_dir = os.path.dirname(current_dir)
        
        data_dir = os.path.join(main_dir, 'data')
        self.file_path = os.path.join(data_dir, file_name)
        
        self._verify_file_exists()
    
    def _verify_file_exists(self) -> None:
        """Verifica existencia del archivo JSON"""
        data_dir = os.path.dirname(self.file_path)
        
        if not os.path.exists(data_dir):
            raise FileNotFoundError(f"El directorio 'data' no existe en: {data_dir}")
        
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump([], file, indent=2, ensure_ascii=False)
            print(f"Se ha creado el archivo: {self.file_path}")

    def read_file(self) -> List[Any]:
        """Lee el contenido del archivo JSON"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                return json.loads(content) if content else []
        except json.JSONDecodeError as e:
            print(f"Error decodificando JSON: {e}")
            return []
        except Exception as e:
            print(f"Error leyendo archivo: {e}")
            raise

    def write_file(self, data: List[Any]) -> None:
        """Escribe datos en el archivo JSON"""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error escribiendo archivo: {e}")
            raise
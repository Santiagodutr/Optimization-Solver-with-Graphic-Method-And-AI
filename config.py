import os
import json
from typing import Optional
from dotenv import load_dotenv

class Config:
    def __init__(self):
        """Inicializar configuración"""
        # Cargar variables de entorno desde .env
        load_dotenv()
        
        self.config_dir = os.path.expanduser("~")
        self.config_file = os.path.join(self.config_dir, ".linear_programming_solver_config.json")
        self.config_data = self._load_config()
    
    def _load_config(self) -> dict:
        """
        Cargar configuración desde archivo
        
        Returns:
            dict: Datos de configuración
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {}
        except Exception:
            # Si hay error al cargar, crear configuración nueva
            return {}
    
    def _save_config(self) -> None:
        """Guardar configuración en archivo"""
        try:
            # Crear directorio si no existe
            os.makedirs(self.config_dir, exist_ok=True)
            
            # Guardar configuración
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise Exception(f"Error al guardar configuración: {str(e)}")
    
    def get_api_key(self) -> Optional[str]:
        """
        Obtener API key de Gemini
        
        Returns:
            Optional[str]: API key si existe, None si no
        """
        # Primero intentar cargar desde .env
        env_api_key = os.getenv('GEMINI_API_KEY')
        if env_api_key:
            return env_api_key
        
        # Si no está en .env, buscar en configuración guardada
        return self.config_data.get('gemini_api_key')
    
    def set_api_key(self, api_key: str) -> None:
        """
        Configurar API key de Gemini
        
        Args:
            api_key (str): Clave de API de Gemini
        """
        if not api_key or not api_key.strip():
            raise ValueError("API key no puede estar vacía")
        
        self.config_data['gemini_api_key'] = api_key.strip()
        self._save_config()
    
    def get_last_image_directory(self) -> Optional[str]:
        """
        Obtener el último directorio usado para cargar imágenes
        
        Returns:
            Optional[str]: Ruta del directorio o None
        """
        return self.config_data.get('last_image_directory')
    
    def set_last_image_directory(self, directory: str) -> None:
        """
        Guardar el último directorio usado para cargar imágenes
        
        Args:
            directory (str): Ruta del directorio
        """
        if directory and os.path.isdir(directory):
            self.config_data['last_image_directory'] = directory
            self._save_config()
    
    def get_window_geometry(self) -> Optional[str]:
        """
        Obtener geometría de ventana guardada
        
        Returns:
            Optional[str]: Geometría de ventana
        """
        return self.config_data.get('window_geometry')
    
    def set_window_geometry(self, geometry: str) -> None:
        """
        Guardar geometría de ventana
        
        Args:
            geometry (str): Geometría de ventana (formato: "widthxheight+x+y")
        """
        if geometry:
            self.config_data['window_geometry'] = geometry
            self._save_config()
    
    def get_language(self) -> str:
        """
        Obtener idioma configurado
        
        Returns:
            str: Código de idioma (por defecto 'es' para español)
        """
        return self.config_data.get('language', 'es')
    
    def set_language(self, language: str) -> None:
        """
        Configurar idioma
        
        Args:
            language (str): Código de idioma
        """
        valid_languages = ['es', 'en']
        if language in valid_languages:
            self.config_data['language'] = language
            self._save_config()
    
    def get_theme(self) -> str:
        """
        Obtener tema configurado
        
        Returns:
            str: Nombre del tema (por defecto 'default')
        """
        return self.config_data.get('theme', 'default')
    
    def set_theme(self, theme: str) -> None:
        """
        Configurar tema
        
        Args:
            theme (str): Nombre del tema
        """
        valid_themes = ['default', 'dark', 'light']
        if theme in valid_themes:
            self.config_data['theme'] = theme
            self._save_config()
    
    def get_max_image_size(self) -> int:
        """
        Obtener tamaño máximo de imagen en MB
        
        Returns:
            int: Tamaño máximo en MB
        """
        return self.config_data.get('max_image_size_mb', 5)
    
    def set_max_image_size(self, size_mb: int) -> None:
        """
        Configurar tamaño máximo de imagen
        
        Args:
            size_mb (int): Tamaño máximo en MB
        """
        if size_mb > 0 and size_mb <= 20:  # Máximo 20MB
            self.config_data['max_image_size_mb'] = size_mb
            self._save_config()
    
    def reset_config(self) -> None:
        """Resetear configuración a valores por defecto"""
        self.config_data = {}
        self._save_config()
    
    def export_config(self, file_path: str) -> None:
        """
        Exportar configuración a archivo
        
        Args:
            file_path (str): Ruta donde guardar la configuración
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise Exception(f"Error al exportar configuración: {str(e)}")
    
    def import_config(self, file_path: str) -> None:
        """
        Importar configuración desde archivo
        
        Args:
            file_path (str): Ruta del archivo de configuración
        """
        try:
            if not os.path.exists(file_path):
                raise Exception("El archivo de configuración no existe")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
            
            # Validar configuración importada
            if isinstance(imported_config, dict):
                self.config_data = imported_config
                self._save_config()
            else:
                raise Exception("Formato de configuración inválido")
                
        except json.JSONDecodeError:
            raise Exception("Error al leer el archivo de configuración")
        except Exception as e:
            raise Exception(f"Error al importar configuración: {str(e)}")
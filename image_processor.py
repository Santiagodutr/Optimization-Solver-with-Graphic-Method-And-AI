import base64
import os
from PIL import Image
from typing import Dict, Any

class ImageProcessor:
    def __init__(self):
        """Inicializar el procesador de imágenes"""
        self.supported_formats = {
            'PNG': 'image/png',
            'JPEG': 'image/jpeg', 
            'JPG': 'image/jpeg',
            'GIF': 'image/gif',
            'BMP': 'image/bmp',
            'WEBP': 'image/webp'
        }
        
        # Tamaño máximo en bytes (5MB)
        self.max_file_size = 5 * 1024 * 1024
    
    def validate_image(self, file_path: str) -> None:
        """
        Validar que el archivo sea una imagen válida
        
        Args:
            file_path (str): Ruta al archivo de imagen
            
        Raises:
            Exception: Si la imagen no es válida
        """
        # Verificar que el archivo existe
        if not os.path.exists(file_path):
            raise Exception("El archivo no existe")
        
        # Verificar el tamaño del archivo
        file_size = os.path.getsize(file_path)
        if file_size > self.max_file_size:
            raise Exception(f"El archivo es demasiado grande. Máximo permitido: {self.max_file_size // (1024*1024)}MB")
        
        if file_size == 0:
            raise Exception("El archivo está vacío")
        
        try:
            # Intentar abrir la imagen con PIL
            with Image.open(file_path) as img:
                # Verificar formato
                if img.format.upper() not in self.supported_formats:
                    supported_list = ', '.join(self.supported_formats.keys())
                    raise Exception(f"Formato no soportado: {img.format}. Formatos soportados: {supported_list}")
                
                # Verificar que la imagen tenga contenido
                if img.size[0] == 0 or img.size[1] == 0:
                    raise Exception("La imagen tiene dimensiones inválidas")
        
        except Exception as e:
            if "cannot identify image file" in str(e):
                raise Exception("El archivo no es una imagen válida")
            elif "Formato no soportado" in str(e) or "dimensiones inválidas" in str(e):
                raise e
            else:
                raise Exception(f"Error al procesar la imagen: {str(e)}")
    
    def get_mime_type(self, file_path: str) -> str:
        """
        Obtener el tipo MIME de una imagen
        
        Args:
            file_path (str): Ruta al archivo de imagen
            
        Returns:
            str: Tipo MIME de la imagen
        """
        try:
            with Image.open(file_path) as img:
                image_format = img.format.upper()
                return self.supported_formats.get(image_format, 'image/jpeg')
        except Exception:
            # Por defecto, asumir JPEG
            return 'image/jpeg'
    
    def optimize_image(self, file_path: str) -> str:
        """
        Optimizar imagen para reducir tamaño si es necesario
        
        Args:
            file_path (str): Ruta al archivo original
            
        Returns:
            str: Ruta al archivo optimizado (puede ser el mismo si no necesita optimización)
        """
        try:
            with Image.open(file_path) as img:
                # Convertir a RGB si es necesario
                if img.mode not in ('RGB', 'L'):
                    img = img.convert('RGB')
                
                # Redimensionar si es muy grande (máximo 1920x1080 para mantener calidad del texto)
                max_width, max_height = 1920, 1080
                if img.size[0] > max_width or img.size[1] > max_height:
                    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                    
                    # Guardar imagen optimizada
                    base_name = os.path.splitext(file_path)[0]
                    optimized_path = f"{base_name}_optimized.jpg"
                    
                    # Guardar con calidad alta para preservar texto
                    img.save(optimized_path, 'JPEG', quality=95, optimize=True)
                    return optimized_path
                
                return file_path
        
        except Exception:
            # Si hay error en optimización, usar archivo original
            return file_path
    
    def convert_to_base64(self, file_path: str) -> str:
        """
        Convertir imagen a base64
        
        Args:
            file_path (str): Ruta al archivo de imagen
            
        Returns:
            str: Imagen codificada en base64
        """
        try:
            with open(file_path, 'rb') as image_file:
                base64_data = base64.b64encode(image_file.read()).decode('utf-8')
                return base64_data
        except Exception as e:
            raise Exception(f"Error al convertir imagen a base64: {str(e)}")
    
    def process_image(self, file_path: str) -> Dict[str, Any]:
        """
        Procesar imagen completa: validar, optimizar y convertir a base64
        
        Args:
            file_path (str): Ruta al archivo de imagen
            
        Returns:
            Dict[str, Any]: Diccionario con datos de la imagen procesada
        """
        # Validar imagen
        self.validate_image(file_path)
        
        # Optimizar si es necesario
        optimized_path = self.optimize_image(file_path)
        
        try:
            # Obtener tipo MIME
            mime_type = self.get_mime_type(optimized_path)
            
            # Convertir a base64
            base64_data = self.convert_to_base64(optimized_path)
            
            # Limpiar archivo optimizado temporal si es diferente al original
            if optimized_path != file_path and os.path.exists(optimized_path):
                try:
                    os.remove(optimized_path)
                except Exception:
                    pass  # No es crítico si no se puede eliminar
            
            return {
                'base64_data': base64_data,
                'mime_type': mime_type,
                'original_path': file_path,
                'file_size': os.path.getsize(file_path)
            }
        
        except Exception as e:
            # Limpiar archivo temporal en caso de error
            if optimized_path != file_path and os.path.exists(optimized_path):
                try:
                    os.remove(optimized_path)
                except Exception:
                    pass
            raise e
    
    def get_image_info(self, file_path: str) -> Dict[str, Any]:
        """
        Obtener información de la imagen sin procesarla
        
        Args:
            file_path (str): Ruta al archivo de imagen
            
        Returns:
            Dict[str, Any]: Información de la imagen
        """
        try:
            with Image.open(file_path) as img:
                return {
                    'format': img.format,
                    'mode': img.mode,
                    'size': img.size,
                    'width': img.size[0],
                    'height': img.size[1],
                    'file_size': os.path.getsize(file_path),
                    'mime_type': self.get_mime_type(file_path)
                }
        except Exception as e:
            raise Exception(f"Error al obtener información de la imagen: {str(e)}")
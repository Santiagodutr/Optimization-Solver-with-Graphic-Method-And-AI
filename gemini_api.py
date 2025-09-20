import requests
import json
import base64
from typing import Dict, Any

class GeminiAPI:
    def __init__(self, api_key: str):
        """
        Inicializar la clase GeminiAPI
        
        Args:
            api_key (str): Clave de API de Google Gemini
        """
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        self.headers = {
            'Content-Type': 'application/json',
            'X-goog-api-key': self.api_key
        }
    
    def analyze_linear_programming_problem(self, image_data: Dict[str, Any]) -> str:
        """
        Analizar un problema de programación lineal desde una imagen
        
        Args:
            image_data (Dict): Diccionario con los datos de la imagen en base64
            
        Returns:
            str: Respuesta de Gemini con el análisis y solución
        """
        
        # Prompt especializado para problemas de programación lineal
        prompt = """
        Analiza la imagen que contiene un problema de programación lineal que debe resolverse usando el método gráfico.

        IMPORTANTE: Al final de tu respuesta, incluye una sección llamada "DATOS PARA GRÁFICA" con el siguiente formato EXACTO:

        === DATOS PARA GRÁFICA ===
        FUNCION_OBJETIVO: [Maximizar o Minimizar] Z = [coeficientes]x1 + [coeficientes]x2
        RESTRICCIONES:
        - [coef]x1 + [coef]x2 <= [valor]
        - [coef]x1 + [coef]x2 <= [valor]
        - [coef]x1 + [coef]x2 >= [valor]
        - x1 >= 0
        - x2 >= 0
        VERTICES:
        - (x1, x2) = (0, 0)
        - (x1, x2) = (valor, valor)
        - (x1, x2) = (valor, valor)
        SOLUCION_OPTIMA: (x1, x2) = (valor, valor)
        VALOR_OPTIMO: Z = valor
        === FIN DATOS ===

        Ejemplo de formato:
        === DATOS PARA GRÁFICA ===
        FUNCION_OBJETIVO: Maximizar Z = 3x1 + 2x2
        RESTRICCIONES:
        - 1x1 + 1x2 <= 6
        - 2x1 + 1x2 <= 8
        - 1x1 <= 4
        - 1x2 <= 5
        - x1 >= 0
        - x2 >= 0
        VERTICES:
        - (x1, x2) = (0, 0)
        - (x1, x2) = (0, 5)
        - (x1, x2) = (2, 4)
        - (x1, x2) = (4, 0)
        SOLUCION_OPTIMA: (x1, x2) = (2, 4)
        VALOR_OPTIMO: Z = 14
        === FIN DATOS ===

        IMPORTANTE: Incluye TODAS las restricciones del problema, incluyendo:
        - Restricciones principales con ambas variables (ax1 + bx2 <= c)
        - Restricciones de límite superior (x1 <= valor, x2 <= valor)
        - Restricciones de no negatividad (x1 >= 0, x2 >= 0)
        - Cualquier restricción de límite inferior (x1 >= valor, x2 >= valor)

        Usa SIEMPRE el formato exacto mostrado arriba para que el programa pueda leerlo correctamente.

        Ahora resuelve el problema paso a paso:
        1. Identifica la función objetivo (maximizar o minimizar)
        2. Lista todas las restricciones del problema
        3. Determina las variables de decisión
        4. Resuelve usando el método gráfico
        5. Encuentra los vértices de la región factible
        6. Evalúa la función objetivo en cada vértice
        7. Determina la solución óptima

        Proporciona el análisis completo Y al final incluye obligatoriamente la sección "DATOS PARA GRÁFICA" con el formato exacto mostrado arriba.
        """
        
        # Preparar el payload para la API
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        },
                        {
                            "inline_data": {
                                "mime_type": image_data["mime_type"],
                                "data": image_data["base64_data"]
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.1,  # Baja temperatura para respuestas más precisas
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 8192
            },
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH", 
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
        }
        
        try:
            # Realizar la petición a la API
            response = requests.post(
                self.base_url,
                headers=self.headers,
                data=json.dumps(payload),
                timeout=60
            )
            
            # Verificar el código de estado
            if response.status_code != 200:
                error_detail = response.text
                raise Exception(f"Error HTTP {response.status_code}: {error_detail}")
            
            # Procesar la respuesta
            response_data = response.json()
            
            if 'candidates' not in response_data or not response_data['candidates']:
                raise Exception("No se recibió respuesta válida de Gemini API")
            
            # Extraer el texto de la respuesta
            candidate = response_data['candidates'][0]
            
            if 'content' not in candidate or 'parts' not in candidate['content']:
                raise Exception("Formato de respuesta inválido")
            
            parts = candidate['content']['parts']
            if not parts or 'text' not in parts[0]:
                raise Exception("No se encontró texto en la respuesta")
            
            return parts[0]['text']
            
        except requests.exceptions.Timeout:
            raise Exception("Timeout al conectar con Gemini API")
        except requests.exceptions.ConnectionError:
            raise Exception("Error de conexión con Gemini API")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error de petición: {str(e)}")
        except json.JSONDecodeError:
            raise Exception("Error al procesar la respuesta JSON")
        except KeyError as e:
            raise Exception(f"Campo faltante en la respuesta: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado: {str(e)}")
    
    def test_connection(self) -> bool:
        """
        Probar la conexión con la API de Gemini
        
        Returns:
            bool: True si la conexión es exitosa, False en caso contrario
        """
        try:
            # Crear un payload simple para probar
            test_payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": "Hello, this is a test."
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                data=json.dumps(test_payload),
                timeout=30
            )
            
            return response.status_code == 200
            
        except Exception:
            return False
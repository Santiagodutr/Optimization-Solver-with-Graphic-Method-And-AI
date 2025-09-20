# Resolvedor de Programación Lineal con IA

Una aplicación con interfaz gráfica que utiliza la API de Google Gemini para resolver problemas de programación lineal mediante el método gráfico a partir de imágenes.

## 📋 Características

- **Análisis de imágenes**: Carga imágenes de problemas de programación lineal
- **IA integrada**: Utiliza Google Gemini 2.0 Flash para análisis automático
- **Método gráfico**: Resuelve problemas paso a paso usando el método gráfico
- **Interfaz amigable**: GUI desarrollada con tkinter
- **Soporte múltiple**: Acepta formatos PNG, JPG, JPEG, GIF, BMP
- **Optimización automática**: Redimensiona imágenes grandes automáticamente

## 🚀 Instalación

### Prerrequisitos

- Python 3.11 o superior
- Una API key de Google Gemini (gratuita en [Google AI Studio](https://makersuite.google.com/app/apikey))

### Pasos de instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd "c:\Users\USUARIO\OneDrive\Documentos\opti\lab IA"
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Obtener API Key de Gemini**
   - Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Crea una cuenta si no la tienes
   - Genera una nueva API key
   - Copia la API key

## 🎯 Uso

### Ejecutar la aplicación

```bash
python main.py
```

### Pasos para usar

1. **Configurar API Key**
   - Al abrir la aplicación, ingresa tu API key de Gemini en el campo correspondiente
   - Haz clic en "Guardar" (la API key se guarda de forma segura)

2. **Cargar imagen**
   - Haz clic en "Cargar Imagen"
   - Selecciona una imagen que contenga un problema de programación lineal
   - La imagen debe mostrar claramente:
     - Función objetivo
     - Variables de decisión
     - Restricciones
     - Condiciones de no negatividad

3. **Analizar problema**
   - Haz clic en "Analizar Problema"
   - Espera mientras la IA procesa la imagen
   - Los resultados aparecerán en el panel derecho

### Ejemplo de imagen válida

La imagen debe contener un problema como:

```
Maximizar: Z = 3x + 2y

Sujeto a:
x + y ≤ 4
2x + y ≤ 6
x ≥ 0, y ≥ 0
```

## 📁 Estructura del proyecto

```
lab IA/
├── main.py              # Interfaz gráfica principal
├── gemini_api.py        # Manejo de la API de Gemini
├── image_processor.py   # Procesamiento de imágenes
├── config.py           # Configuración y almacenamiento de API key
├── requirements.txt    # Dependencias del proyecto
└── README.md          # Este archivo
```

## 🔧 Configuración avanzada

### Formatos de imagen soportados
- PNG (recomendado para texto claro)
- JPEG/JPG
- GIF
- BMP
- WEBP

### Limitaciones técnicas
- Tamaño máximo de imagen: 5MB
- Dimensiones máximas recomendadas: 1920x1080
- La imagen debe tener texto legible

### Personalización

Puedes modificar la configuración editando `config.py`:

- **Tamaño máximo de imagen**: Modifica `max_file_size` en `ImageProcessor`
- **Prompt de IA**: Edita el prompt en `gemini_api.py` para ajustar el análisis
- **Formatos soportados**: Añade más formatos en `supported_formats`

## 🐛 Solución de problemas

### Error: "Import could not be resolved"
```bash
# Asegúrate de que estás en el directorio correcto
cd "c:\Users\USUARIO\OneDrive\Documentos\opti\lab IA"
# Verifica que todas las dependencias estén instaladas
pip install -r requirements.txt
```

### Error: "Error HTTP 403"
- Verifica que tu API key de Gemini sea válida
- Asegúrate de que la API key tenga permisos para usar Gemini 2.0 Flash

### Error: "El archivo es demasiado grande"
- Reduce el tamaño de la imagen
- Usa una herramienta de compresión de imágenes
- Convierte a formato PNG o JPEG

### Error: "No se puede analizar la imagen"
- Verifica que la imagen contenga texto claro y legible
- Asegúrate de que el problema esté completo (función objetivo, restricciones)
- Usa imágenes con buena resolución y contraste

## 📚 Ejemplo completo

### 1. Prepara tu imagen
Crea o toma una foto de un problema como:

```
Problema: Una empresa produce dos tipos de productos A y B.

Maximizar: Utilidad = 5A + 3B

Restricciones:
- Tiempo de máquina: 2A + B ≤ 100
- Materia prima: A + 2B ≤ 80
- Demanda A: A ≤ 40
- No negatividad: A ≥ 0, B ≥ 0

Resolver usando método gráfico.
```

### 2. Resultado esperado
La IA debería proporcionar:
- Identificación de variables (A, B)
- Función objetivo: Max Z = 5A + 3B
- Lista de restricciones
- Procedimiento del método gráfico paso a paso
- Vértices de la región factible
- Evaluación de la función objetivo en cada vértice
- Solución óptima con interpretación

## 🤝 Contribuir

Si encuentras errores o quieres mejorar la aplicación:

1. Reporta issues describiendo el problema
2. Propón mejoras en la funcionalidad
3. Comparte ejemplos de problemas que no se resuelven correctamente

## 📄 Licencia

Este proyecto es de uso educativo y personal. La API de Gemini tiene sus propios términos de uso.

## ⚡ Comandos rápidos

```bash
# Instalar y ejecutar
pip install -r requirements.txt
python main.py

# Verificar instalación
python -c "import requests, PIL; print('Dependencias OK')"

# Limpiar archivos temporales (opcional)
python -c "import os, glob; [os.remove(f) for f in glob.glob('*_optimized.jpg')]"
```

---

**Nota**: Asegúrate de tener una conexión a internet estable para usar la API de Gemini. La primera ejecución puede tomar más tiempo mientras se cargan las librerías.
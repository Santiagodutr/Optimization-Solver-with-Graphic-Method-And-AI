# 🎯 Resolvedor de Programación Lineal con IA y Método Simplex

Sistema completo para resolver problemas de programación lineal utilizando:
- 🤖 **Inteligencia Artificial (Gemini)** para extraer problemas de imágenes
- 📊 **Método Gráfico** para visualización en 2D
- 🔢 **Método Simplex** para resolución algorítmica paso a paso ⭐ **NUEVO**

## 🎯 Características Principales

### 1. Análisis con IA
- Carga imágenes con problemas de programación lineal escritos a mano o impresos
- Extracción automática de función objetivo y restricciones usando Gemini AI
- Formato de salida estructurado para procesamiento automático

### 2. Método Gráfico
- Visualización de restricciones como líneas en el plano
- Región factible resaltada en color
- Identificación automática de vértices
- Punto óptimo marcado claramente

### 3. Método Simplex ⭐ **NUEVO**
- Resolución paso a paso del problema
- Visualización de todas las iteraciones en tablas
- Resaltado de elementos pivote:
  - 🔴 **Rojo**: Elemento pivote
  - 🟡 **Amarillo**: Columna pivote
  - 🔵 **Azul**: Fila pivote
  - 🟣 **Lavanda**: Fila Z
- Solución óptima con valores detallados

⚠️ **NOTA**: El método Simplex solo soporta problemas de **MAXIMIZACIÓN**

## 📦 Instalación

### Requisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos

1. **Clonar o descargar el repositorio**
```bash
git clone <url-del-repositorio>
cd Optimization-Solver-with-Graphic-Method-And-AI
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar API Key de Gemini**
   
   Opción A: Crear archivo `.env` en la raíz del proyecto:
   ```
   GEMINI_API_KEY=tu_api_key_aqui
   ```
   
   Opción B: Ingresar la API key desde la interfaz gráfica al iniciar

   Para obtener una API key de Gemini:
   - Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Inicia sesión con tu cuenta de Google
   - Crea una nueva API key

## 🚀 Uso

### Ejecutar la aplicación
```bash
python main.py
```

### Flujo de trabajo

1. **Pestaña "Imagen del Problema"**
   - Clic en "Cargar Imagen"
   - Selecciona una imagen con el problema de programación lineal

2. **Pestaña "Análisis y Solución"**
   - Clic en "Analizar Problema"
   - Espera a que la IA procese la imagen
   - Revisa el análisis completo del problema

3. **Pestaña "Gráfica del Método"**
   - Visualiza automáticamente el método gráfico
   - Observa restricciones, región factible y punto óptimo

4. **Pestaña "Método Simplex"** ⭐ **NUEVO**
   - Clic en "Resolver con Método Simplex"
   - Revisa cada iteración del algoritmo
   - Observa el tableau inicial y todas las transformaciones
   - Identifica columnas y filas pivote en cada paso
   - Consulta la solución óptima al final

## 📁 Estructura del Proyecto

```
├── main.py                      # Interfaz gráfica principal
├── simplex_solver.py           # ⭐ Implementación del método Simplex
├── gemini_api.py               # Integración con Gemini AI
├── image_processor.py          # Procesamiento de imágenes
├── config.py                   # Gestión de configuración
├── test_simplex.py            # ⭐ Pruebas del solver Simplex
├── requirements.txt            # Dependencias
├── README.md                   # Este archivo
├── SIMPLEX_DOCUMENTATION.md    # ⭐ Documentación detallada del Simplex
└── .env                        # Configuración (crear manualmente)
```

## 🧪 Ejecutar Pruebas

Para verificar que el método Simplex funciona correctamente:

```bash
python test_simplex.py
```

Esto ejecutará múltiples casos de prueba y mostrará los resultados detallados.

## 📖 Formato de Problemas

### Función Objetivo
```
Maximizar Z = c1*x1 + c2*x2
```

### Restricciones
```
a1*x1 + a2*x2 <= b
x1 >= 0
x2 >= 0
```

### Ejemplo Completo
```
Maximizar Z = 3x1 + 2x2
Sujeto a:
  2x1 + 1x2 <= 10
  1x1 + 1x2 <= 6
  x1 <= 4
  x1, x2 >= 0
```

## 🎨 Capturas de Pantalla

### Ventana Principal
La interfaz tiene 4 pestañas:
1. Imagen del Problema
2. Análisis y Solución
3. Gráfica del Método
4. Método Simplex ⭐

### Método Simplex (Iteraciones)
Cada iteración muestra:
- Tableau completo con valores numéricos
- Variables básicas en cada fila
- Columna pivote resaltada en amarillo
- Fila pivote resaltada en azul
- Elemento pivote resaltado en rojo
- Información del pivote actual

## ⚙️ Configuración Avanzada

### Archivo .env
```env
GEMINI_API_KEY=tu_api_key_aqui
```

### Configuración de Ventana
La geometría de la ventana se guarda automáticamente en:
```
~/.linear_programming_solver_config.json
```

## 🔧 Solución de Problemas

### El botón de Simplex está deshabilitado
- Asegúrate de analizar una imagen primero
- Verifica que la IA extrajo correctamente los datos
- El problema debe ser de maximización

### Error "Este solver solo soporta problemas de MAXIMIZACIÓN"
- El método Simplex actual solo funciona con maximización
- Usa solo problemas de maximización o convierte manualmente

### La imagen no se analiza correctamente
- Usa imágenes claras y legibles
- Formatos soportados: PNG, JPG, JPEG, GIF, BMP
- Tamaño máximo: 5MB

### Error de API Key
- Verifica que la API key sea correcta
- Asegúrate de tener conexión a internet
- Revisa el archivo .env o configura desde la interfaz

## 🆕 Novedades (Versión con Simplex)

### Agregado
- ✅ Implementación completa del método Simplex
- ✅ Interfaz gráfica para visualizar iteraciones
- ✅ Resaltado de elementos pivote con colores
- ✅ Mostrar tableau inicial y todas las transformaciones
- ✅ Información detallada de cada iteración
- ✅ Solución óptima con valores de variables
- ✅ Suite de pruebas completa
- ✅ Documentación detallada del Simplex

### Características del Método Simplex
- Algoritmo Simplex estándar
- Solo maximización (por ahora)
- Variables de holgura automáticas
- Detección de solución óptima
- Detección de problemas no acotados
- Scroll para ver todas las iteraciones

## 🚧 Limitaciones Conocidas

1. **Método Simplex**: Solo maximización (no minimización)
2. **Variables**: Problemas con 2 variables (x1, x2)
3. **Restricciones**: Solo operador <= (menor o igual)
4. **Idioma**: Interfaz en español
5. **Formato**: La IA debe extraer correctamente el formato

## 📚 Documentación Adicional

- **[SIMPLEX_DOCUMENTATION.md](SIMPLEX_DOCUMENTATION.md)**: Guía completa del método Simplex
- **[2. Guía 2_ProgramaciónLineal_MétodoGráfico.pdf](2.%20Guía%202_ProgramaciónLineal_MétodoGráfico.pdf)**: Guía teórica (si existe)

## 🔮 Mejoras Futuras

- [ ] Soporte para minimización en Simplex
- [ ] Problemas con más de 2 variables
- [ ] Método de dos fases
- [ ] Variables artificiales
- [ ] Análisis de sensibilidad
- [ ] Exportar resultados a PDF
- [ ] Gráficas 3D para 3 variables
- [ ] Modo de comparación entre métodos

## 👨‍💻 Tecnologías Utilizadas

- **Python 3.x**: Lenguaje principal
- **Tkinter**: Interfaz gráfica
- **Matplotlib**: Visualización de gráficas
- **NumPy**: Cálculos numéricos y álgebra lineal
- **Pillow (PIL)**: Procesamiento de imágenes
- **Google Gemini AI**: Análisis de imágenes con IA
- **python-dotenv**: Gestión de variables de entorno

## 📄 Licencia

Este proyecto es de código abierto para fines educativos.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📞 Soporte

Para problemas o preguntas:
- Abre un issue en el repositorio
- Consulta la documentación en SIMPLEX_DOCUMENTATION.md

## 💡 Ejemplos de Uso

### Ejemplo 1: Problema Simple
```
Maximizar Z = 3x1 + 2x2
Sujeto a:
  2x1 + 1x2 <= 10
  1x1 + 1x2 <= 6
  x1, x2 >= 0

Solución óptima: x1 = 4, x2 = 2, Z = 16
```

### Ejemplo 2: Problema de Producción
```
Maximizar Z = 5x1 + 4x2
Sujeto a:
  6x1 + 4x2 <= 24
  x1 + 2x2 <= 6
  x1, x2 >= 0

Solución óptima: x1 = 3, x2 = 1.5, Z = 21
```

---

**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub**

**🎓 Proyecto educativo para aprendizaje de Programación Lineal**

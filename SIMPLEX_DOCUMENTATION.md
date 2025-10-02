# Documentación del Método Simplex

## Descripción General

Se ha agregado una nueva funcionalidad al Resolvedor de Programación Lineal que permite resolver problemas usando el **Método Simplex**. Esta funcionalidad trabaja en conjunto con la IA (Gemini) para extraer automáticamente los datos del problema y resolverlos paso a paso.

⚠️ **IMPORTANTE: Este solver solo soporta problemas de MAXIMIZACIÓN.**

## Características Principales

### 1. Pestaña de Método Simplex
- Nueva pestaña en la interfaz dedicada exclusivamente al método Simplex
- Visualización completa de todas las iteraciones del algoritmo
- Interfaz con scroll para navegar por todas las tablas

### 2. Visualización de Tablas
Cada iteración muestra:
- **Tableau completo** con todos los valores numéricos
- **Variables básicas** en cada fila
- **Nombres de columnas** (variables de decisión y holgura)
- **Columna RHS** (lado derecho de las ecuaciones)

### 3. Resaltado de Elementos Pivote
El sistema utiliza código de colores para facilitar la comprensión:

| Color | Significado |
|-------|-------------|
| 🔴 **Rojo** | Elemento pivote (celda seleccionada para pivoteo) |
| 🟡 **Amarillo** | Columna pivote (variable que entra a la base) |
| 🔵 **Azul claro** | Fila pivote (variable que sale de la base) |
| 🟣 **Lavanda** | Fila Z (función objetivo) |
| ⚪ **Blanco** | Celdas normales |

### 4. Información de Cada Iteración
Para cada iteración se muestra:
- Número de iteración (0 = Tableau Inicial)
- Columna pivote identificada
- Fila pivote identificada
- Valor del elemento pivote
- Indicador cuando se alcanza la solución óptima

## Cómo Usar

### Paso 1: Cargar y Analizar Imagen
1. Ve a la pestaña "Imagen del Problema"
2. Haz clic en "Cargar Imagen" y selecciona una imagen con el problema
3. Ve a la pestaña "Análisis y Solución"
4. Haz clic en "Analizar Problema"
5. Espera a que la IA extraiga los datos del problema

### Paso 2: Resolver con Simplex
1. Ve a la pestaña "Método Simplex"
2. Verifica que el botón "Resolver con Método Simplex" esté habilitado
3. Haz clic en el botón
4. El sistema resolverá automáticamente el problema

### Paso 3: Revisar Resultados
1. Observa el cuadro de "SOLUCIÓN ÓPTIMA" al inicio
2. Revisa cada iteración del método Simplex
3. Identifica las columnas y filas pivote en cada paso
4. Sigue el proceso hasta la solución óptima

## Estructura del Código

### Archivos Nuevos

#### `simplex_solver.py`
Módulo principal que implementa el algoritmo Simplex:

**Clase: `SimplexSolver`**
- `parse_problem()`: Parsea el problema desde formato texto
- `solve()`: Ejecuta el algoritmo Simplex
- `solve_from_text()`: Método conveniente para resolver desde strings
- `_save_iteration()`: Guarda información de cada iteración

**Métodos principales:**
```python
def solve_from_text(self, objective: str, restrictions: List[str]) -> Dict:
    """
    Resuelve un problema de programación lineal
    
    Args:
        objective: "Maximizar Z = 3x1 + 2x2"
        restrictions: ["2x1 + 1x2 <= 10", "1x1 + 1x2 <= 6", ...]
    
    Returns:
        Dict con estado, solución, valor óptimo e iteraciones
    """
```

### Modificaciones en Archivos Existentes

#### `main.py`
Se agregaron:
- Importación de `SimplexSolver`
- Nueva pestaña "Método Simplex" en el notebook
- Métodos para resolver y visualizar:
  - `solve_simplex()`: Inicia la resolución
  - `_solve_simplex_thread()`: Ejecuta Simplex en hilo separado
  - `_display_simplex_result()`: Muestra resultados
  - `_create_iteration_table()`: Crea tablas visuales

#### `gemini_api.py`
El prompt ya incluye la sección "DATOS PARA GRÁFICA" que ahora también se usa para el Simplex.

## Formato de Entrada

El sistema espera restricciones en el formato:
```
coef1 x1 + coef2 x2 <= valor
```

Ejemplos válidos:
- `2x1 + 3x2 <= 10`
- `1x1 + 1x2 <= 6`
- `x1 <= 4`
- `x2 >= 0`
- `-3x1 + 2x2 >= 5`

## Limitaciones Actuales

1. **Tipo de Problema**: **Solo soporta problemas de MAXIMIZACIÓN** (no minimización)
2. **Variables**: Actualmente soporta problemas con 2 variables (x1, x2)
3. **Restricciones**: Todas las restricciones deben ser lineales con operador <= (menor o igual)
4. **Método**: Solo implementa el método Simplex estándar (no el método de dos fases)
5. **Precisión**: Los cálculos se muestran con 4 decimales

## Ejemplos de Problemas Soportados

### Ejemplo 1: Maximización Simple
```
Maximizar Z = 3x1 + 2x2
Sujeto a:
  2x1 + 1x2 <= 10
  1x1 + 1x2 <= 6
  x1 <= 4
  x1, x2 >= 0
```

### Ejemplo 2: Maximización con Más Restricciones
```
Maximizar Z = 5x1 + 4x2
Sujeto a:
  6x1 + 4x2 <= 24
  x1 + 2x2 <= 6
  -x1 + x2 <= 1
  x2 <= 2
  x1, x2 >= 0
```

### Ejemplo 3: Problema de Producción
```
Maximizar Z = 40x1 + 30x2
Sujeto a:
  x1 + x2 <= 12
  2x1 + x2 <= 16
  x1, x2 >= 0
```

## Solución de Problemas

### El botón de Simplex está deshabilitado
- Asegúrate de haber analizado una imagen primero
- Verifica que la IA haya extraído correctamente los datos
- Revisa que el problema tenga función objetivo y restricciones válidas

### Error al resolver
- Verifica que las restricciones estén en formato correcto
- Asegúrate de que el problema sea factible
- Revisa que no haya errores de sintaxis en la imagen

### Las tablas no se muestran correctamente
- Usa el scroll vertical para ver todas las iteraciones
- Aumenta el tamaño de la ventana si es necesario
- Verifica que todas las restricciones sean válidas

## Mejoras Futuras

Posibles extensiones del sistema:
1. Soporte para más de 2 variables
2. Implementación del método de dos fases
3. Manejo de variables artificiales
4. Análisis de sensibilidad
5. Exportación de resultados a PDF
6. Gráficas 3D para problemas con 3 variables
7. Comparación entre método gráfico y Simplex

## Referencias

- Método Simplex: Algoritmo desarrollado por George Dantzig en 1947
- Programación Lineal: Técnica de optimización para problemas con restricciones lineales
- Tableau: Representación tabular del problema de programación lineal

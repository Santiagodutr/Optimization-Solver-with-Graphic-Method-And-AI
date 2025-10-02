import numpy as np
from typing import List, Dict, Tuple, Optional
import re

class SimplexSolver:
    """
    Implementación del método Simplex para resolver problemas de programación lineal.
    Solo soporta problemas de MAXIMIZACIÓN.
    """
    
    def __init__(self):
        """Inicializar el solver Simplex"""
        self.iterations = []
        self.optimal_solution = None
        self.optimal_value = None
        self.variable_names = []
        self.slack_variable_names = []
        
    def parse_problem(self, objective: str, restrictions: List[str]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Parsear el problema desde el formato de texto (solo maximización)
        
        Args:
            objective: Función objetivo en formato "Maximizar Z = 3x1 + 2x2"
            restrictions: Lista de restricciones en formato "2x1 + 1x2 <= 10"
            
        Returns:
            Tuple con (coeficientes_objetivo, matriz_restricciones, valores_derecha)
        """
        # Verificar que sea maximización
        if 'minimizar' in objective.lower() or 'min' in objective.lower():
            raise ValueError("Este solver solo soporta problemas de MAXIMIZACIÓN")
        
        # Extraer coeficientes de la función objetivo
        obj_match = re.search(r'Z\s*=\s*(.+)', objective, re.IGNORECASE)
        if not obj_match:
            raise ValueError("No se pudo parsear la función objetivo")
        
        obj_expr = obj_match.group(1).strip()
        c = self._parse_expression(obj_expr)
        n_vars = len(c)
        
        # Parsear restricciones
        A = []
        b = []
        
        for restriction in restrictions:
            # Limpiar restricción
            restriction = restriction.strip()
            
            # Saltar restricciones de no negatividad
            if '>= 0' in restriction or '≥ 0' in restriction:
                continue
            
            # Separar lado izquierdo y derecho
            for op in ['<=', '>=', '=', '≤', '≥']:
                if op in restriction:
                    parts = restriction.split(op)
                    if len(parts) == 2:
                        left = parts[0].strip()
                        right = parts[1].strip()
                        
                        # Parsear lado izquierdo
                        coeffs_left = self._parse_expression(left)
                        
                        # Verificar si el lado derecho tiene variables o es solo un número
                        coeffs_right = self._parse_expression(right)
                        
                        if coeffs_right and any(c != 0 for c in coeffs_right):
                            # Hay variables en el lado derecho, moverlas al lado izquierdo
                            # Asegurar que ambos lados tengan el mismo tamaño
                            max_len = max(len(coeffs_left), len(coeffs_right))
                            while len(coeffs_left) < max_len:
                                coeffs_left.append(0.0)
                            while len(coeffs_right) < max_len:
                                coeffs_right.append(0.0)
                            
                            # Restar lado derecho del izquierdo: ax1 + bx2 >= cx1 + dx2 -> (a-c)x1 + (b-d)x2 >= 0
                            coeffs = [coeffs_left[i] - coeffs_right[i] for i in range(max_len)]
                            rhs = 0.0
                        else:
                            # Lado derecho es solo un número
                            coeffs = coeffs_left
                            try:
                                rhs = float(right)
                            except ValueError:
                                continue
                        
                        # Asegurar que tenga el mismo número de variables que la función objetivo
                        while len(coeffs) < n_vars:
                            coeffs.append(0.0)
                        coeffs = coeffs[:n_vars]
                        
                        # Para >= convertir a <= multiplicando por -1
                        if op in ['>=', '≥']:
                            coeffs = [-x for x in coeffs]
                            rhs = -rhs
                        
                        # Solo agregar restricciones válidas con RHS positivo o cero
                        # (Simplex estándar requiere RHS >= 0)
                        if rhs >= -1e-10:  # Permitir pequeños errores numéricos
                            # Si RHS es negativo pequeño, ajustar a 0
                            if rhs < 0:
                                rhs = 0.0
                            A.append(coeffs)
                            b.append(rhs)
                        break
        
        # Convertir a arrays numpy
        c_array = np.array(c, dtype=float)
        A_array = np.array(A, dtype=float) if A else np.array([[]], dtype=float)
        b_array = np.array(b, dtype=float)
        
        return c_array, A_array, b_array
    
    def _parse_expression(self, expr: str) -> List[float]:
        """
        Parsear una expresión lineal como "3x1 + 2x2 - 5x3" o "40x1 + 30x2"
        
        Args:
            expr: Expresión a parsear
            
        Returns:
            Lista de coeficientes
        """
        # Limpiar expresión y convertir a minúsculas
        expr = expr.replace(' ', '').lower()
        
        # Patrón mejorado: captura coeficientes opcionales (incluyendo números grandes) antes de x
        # ([+-]?\d+\.?\d*) captura: signo opcional + uno o más dígitos + punto decimal opcional + más dígitos opcionales
        pattern = r'([+-]?\d+\.?\d*)?x(\d+)'
        matches = re.findall(pattern, expr)
        
        if not matches:
            return []
        
        # Determinar número de variables
        max_var = max(int(m[1]) for m in matches)
        coeffs = [0.0] * max_var
        
        # Asignar coeficientes
        for coef_str, var_num in matches:
            var_idx = int(var_num) - 1
            
            # Si coef_str está vacío, el coeficiente es 1 (o -1 si hay signo)
            if coef_str == '' or coef_str == '+':
                coef = 1.0
            elif coef_str == '-':
                coef = -1.0
            else:
                # Convertir el string del coeficiente a float
                coef = float(coef_str)
            
            coeffs[var_idx] = coef
        
        return coeffs
    
    def solve(self, c: np.ndarray, A: np.ndarray, b: np.ndarray) -> Dict:
        """
        Resolver el problema usando el método Simplex
        
        Args:
            c: Coeficientes de la función objetivo
            A: Matriz de restricciones
            b: Valores del lado derecho
            
        Returns:
            Diccionario con la solución y todas las iteraciones
        """
        # Inicializar
        self.iterations = []
        n_vars = len(c)
        n_constraints = len(b)
        
        # Crear nombres de variables
        self.variable_names = [f'x{i+1}' for i in range(n_vars)]
        self.slack_variable_names = [f's{i+1}' for i in range(n_constraints)]
        
        # Agregar variables de holgura para formar el tableau inicial
        # Tableau: [A | I | b]
        #          [c | 0 | 0]
        
        tableau = np.zeros((n_constraints + 1, n_vars + n_constraints + 1))
        
        # Llenar parte de restricciones
        tableau[:n_constraints, :n_vars] = A
        tableau[:n_constraints, n_vars:n_vars+n_constraints] = np.eye(n_constraints)
        tableau[:n_constraints, -1] = b
        
        # Llenar fila Z (función objetivo)
        tableau[-1, :n_vars] = -c  # Negativo porque estamos en forma estándar
        
        # Variables básicas iniciales (las de holgura)
        basic_vars = list(range(n_vars, n_vars + n_constraints))
        
        # Guardar tableau inicial
        self._save_iteration(tableau.copy(), basic_vars.copy(), -1, -1, 0)
        
        # Iterar hasta encontrar solución óptima
        iteration = 0
        max_iterations = 100
        
        while iteration < max_iterations:
            # Verificar si es óptimo (todos los coeficientes en fila Z son >= 0)
            if np.all(tableau[-1, :-1] >= -1e-10):
                # Solución óptima encontrada
                break
            
            # Seleccionar columna pivote (más negativo en fila Z)
            pivot_col = np.argmin(tableau[-1, :-1])
            
            # Verificar factibilidad (problema no acotado)
            if np.all(tableau[:-1, pivot_col] <= 0):
                return {
                    'status': 'unbounded',
                    'message': 'El problema no está acotado',
                    'iterations': self.iterations
                }
            
            # Seleccionar fila pivote (prueba del cociente mínimo)
            ratios = []
            for i in range(n_constraints):
                if tableau[i, pivot_col] > 1e-10:
                    ratio = tableau[i, -1] / tableau[i, pivot_col]
                    ratios.append((ratio, i))
                else:
                    ratios.append((float('inf'), i))
            
            # Encontrar mínimo ratio válido
            min_ratio = float('inf')
            pivot_row = -1
            for ratio, idx in ratios:
                if 0 <= ratio < min_ratio:
                    min_ratio = ratio
                    pivot_row = idx
            
            if pivot_row == -1:
                return {
                    'status': 'error',
                    'message': 'No se pudo encontrar fila pivote',
                    'iterations': self.iterations
                }
            
            # Realizar operación de pivoteo
            pivot_element = tableau[pivot_row, pivot_col]
            
            # Dividir fila pivote por elemento pivote
            tableau[pivot_row, :] /= pivot_element
            
            # Hacer ceros en el resto de la columna pivote
            for i in range(n_constraints + 1):
                if i != pivot_row:
                    factor = tableau[i, pivot_col]
                    tableau[i, :] -= factor * tableau[pivot_row, :]
            
            # Actualizar variable básica
            basic_vars[pivot_row] = pivot_col
            
            # Guardar iteración
            iteration += 1
            self._save_iteration(tableau.copy(), basic_vars.copy(), pivot_row, pivot_col, iteration)
        
        # Extraer solución
        solution = np.zeros(n_vars)
        for i, var_idx in enumerate(basic_vars):
            if var_idx < n_vars:
                solution[var_idx] = tableau[i, -1]
        
        # Valor óptimo
        z_value = tableau[-1, -1]
        
        self.optimal_solution = solution
        self.optimal_value = z_value
        
        return {
            'status': 'optimal',
            'solution': solution,
            'optimal_value': z_value,
            'iterations': self.iterations,
            'variable_names': self.variable_names
        }
    
    def _save_iteration(self, tableau: np.ndarray, basic_vars: List[int], 
                       pivot_row: int, pivot_col: int, iteration_num: int):
        """
        Guardar información de una iteración
        
        Args:
            tableau: Tableau actual
            basic_vars: Variables básicas actuales
            pivot_row: Fila pivote (-1 si es inicial)
            pivot_col: Columna pivote (-1 si es inicial)
            iteration_num: Número de iteración
        """
        n_vars = len(self.variable_names)
        n_slack = len(self.slack_variable_names)
        
        # Crear nombres de columnas
        col_names = self.variable_names + self.slack_variable_names + ['RHS']
        
        # Crear nombres de filas
        row_names = []
        for var_idx in basic_vars:
            if var_idx < n_vars:
                row_names.append(self.variable_names[var_idx])
            else:
                row_names.append(self.slack_variable_names[var_idx - n_vars])
        row_names.append('Z')
        
        iteration_data = {
            'iteration': iteration_num,
            'tableau': tableau.copy(),
            'basic_vars': basic_vars.copy(),
            'pivot_row': pivot_row,
            'pivot_col': pivot_col,
            'col_names': col_names,
            'row_names': row_names,
            'is_optimal': iteration_num > 0 and np.all(tableau[-1, :-1] >= -1e-10)
        }
        
        self.iterations.append(iteration_data)
    
    def solve_from_text(self, objective: str, restrictions: List[str]) -> Dict:
        """
        Resolver problema directamente desde formato texto
        
        Args:
            objective: Función objetivo como string
            restrictions: Lista de restricciones como strings
            
        Returns:
            Diccionario con solución completa
        """
        try:
            # Parsear problema
            c, A, b = self.parse_problem(objective, restrictions)
            
            # Validar que se parseó correctamente
            if len(c) == 0 or len(A) == 0:
                return {
                    'status': 'error',
                    'message': 'No se pudieron parsear las restricciones correctamente',
                    'iterations': []
                }
            
            # Resolver
            return self.solve(c, A, b)
        
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error al resolver: {str(e)}',
                'iterations': []
            }
    
    def get_iteration_summary(self, iteration_idx: int) -> str:
        """
        Obtener resumen de una iteración
        
        Args:
            iteration_idx: Índice de la iteración
            
        Returns:
            String con resumen
        """
        if iteration_idx >= len(self.iterations):
            return "Iteración no válida"
        
        iter_data = self.iterations[iteration_idx]
        
        summary = f"{'='*60}\n"
        if iter_data['iteration'] == 0:
            summary += "TABLA INICIAL\n"
        else:
            summary += f"ITERACIÓN {iter_data['iteration']}\n"
        summary += f"{'='*60}\n\n"
        
        if iter_data['pivot_row'] >= 0 and iter_data['pivot_col'] >= 0:
            col_name = iter_data['col_names'][iter_data['pivot_col']]
            row_name = iter_data['row_names'][iter_data['pivot_row']]
            pivot_val = iter_data['tableau'][iter_data['pivot_row'], iter_data['pivot_col']]
            
            summary += f"Columna Pivote: {col_name} (columna {iter_data['pivot_col']})\n"
            summary += f"Fila Pivote: {row_name} (fila {iter_data['pivot_row']})\n"
            summary += f"Elemento Pivote: {pivot_val:.4f}\n\n"
        
        if iter_data['is_optimal']:
            summary += "*** SOLUCIÓN ÓPTIMA ALCANZADA ***\n\n"
        
        return summary

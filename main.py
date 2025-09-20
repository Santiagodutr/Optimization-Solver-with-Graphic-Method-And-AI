import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import threading
import os
import matplotlib
matplotlib.use('TkAgg')  # Configurar backend antes de importar pyplot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
import re
from gemini_api import GeminiAPI
from image_processor import ImageProcessor
from config import Config

class LinearProgrammingGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Resolvedor de Programación Lineal con IA")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Configuración
        self.config = Config()
        self.gemini_api = None
        self.image_processor = ImageProcessor()
        self.current_image_path = None
        
        self.setup_ui()
        self.check_api_key()
    
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar pesos de grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Resolvedor de Programación Lineal con IA", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Solo mostrar configuración manual si no hay API key configurada
        api_key = self.config.get_api_key()
        if not api_key:
            # Frame de configuración manual si no hay .env
            api_frame = ttk.LabelFrame(main_frame, text="Configuración API", padding="10")
            api_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
            api_frame.columnconfigure(1, weight=1)
            
            ttk.Label(api_frame, text="API Key Gemini:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
            
            self.api_key_var = tk.StringVar()
            api_entry = ttk.Entry(api_frame, textvariable=self.api_key_var, show="*", width=60)
            api_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
            
            save_api_btn = ttk.Button(api_frame, text="Guardar", command=self.save_api_key)
            save_api_btn.grid(row=0, column=2)
        
        # Crear notebook para pestañas
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Pestaña 1: Imagen del problema
        image_frame = ttk.Frame(notebook, padding="10")
        notebook.add(image_frame, text="Imagen del Problema")
        image_frame.columnconfigure(0, weight=1)
        image_frame.rowconfigure(1, weight=1)
        
        # Botón para cargar imagen
        load_btn = ttk.Button(image_frame, text="Cargar Imagen", command=self.load_image)
        load_btn.grid(row=0, column=0, pady=(0, 10))
        
        # Canvas para mostrar imagen
        self.image_canvas = tk.Canvas(image_frame, bg="white", width=600, height=500)
        self.image_canvas.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Pestaña 2: Análisis y texto
        analysis_frame = ttk.Frame(notebook, padding="10")
        notebook.add(analysis_frame, text="Análisis y Solución")
        analysis_frame.columnconfigure(0, weight=1)
        analysis_frame.rowconfigure(1, weight=1)
        
        # Botón para analizar
        self.analyze_btn = ttk.Button(analysis_frame, text="Analizar Problema", 
                                    command=self.analyze_image, state="disabled")
        self.analyze_btn.grid(row=0, column=0, pady=(0, 10))
        
        # Área de texto para resultados
        self.result_text = scrolledtext.ScrolledText(analysis_frame, wrap=tk.WORD, 
                                                   width=80, height=30)
        self.result_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Pestaña 3: Gráfica
        graph_frame = ttk.Frame(notebook, padding="10")
        notebook.add(graph_frame, text="Gráfica del Método")
        graph_frame.columnconfigure(0, weight=1)
        graph_frame.rowconfigure(0, weight=1)
        
        # Crear figura de matplotlib
        self.fig = Figure(figsize=(10, 8), dpi=100, facecolor='white')
        self.ax = self.fig.add_subplot(111)
        
        # Canvas de matplotlib
        self.graph_canvas = FigureCanvasTkAgg(self.fig, graph_frame)
        self.graph_canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar el canvas
        self.graph_canvas.get_tk_widget().configure(background='white')
        
        # Inicializar con gráfica de ejemplo
        self._generate_initial_graph()
        
        # Actualizar canvas
        self.graph_canvas.draw()
        
        # Agregar toolbar de navegación (opcional)
        toolbar_frame = ttk.Frame(graph_frame)
        toolbar_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.toolbar = NavigationToolbar2Tk(self.graph_canvas, toolbar_frame)
        
        # Barra de progreso
        self.progress_frame = ttk.Frame(main_frame)
        self.progress_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        self.progress_frame.columnconfigure(1, weight=1)
        
        self.progress_label = ttk.Label(self.progress_frame, text="Listo")
        self.progress_label.grid(row=0, column=0, padx=(0, 10))
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, mode='indeterminate')
        self.progress_bar.grid(row=0, column=1, sticky=(tk.W, tk.E))
    
    def check_api_key(self):
        """Verificar si hay una API key configurada"""
        api_key = self.config.get_api_key()
        if api_key:
            self.gemini_api = GeminiAPI(api_key)
    
    def save_api_key(self):
        """Guardar la API key"""
        if hasattr(self, 'api_key_var'):
            api_key = self.api_key_var.get().strip()
            if not api_key:
                messagebox.showerror("Error", "Por favor ingresa una API key válida")
                return
            
            try:
                self.config.set_api_key(api_key)
                self.gemini_api = GeminiAPI(api_key)
                messagebox.showinfo("Éxito", "API key guardada correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar la API key: {str(e)}")
    
    def load_image(self):
        """Cargar imagen desde archivo"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[
                ("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Cargar y mostrar imagen
                image = Image.open(file_path)
                
                # Redimensionar imagen para el canvas
                canvas_width = self.image_canvas.winfo_width() or 600
                canvas_height = self.image_canvas.winfo_height() or 500
                
                # Mantener proporción
                image.thumbnail((canvas_width - 20, canvas_height - 20), Image.Resampling.LANCZOS)
                
                # Convertir para tkinter
                self.photo = ImageTk.PhotoImage(image)
                
                # Limpiar canvas y mostrar imagen
                self.image_canvas.delete("all")
                self.image_canvas.create_image(
                    canvas_width // 2, 
                    canvas_height // 2, 
                    image=self.photo
                )
                
                self.current_image_path = file_path
                self.analyze_btn.config(state="normal")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar la imagen: {str(e)}")
    
    def analyze_image(self):
        """Analizar imagen con Gemini API"""
        if not self.current_image_path:
            messagebox.showerror("Error", "Por favor carga una imagen primero")
            return
        
        if not self.gemini_api:
            messagebox.showerror("Error", "Por favor configura tu API key primero")
            return
        
        # Ejecutar en hilo separado para no bloquear la UI
        threading.Thread(target=self._analyze_image_thread, daemon=True).start()
    
    def _analyze_image_thread(self):
        """Hilo para análisis de imagen"""
        try:
            # Actualizar UI
            self.root.after(0, self._update_progress, True, "Procesando imagen...")
            
            # Procesar imagen
            image_data = self.image_processor.process_image(self.current_image_path)
            
            self.root.after(0, self._update_progress, True, "Enviando a Gemini AI...")
            
            # Enviar a Gemini
            response = self.gemini_api.analyze_linear_programming_problem(image_data)
            
            # Mostrar resultado
            self.root.after(0, self._display_result, response)
            
        except Exception as e:
            self.root.after(0, self._show_error, str(e))
        finally:
            self.root.after(0, self._update_progress, False, "Listo")
    
    def _update_progress(self, active, message):
        """Actualizar barra de progreso"""
        self.progress_label.config(text=message)
        if active:
            self.progress_bar.start()
            self.analyze_btn.config(state="disabled")
        else:
            self.progress_bar.stop()
            self.analyze_btn.config(state="normal")
    
    def _display_result(self, response):
        """Mostrar resultado en el área de texto y generar gráfica"""
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, response)
        
        # Generar gráfica basada en la respuesta
        self._generate_graph(response)
    
    def _show_error(self, error_message):
        """Mostrar error"""
        messagebox.showerror("Error", f"Error al analizar la imagen: {error_message}")
    
    def _generate_graph(self, response):
        """Generar gráfica del método gráfico después del análisis"""
        try:
            # Limpiar gráfica anterior
            self.ax.clear()
            
            print("Generando gráfica después del análisis...")
            
            # Intentar extraer datos específicos de la respuesta
            graph_data = self._extract_graph_data(response)
            
            if graph_data and graph_data.get('restrictions') and graph_data.get('vertices'):
                print("Usando datos extraídos de la IA")
                self._plot_from_ai_data(graph_data)
            else:
                print("Usando gráfica de ejemplo por defecto")
                self._plot_default_example()
                
        except Exception as e:
            print(f"Error generando gráfica: {e}")
            self._plot_error_message(str(e))
    
    def _extract_graph_data(self, response):
        """Extraer datos específicos de la sección DATOS PARA GRÁFICA"""
        try:
            # Buscar la sección de datos
            start_marker = "=== DATOS PARA GRÁFICA ==="
            end_marker = "=== FIN DATOS ==="
            
            start_idx = response.find(start_marker)
            end_idx = response.find(end_marker)
            
            if start_idx == -1 or end_idx == -1:
                print("No se encontró la sección de datos para gráfica")
                return None
            
            # Extraer la sección de datos
            data_section = response[start_idx + len(start_marker):end_idx].strip()
            
            # Parsear los datos
            graph_data = {
                'objective': None,
                'restrictions': [],
                'vertices': [],
                'optimal_point': None,
                'optimal_value': None
            }
            
            lines = data_section.split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if not line or line.startswith('==='):
                    continue
                
                if line.startswith('FUNCION_OBJETIVO:'):
                    graph_data['objective'] = line.replace('FUNCION_OBJETIVO:', '').strip()
                elif line.startswith('RESTRICCIONES:'):
                    current_section = 'restrictions'
                elif line.startswith('VERTICES:'):
                    current_section = 'vertices'
                elif line.startswith('SOLUCION_OPTIMA:'):
                    # Extraer punto óptimo: (x1, x2) = (valor, valor)
                    opt_match = re.search(r'\(([^,]+),\s*([^)]+)\)\s*=\s*\(([^,]+),\s*([^)]+)\)', line)
                    if opt_match:
                        x_val = float(opt_match.group(3).strip())
                        y_val = float(opt_match.group(4).strip())
                        graph_data['optimal_point'] = (x_val, y_val)
                elif line.startswith('VALOR_OPTIMO:'):
                    # Extraer valor óptimo
                    val_match = re.search(r'Z\s*=\s*([0-9.]+)', line)
                    if val_match:
                        graph_data['optimal_value'] = float(val_match.group(1))
                elif current_section == 'restrictions' and line.startswith('-'):
                    # Parsear restricción: - 1x1 + 1x2 <= 6
                    restriction = line[1:].strip()  # Quitar el '-'
                    graph_data['restrictions'].append(restriction)
                elif current_section == 'vertices' and line.startswith('-'):
                    # Parsear vértice: - (x1, x2) = (0, 6)
                    vertex_match = re.search(r'\(([^,]+),\s*([^)]+)\)\s*=\s*\(([^,]+),\s*([^)]+)\)', line)
                    if vertex_match:
                        x_val = float(vertex_match.group(3).strip())
                        y_val = float(vertex_match.group(4).strip())
                        graph_data['vertices'].append((x_val, y_val))
            
            print(f"Datos extraídos: {len(graph_data['restrictions'])} restricciones, {len(graph_data['vertices'])} vértices")
            return graph_data
            
        except Exception as e:
            print(f"Error extrayendo datos: {e}")
            return None
    
    def _plot_from_ai_data(self, graph_data):
        """Graficar usando los datos extraídos de la IA"""
        try:
            # Determinar límites del gráfico
            max_coord = 10
            if graph_data['vertices']:
                max_x = max(v[0] for v in graph_data['vertices'])
                max_y = max(v[1] for v in graph_data['vertices'])
                max_coord = max(max_x, max_y) * 1.2
            
            x = np.linspace(0, max_coord, 200)
            
            # Graficar restricciones
            colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
            restriction_lines = []
            
            print(f"Graficando {len(graph_data['restrictions'])} restricciones...")
            
            for i, restriction in enumerate(graph_data['restrictions']):
                try:
                    coeffs = self._parse_restriction_format(restriction)
                    if coeffs:
                        a, b, c, operator = coeffs
                        color = colors[i % len(colors)]
                        
                        print(f"Restricción {i+1}: a={a}, b={b}, c={c}, op={operator}")
                        
                        # Caso 1: Restricción con ambas variables (a≠0 y b≠0)
                        if a != 0 and b != 0:
                            # ax1 + bx2 <= c  ->  x2 = (c - ax1)/b
                            y = (c - a * x) / b
                            y = np.clip(y, 0, max_coord)
                            self.ax.plot(x, y, color=color, linewidth=3, 
                                       label=f'{restriction[:25]}{"..." if len(restriction) > 25 else ""}', 
                                       alpha=0.8)
                            print(f"  Graficada línea inclinada")
                        
                        # Caso 2: Solo restricción en x1 (línea vertical)
                        elif a != 0 and b == 0:
                            if operator in ['<=', '≤']:
                                x_line = c / a
                                if 0 <= x_line <= max_coord:
                                    self.ax.axvline(x=x_line, color=color, linewidth=3,
                                                  label=f'{restriction}', alpha=0.8)
                                    print(f"  Graficada línea vertical en x={x_line}")
                            elif operator in ['>=', '≥']:
                                x_line = c / a
                                if x_line >= 0:  # x1 >= valor
                                    if x_line <= max_coord:
                                        self.ax.axvline(x=x_line, color=color, linewidth=3,
                                                      label=f'{restriction}', alpha=0.8, linestyle='--')
                                    print(f"  Graficada línea vertical >= en x={x_line}")
                        
                        # Caso 3: Solo restricción en x2 (línea horizontal)  
                        elif a == 0 and b != 0:
                            if operator in ['<=', '≤']:
                                y_line = c / b
                                if 0 <= y_line <= max_coord:
                                    self.ax.axhline(y=y_line, color=color, linewidth=3,
                                                  label=f'{restriction}', alpha=0.8)
                                    print(f"  Graficada línea horizontal en y={y_line}")
                            elif operator in ['>=', '≥']:
                                y_line = c / b
                                if y_line >= 0:  # x2 >= valor
                                    if y_line <= max_coord:
                                        self.ax.axhline(y=y_line, color=color, linewidth=3,
                                                      label=f'{restriction}', alpha=0.8, linestyle='--')
                                    print(f"  Graficada línea horizontal >= en y={y_line}")
                        
                        # Caso 4: Restricciones de no negatividad (ya cubiertas arriba, pero por claridad)
                        if c == 0 and operator in ['>=', '≥']:
                            if a == 1 and b == 0:  # x1 >= 0
                                # No graficar explícitamente, ya está el eje
                                print(f"  x1 >= 0 (eje izquierdo)")
                            elif a == 0 and b == 1:  # x2 >= 0  
                                # No graficar explícitamente, ya está el eje
                                print(f"  x2 >= 0 (eje inferior)")
                    else:
                        print(f"No se pudo parsear la restricción: '{restriction}'")
                        
                except Exception as e:
                    print(f"Error graficando restricción '{restriction}': {e}")
            
            # Graficar región factible si tenemos vértices
            if graph_data['vertices'] and len(graph_data['vertices']) >= 3:
                vertices = graph_data['vertices']
                # Ordenar vértices para formar un polígono convexo
                vertices_sorted = self._sort_vertices_convex(vertices)
                
                vertices_x = [v[0] for v in vertices_sorted] + [vertices_sorted[0][0]]
                vertices_y = [v[1] for v in vertices_sorted] + [vertices_sorted[0][1]]
                
                # Dibujar región factible
                self.ax.fill(vertices_x, vertices_y, alpha=0.4, color='lightgreen',
                           label='Región Factible', zorder=1)
                self.ax.plot(vertices_x, vertices_y, 'k-', linewidth=2, zorder=2)
                
                # Marcar vértices
                for i, (vx, vy) in enumerate(vertices_sorted):
                    self.ax.plot(vx, vy, 'ko', markersize=10, zorder=3)
                    self.ax.annotate(f'V{i+1}({vx}, {vy})', (vx, vy),
                                   xytext=(15, 15), textcoords='offset points',
                                   fontsize=10, fontweight='bold',
                                   bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow',
                                           alpha=0.9, edgecolor='black'))
            
            # Marcar punto óptimo
            if graph_data['optimal_point']:
                ox, oy = graph_data['optimal_point']
                self.ax.plot(ox, oy, 'r*', markersize=25, label='★ SOLUCIÓN ÓPTIMA', zorder=5)
                
                opt_label = f"ÓPTIMO\n({ox}, {oy})"
                if graph_data['optimal_value']:
                    opt_label += f"\nZ = {graph_data['optimal_value']}"
                
                self.ax.annotate(opt_label, (ox, oy),
                               xytext=(20, -40), textcoords='offset points',
                               fontsize=12, fontweight='bold', ha='center',
                               bbox=dict(boxstyle='round,pad=0.5', facecolor='red',
                                       alpha=0.9, edgecolor='darkred'),
                               color='white', zorder=6)
            
            # Configurar gráfica
            self.ax.set_xlim(-0.5, max_coord)
            self.ax.set_ylim(-0.5, max_coord)
            self.ax.set_xlabel('X₁ (Variable 1)', fontsize=14, fontweight='bold')
            self.ax.set_ylabel('X₂ (Variable 2)', fontsize=14, fontweight='bold')
            
            title = 'SOLUCIÓN POR MÉTODO GRÁFICO'
            if graph_data['objective']:
                title += f"\n{graph_data['objective']}"
            
            self.ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            self.ax.grid(True, alpha=0.4, linewidth=1)
            self.ax.legend(loc='upper right', fontsize=10, framealpha=0.9)
            
            # Ejes de coordenadas
            self.ax.axhline(y=0, color='black', linewidth=1)
            self.ax.axvline(x=0, color='black', linewidth=1)
            
            # Mejorar apariencia
            self.ax.set_facecolor('#f8f9fa')
            self.fig.patch.set_facecolor('white')
            self.fig.tight_layout()
            
            # Actualizar canvas
            self.graph_canvas.draw()
            self.graph_canvas.flush_events()
            
        except Exception as e:
            print(f"Error en _plot_from_ai_data: {e}")
            self._plot_default_example()
    
    def _parse_restriction_format(self, restriction):
        """Parsear restricción en el formato: coef x1 + coef x2 <= valor"""
        try:
            # Limpiar y normalizar
            clean = restriction.replace(' ', '').lower().replace('≤', '<=').replace('≥', '>=')
            
            print(f"Parseando restricción: '{restriction}' -> '{clean}'")
            
            # Patrones más completos para extraer coeficientes
            patterns = [
                # Formato completo: ax1+bx2<=c (incluye coeficientes negativos)
                r'([+-]?\d*\.?\d*)x1([+-]\d*\.?\d*)x2([<>=]{1,2})(\d+\.?\d*)',
                # Solo x1 con coeficiente: ax1<=c
                r'([+-]?\d*\.?\d*)x1([<>=]{1,2})(\d+\.?\d*)',
                # Solo x2 con coeficiente: bx2<=c  
                r'([+-]?\d*\.?\d*)x2([<>=]{1,2})(\d+\.?\d*)',
                # x1 sin coeficiente con x2: x1+bx2<=c
                r'x1([+-]\d*\.?\d*)x2([<>=]{1,2})(\d+\.?\d*)',
                # Solo x1 sin coeficiente: x1<=c
                r'x1([<>=]{1,2})(\d+\.?\d*)',
                # Solo x2 sin coeficiente: x2<=c
                r'x2([<>=]{1,2})(\d+\.?\d*)',
                # Casos especiales de no negatividad
                r'x1([<>=]{1,2})0',
                r'x2([<>=]{1,2})0'
            ]
            
            for i, pattern in enumerate(patterns):
                match = re.search(pattern, clean)
                if match:
                    groups = match.groups()
                    print(f"  Patrón {i+1} coincide: {groups}")
                    
                    if len(groups) == 4:  # ax1+bx2<=c
                        a_str = groups[0]
                        b_str = groups[1]
                        op = groups[2]
                        c = float(groups[3])
                        
                        # Manejar coeficiente de x1
                        if a_str == '' or a_str == '+':
                            a = 1
                        elif a_str == '-':
                            a = -1
                        else:
                            a = float(a_str)
                        
                        # Manejar coeficiente de x2
                        if b_str == '' or b_str == '+':
                            b = 1
                        elif b_str == '-':
                            b = -1
                        else:
                            b = float(b_str)
                        
                        print(f"  Resultado: a={a}, b={b}, c={c}, op={op}")
                        return (a, b, c, op)
                        
                    elif len(groups) == 3:
                        if 'x1' in pattern and '+' not in pattern and 'x2' not in pattern:  # ax1<=c
                            a_str = groups[0]
                            op = groups[1]  
                            c = float(groups[2])
                            
                            if a_str == '' or a_str == '+':
                                a = 1
                            elif a_str == '-':
                                a = -1
                            else:
                                a = float(a_str)
                            
                            print(f"  x1 restricción: a={a}, b=0, c={c}, op={op}")
                            return (a, 0, c, op)
                            
                        elif 'x2' in pattern and '+' not in pattern and 'x1' not in pattern:  # bx2<=c
                            b_str = groups[0]
                            op = groups[1]
                            c = float(groups[2])
                            
                            if b_str == '' or b_str == '+':
                                b = 1
                            elif b_str == '-':
                                b = -1
                            else:
                                b = float(b_str)
                            
                            print(f"  x2 restricción: a=0, b={b}, c={c}, op={op}")
                            return (0, b, c, op)
                            
                        elif 'x1' in pattern and 'x2' in pattern:  # x1+bx2<=c
                            b_str = groups[0]
                            op = groups[1]
                            c = float(groups[2])
                            
                            if b_str == '' or b_str == '+':
                                b = 1
                            elif b_str == '-':
                                b = -1
                            else:
                                b = float(b_str)
                            
                            print(f"  x1+x2 restricción: a=1, b={b}, c={c}, op={op}")
                            return (1, b, c, op)
                    
                    elif len(groups) == 2:  # x1<=c o x2<=c
                        op = groups[0]
                        c = float(groups[1]) if groups[1] != '0' else 0
                        
                        if 'x1' in pattern:
                            print(f"  x1 simple: a=1, b=0, c={c}, op={op}")
                            return (1, 0, c, op)
                        else:
                            print(f"  x2 simple: a=0, b=1, c={c}, op={op}")
                            return (0, 1, c, op)
                    
                    elif len(groups) == 1:  # x1>=0 o x2>=0
                        op = groups[0]
                        c = 0
                        
                        if 'x1' in pattern:
                            print(f"  x1>=0: a=1, b=0, c=0, op={op}")
                            return (1, 0, c, op)
                        else:
                            print(f"  x2>=0: a=0, b=1, c=0, op={op}")
                            return (0, 1, c, op)
            
            print(f"  No se pudo parsear la restricción")
            return None
            
        except Exception as e:
            print(f"Error parseando restricción '{restriction}': {e}")
            return None
    
    def _sort_vertices_convex(self, vertices):
        """Ordenar vértices para formar polígono convexo"""
        if len(vertices) <= 2:
            return vertices
        
        # Encontrar centroide
        cx = sum(v[0] for v in vertices) / len(vertices)
        cy = sum(v[1] for v in vertices) / len(vertices)
        
        # Ordenar por ángulo polar desde el centroide
        def polar_angle(vertex):
            return np.arctan2(vertex[1] - cy, vertex[0] - cx)
        
        return sorted(vertices, key=polar_angle)
    
    def _plot_default_example(self):
        """Graficar ejemplo por defecto si no se pueden extraer datos"""
        try:
            # Crear gráfica mejorada basada en análisis
            x = np.linspace(0, 10, 200)
            
            # Restricciones de ejemplo
            # x1 + x2 <= 8
            y1 = 8 - x
            y1 = np.clip(y1, 0, 10)
            
            # 2x1 + x2 <= 12  
            y2 = 12 - 2*x
            y2 = np.clip(y2, 0, 10)
            
            # Graficar restricciones
            self.ax.plot(x, y1, 'r-', linewidth=3, label='x₁ + x₂ ≤ 8')
            self.ax.plot(x, y2, 'b-', linewidth=3, label='2x₁ + x₂ ≤ 12')
            self.ax.axvline(x=5, color='g', linewidth=3, label='x₁ ≤ 5')
            
            # Ejes
            self.ax.axhline(y=0, color='black', linewidth=1)
            self.ax.axvline(x=0, color='black', linewidth=1)
            
            # Región factible
            vertices_x = [0, 0, 4, 5, 0]
            vertices_y = [0, 8, 4, 2, 0]
            
            self.ax.fill(vertices_x, vertices_y, alpha=0.4, color='lightgreen', 
                        label='Región Factible')
            self.ax.plot(vertices_x, vertices_y, 'k-', linewidth=2)
            
            # Vértices
            vertices = [(0, 0), (0, 8), (4, 4), (5, 2)]
            for i, (vx, vy) in enumerate(vertices):
                self.ax.plot(vx, vy, 'ko', markersize=10)
                self.ax.annotate(f'({vx}, {vy})', (vx, vy), 
                               xytext=(15, 15), textcoords='offset points',
                               bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow'))
            
            # Punto óptimo
            self.ax.plot(4, 4, 'r*', markersize=25, label='★ SOLUCIÓN ÓPTIMA')
            
            # Configurar
            self.ax.set_xlim(-0.5, 9)
            self.ax.set_ylim(-0.5, 9)
            self.ax.set_xlabel('X₁ (Variable 1)', fontsize=14, fontweight='bold')
            self.ax.set_ylabel('X₂ (Variable 2)', fontsize=14, fontweight='bold')
            self.ax.set_title('MÉTODO GRÁFICO - EJEMPLO', fontsize=16, fontweight='bold')
            self.ax.grid(True, alpha=0.4)
            self.ax.legend(loc='upper right', fontsize=11)
            
            # Actualizar
            self.fig.tight_layout()
            self.graph_canvas.draw()
            self.graph_canvas.flush_events()
            
        except Exception as e:
            self._plot_error_message(str(e))
    
    def _plot_error_message(self, error_msg):
        """Mostrar mensaje de error en la gráfica"""
        try:
            self.ax.clear()
            self.ax.text(0.5, 0.5, f'Error al generar gráfica:\n\n{error_msg}\n\nRevisa la consola para más detalles', 
                        horizontalalignment='center', verticalalignment='center',
                        transform=self.ax.transAxes, fontsize=12,
                        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightcoral', alpha=0.8))
            self.ax.set_title("Error en Gráfica")
            self.ax.set_xlabel('X₁')
            self.ax.set_ylabel('X₂')
            self.graph_canvas.draw()
        except:
            print(f"Error crítico en gráfica: {error_msg}")
    
    def _generate_initial_graph(self):
        """Generar gráfica inicial con un ejemplo básico"""
        try:
            # Limpiar la gráfica
            self.ax.clear()
            
            # Crear un ejemplo simple funcional
            x = np.linspace(0, 10, 100)
            
            # Ejemplo: Maximizar Z = 3x + 2y
            # Restricciones:
            # x + y <= 6
            y1 = 6 - x
            y1 = np.clip(y1, 0, 10)
            
            # 2x + y <= 10
            y2 = 10 - 2*x
            y2 = np.clip(y2, 0, 10)
            
            # x <= 4
            x_limit = 4
            
            # Graficar restricciones
            self.ax.plot(x, y1, 'r-', linewidth=2, label='x + y ≤ 6')
            self.ax.plot(x, y2, 'b-', linewidth=2, label='2x + y ≤ 10')
            self.ax.axvline(x=x_limit, color='g', linewidth=2, label='x ≤ 4')
            
            # Ejes
            self.ax.axhline(y=0, color='k', linewidth=1, alpha=0.5)
            self.ax.axvline(x=0, color='k', linewidth=1, alpha=0.5)
            
            # Región factible (polígono)
            vertices_x = [0, 0, 2, 4, 0]
            vertices_y = [0, 6, 4, 0, 0]
            
            self.ax.fill(vertices_x, vertices_y, alpha=0.3, color='lightblue', label='Región Factible')
            self.ax.plot(vertices_x, vertices_y, 'k-', linewidth=2)
            
            # Marcar vértices
            vertices = [(0, 0), (0, 6), (2, 4), (4, 0)]
            for i, (vx, vy) in enumerate(vertices):
                self.ax.plot(vx, vy, 'ko', markersize=8)
                self.ax.annotate(f'({vx}, {vy})', (vx, vy), 
                               xytext=(10, 10), textcoords='offset points',
                               fontsize=10, ha='left',
                               bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.8))
            
            # Punto óptimo
            opt_x, opt_y = 2, 4
            self.ax.plot(opt_x, opt_y, 'r*', markersize=20, label='Punto Óptimo (2, 4)', zorder=5)
            
            # Configuración de la gráfica
            self.ax.set_xlim(-0.5, 8)
            self.ax.set_ylim(-0.5, 8)
            self.ax.set_xlabel('X₁ (Variable 1)', fontsize=12)
            self.ax.set_ylabel('X₂ (Variable 2)', fontsize=12)
            self.ax.set_title('Método Gráfico - Ejemplo de Programación Lineal', fontsize=14, fontweight='bold')
            self.ax.grid(True, alpha=0.3)
            self.ax.legend(loc='upper right')
            
            # Ajustar layout
            self.fig.tight_layout()
            
        except Exception as e:
            # Si hay error, mostrar mensaje simple
            self.ax.clear()
            self.ax.text(0.5, 0.5, f'Cargando gráfica...\n\nCarga una imagen y analízala\npara ver el método gráfico', 
                        horizontalalignment='center', verticalalignment='center',
                        transform=self.ax.transAxes, fontsize=14,
                        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.8))
            self.ax.set_title("Gráfica del Método Gráfico")
            print(f"Error en gráfica inicial: {e}")
    
    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

def main():
    """Función principal"""
    app = LinearProgrammingGUI()
    app.run()

if __name__ == "__main__":
    main()
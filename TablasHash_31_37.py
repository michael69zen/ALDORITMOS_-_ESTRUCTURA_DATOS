# ================================================================ 
# EXPERIMENTO: CONSTANTE BASE POLINOMIAL (p=31 vs p=37)
# ================================================================ 

import pandas as pd
import time
import os
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────────────────────── 
# 1. PREPARACIÓN (Carga de datos)
# ─────────────────────────────────────────────────────────────── 
def cargar_claves(ruta_csv: str, columna_clave: str) -> list:
    if not os.path.exists(ruta_csv):
        print(f"Error: No se encontró el archivo {ruta_csv}")
        return []
    
    # Carga el CSV y extrae solo los Student_ID únicos
    df = pd.read_csv(ruta_csv, low_memory=False)
    df.dropna(subset=[columna_clave], inplace=True)
    claves = df[columna_clave].astype(str).str.strip().unique().tolist()
    
    return claves

# ─────────────────────────────────────────────────────────────── 
# 2. FUNCIÓN HASH PARAMETRIZABLE
# ─────────────────────────────────────────────────────────────── 
def hash_polinomial(clave: str, tamanio: int, p: int) -> int:
    hash_val = 0
    for c in str(clave):
        hash_val = (hash_val * p + ord(c)) % tamanio
    return hash_val

# ─────────────────────────────────────────────────────────────── 
# 3. TABLA HASH EXPERIMENTAL (Encadenamiento)
# ─────────────────────────────────────────────────────────────── 
class TablaHashTest:
    def __init__(self, tamanio: int, p: int):
        self.tamanio = tamanio
        self.p = p
        self.tabla = [[] for _ in range(tamanio)]
        self.colisiones = 0

    def insertar(self, clave: str):
        idx = hash_polinomial(clave, self.tamanio, self.p)
        if self.tabla[idx]:  # Si la lista no está vacía, hay colisión
            self.colisiones += 1
        self.tabla[idx].append(clave)

    def buscar(self, clave: str) -> bool:
        idx = hash_polinomial(clave, self.tamanio, self.p)
        for k in self.tabla[idx]:
            if k == clave:
                return True
        return False

# ─────────────────────────────────────────────────────────────── 
# 4. EJECUCIÓN, MEDICIÓN Y EVALUACIÓN
# ─────────────────────────────────────────────────────────────── 
def ejecutar_experimento(claves: list):
    n = len(claves)
    
    # Calcular un tamaño de tabla primo (m) para un factor de carga de ~0.65
    m_ideal = int(n / 0.65)
    
    def es_primo(num):
        if num < 2: return False
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0: return False
        return True
    
    m = m_ideal | 1  # Aseguramos que sea impar
    while not es_primo(m):
        m += 2
        
    print("="*60)
    print(" INICIANDO EXPERIMENTO DE COLISIONES ")
    print("="*60)
    print(f"Total de claves únicas (N): {n}")
    print(f"Tamaño de tabla primo (m) seleccionado: {m}")
    
    resultados = {}
    
    # Probamos con ambas constantes
    for p in [31, 37]:
        tabla = TablaHashTest(m, p)
        
        # Insertamos todos los datos
        for clave in claves:
            tabla.insertar(clave)
            
        # Medimos el tiempo de búsqueda (buscando todas las claves)
        t0 = time.perf_counter()
        for clave in claves:
            tabla.buscar(clave)
        t_busqueda = (time.perf_counter() - t0) * 1000  # en milisegundos
        
        resultados[p] = {
            'colisiones': tabla.colisiones,
            'tiempo_ms': t_busqueda
        }
        
        print(f"\nResultados para p = {p}:")
        print(f" -> Colisiones totales: {tabla.colisiones}")
        print(f" -> Tiempo de búsqueda: {t_busqueda:.3f} ms")

    # ─────────────────────────────────────────────────────────────── 
    # 5. CONCLUSIÓN AUTOMÁTICA
    # ─────────────────────────────────────────────────────────────── 
    c31 = resultados[31]['colisiones']
    c37 = resultados[37]['colisiones']
    
    print("\n" + "="*60)
    print(" CONCLUSIÓN ")
    print("="*60)
    if c31 < c37:
        print(f"El valor p=31 es más eficiente para tu dataset.")
        print(f"Redujo las colisiones en {c37 - c31} respecto a p=37.")
    elif c37 < c31:
        print(f"El valor p=37 es más eficiente para tu dataset.")
        print(f"Redujo las colisiones en {c31 - c37} respecto a p=31.")
    else:
        print("Ambos valores (p=31 y p=37) generaron exactamente la misma cantidad de colisiones.")
        
    # Graficar resultados
    bases = ['p = 31', 'p = 37']
    cols = [c31, c37]
    tiempos = [resultados[31]['tiempo_ms'], resultados[37]['tiempo_ms']]
    
    fig, ax1 = plt.subplots(1, 2, figsize=(10, 4))
    
    # Gráfico de Colisiones
    ax1[0].bar(bases, cols, color=['#4C72B0', '#DD8452'])
    ax1[0].set_title('Total de Colisiones')
    ax1[0].set_ylabel('Número de colisiones')
    for i, v in enumerate(cols):
        ax1[0].text(i, v + (max(cols)*0.02), str(v), ha='center', fontweight='bold')
        
    # Gráfico de Tiempos
    ax1[1].bar(bases, tiempos, color=['#4C72B0', '#DD8452'])
    ax1[1].set_title('Tiempo de Búsqueda (ms)')
    ax1[1].set_ylabel('Milisegundos')
    for i, v in enumerate(tiempos):
        ax1[1].text(i, v + (max(tiempos)*0.02), f"{v:.2f}", ha='center', fontweight='bold')
        
    plt.tight_layout()
    nombre_img = 'experimento_constante_p.png'
    plt.savefig(nombre_img, dpi=150)
    print(f"\n[!] Gráfico guardado exitosamente como '{nombre_img}'.")
    plt.show()

# ─────────────────────────────────────────────────────────────── 
# PUNTO DE ENTRADA
# ─────────────────────────────────────────────────────────────── 
if __name__ == '__main__':
    archivo_csv = 'AI_Impact_Student_Life_2026.csv'
    columna_id = 'Student_ID'
    
    claves_dataset = cargar_claves(archivo_csv, columna_id)
    
    if claves_dataset:
        ejecutar_experimento(claves_dataset)

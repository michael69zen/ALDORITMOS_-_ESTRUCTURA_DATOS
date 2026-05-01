# ================================================================ 
# PRÁCTICA: TABLAS HASH CON DATOS REALES DE KAGGLE 
# Curso: Estructuras de Datos | Semanas 5-6 
# ================================================================ 

import pandas as pd             # Carga y limpieza de datos CSV 
import time                     # Medición de tiempos de ejecución 
import matplotlib.pyplot as plt # Generación de gráficos 
import hashlib                  # Para funciones hash criptográficas 
import random                   # Generación de datos sintéticos 
import os 

# ─────────────────────────────────────────────────────────────── 
# 1. CARGA Y LIMPIEZA DE DATOS DESDE CSV 
# ─────────────────────────────────────────────────────────────── 
def cargar_datos(ruta_csv: str, columna_clave: str, columna_valor: str) -> list: 
    """Carga un CSV y extrae la columna clave y valor para hashing.""" 
    if not os.path.exists(ruta_csv):
        print(f"Error: No se encontró el archivo {ruta_csv}")
        return []
    
    df = pd.read_csv(ruta_csv, low_memory=False)  # Lee el CSV 
    df.dropna(subset=[columna_clave], inplace=True)  # Elimina filas sin clave 
    df[columna_clave] = df[columna_clave].astype(str).str.strip()  # Normaliza clave
    
    # Convierte a lista de tuplas (clave, valor)
    datos = list(zip(df[columna_clave], df[columna_valor]))
    print(f'Registros cargados: {len(datos)}')   # Muestra cantidad 
    return datos 

# ─────────────────────────────────────────────────────────────── 
# 2. FUNCIÓN HASH PERSONALIZADA 
# ─────────────────────────────────────────────────────────────── 
def funcion_hash(clave: str, tamanio: int) -> int: 
    """Función hash polinomial: h(k) = sum(ord(c)*31^i) mod tamanio.""" 
    hash_val = 0 
    for c in str(clave):  # Itera sobre cada carácter 
        hash_val = (hash_val * 31 + ord(c)) % tamanio  # Acumula hash 
    return hash_val  # Retorna índice en la tabla 

# ─────────────────────────────────────────────────────────────── 
# 3. TABLA HASH CON ENCADENAMIENTO SEPARADO 
# ─────────────────────────────────────────────────────────────── 
class TablaHashEncadenamiento: 
    def __init__(self, tamanio: int): 
        self.tamanio = tamanio                # Capacidad de la tabla 
        self.tabla = [[] for _ in range(tamanio)]  # Lista de listas (cadenas) 
        self.colisiones = 0                   # Contador de colisiones 
        self.elementos = 0                    # Número de elementos insertados 

    def insertar(self, clave: str, valor=None): 
        idx = funcion_hash(clave, self.tamanio)   # Calcula índice 
        if self.tabla[idx]:                       # Si la cadena no está vacía 
            self.colisiones += 1                  # Registra colisión 
        self.tabla[idx].append((clave, valor))    # Agrega par clave-valor 
        self.elementos += 1                       # Incrementa contador 

    def buscar(self, clave: str): 
        idx = funcion_hash(clave, self.tamanio)   # Calcula índice
        for k, v in self.tabla[idx]:              # Recorre la cadena 
            if k == clave:                        # Si encuentra la clave 
                return v                          # Retorna el valor 
        return None                               # No encontrado 

    def factor_de_carga(self) -> float: 
        return self.elementos / self.tamanio      # λ = n / m 

# ─────────────────────────────────────────────────────────────── 
# 4. TABLA HASH CON SONDEO LINEAL 
# ─────────────────────────────────────────────────────────────── 
class TablaHashSondeoLineal: 
    ELIMINADO = '__ELIMINADO__'  # Marcador para celdas borradas 

    def __init__(self, tamanio: int): 
        self.tamanio = tamanio 
        self.tabla = [None] * tamanio        # Arreglo de slots 
        self.colisiones = 0 
        self.elementos = 0 

    def insertar(self, clave: str, valor=None): 
        if self.elementos >= self.tamanio * 0.75:  # Umbral de carga 75% 
            raise OverflowError('Tabla llena: factor de carga superado') 
        
        idx = funcion_hash(clave, self.tamanio)    # Índice inicial 
        pasos = 0 
        while self.tabla[idx] is not None and self.tabla[idx] != self.ELIMINADO: 
            self.colisiones += 1           # Colisión detectada 
            idx = (idx + 1) % self.tamanio # Sondeo lineal: h(k,i) = (h(k)+i) mod m 
            pasos += 1 
            if pasos >= self.tamanio:      # Evita bucle infinito 
                raise OverflowError('No hay espacio disponible') 
        
        self.tabla[idx] = (clave, valor)   # Inserta en la posición libre 
        self.elementos += 1 

    def buscar(self, clave: str): 
        idx = funcion_hash(clave, self.tamanio) 
        pasos = 0 
        while self.tabla[idx] is not None: 
            if self.tabla[idx] != self.ELIMINADO and self.tabla[idx][0] == clave: 
                return self.tabla[idx][1]  # Clave encontrada 
            idx = (idx + 1) % self.tamanio # Continúa sondeo 
            pasos += 1 
            if pasos >= self.tamanio: 
                break 
        return None 

    def factor_de_carga(self) -> float: 
        return self.elementos / self.tamanio 

# ─────────────────────────────────────────────────────────────── 
# 5. FUNCIÓN PRINCIPAL DE BENCHMARK 
# ─────────────────────────────────────────────────────────────── 
def benchmark_completo(datos: list, tamanios=[1009, 2003, 4001, 8009]): 
    resultados = []  # Lista para almacenar métricas 

    for m in tamanios: 
        subdatos = datos[:min(len(datos), int(m * 0.65))]  # 65% de llenado 

        # --- Encadenamiento --- 
        th_enc = TablaHashEncadenamiento(m) 
        t0 = time.perf_counter()                # Inicio medición 
        for k, v in subdatos: th_enc.insertar(k, v)  # Inserciones 
        t_ins_enc = (time.perf_counter() - t0) * 1000  # ms 

        t0 = time.perf_counter() 
        for k, v in subdatos[:100]: th_enc.buscar(k)  # Búsquedas 
        t_bus_enc = (time.perf_counter() - t0) * 1000 

        # --- Sondeo Lineal --- 
        th_sl = TablaHashSondeoLineal(m) 
        t0 = time.perf_counter() 
        for k, v in subdatos: 
            try: th_sl.insertar(k, v) 
            except OverflowError: break 
        t_ins_sl = (time.perf_counter() - t0) * 1000 

        t0 = time.perf_counter() 
        for k, v in subdatos[:100]: th_sl.buscar(k) 
        t_bus_sl = (time.perf_counter() - t0) * 1000 

        # --- Diccionario nativo Python --- 
        dict_py = {} 
        t0 = time.perf_counter() 
        for k, v in subdatos: dict_py[k] = v 
        t_ins_py = (time.perf_counter() - t0) * 1000 

        t0 = time.perf_counter() 
        for k, v in subdatos[:100]: _ = dict_py.get(k) 
        t_bus_py = (time.perf_counter() - t0) * 1000 

        resultados.append({ 
            'tamanio': m, 
            'n': len(subdatos), 
            'lambda_enc': round(th_enc.factor_de_carga(), 3), 
            'col_enc': th_enc.colisiones, 
            'ins_enc_ms': round(t_ins_enc, 3), 
            'bus_enc_ms': round(t_bus_enc, 4), 
            'col_sl': th_sl.colisiones, 
            'ins_sl_ms': round(t_ins_sl, 3), 
            'bus_sl_ms': round(t_bus_sl, 4), 
            'ins_py_ms': round(t_ins_py, 3), 
            'bus_py_ms': round(t_bus_py, 4), 
        }) 
        print(f'm={m}: λ={resultados[-1]["lambda_enc"]} | col_enc={th_enc.colisiones} | col_sl={th_sl.colisiones}') 

    return resultados 

# ─────────────────────────────────────────────────────────────── 
# 6. TABLA COMPARATIVA Y GRÁFICOS 
# ─────────────────────────────────────────────────────────────── 
def mostrar_tabla(resultados): 
    """Imprime tabla comparativa de resultados en consola.""" 
    print('\n' + '='*100) 
    print(f'{"m":>6} {"n":>6} {"λ":>6} {"Col_Enc":>8} {"Col_SL":>8} {"T_ins_Enc":>10} {"T_ins_SL":>10} {"T_Py":>8}') 
    print('='*100) 
    for r in resultados: 
        print(f'{r["tamanio"]:>6} {r["n"]:>6} {r["lambda_enc"]:>6} {r["col_enc"]:>8} {r["col_sl"]:>8} '
              f'{r["ins_enc_ms"]:>10} {r["ins_sl_ms"]:>10} {r["ins_py_ms"]:>8}')

def graficar_resultados(resultados): 
    """Genera gráficos de colisiones y tiempos de inserción.""" 
    tamanios = [r['tamanio'] for r in resultados] 
    col_enc  = [r['col_enc'] for r in resultados] 
    col_sl   = [r['col_sl']  for r in resultados] 
    ins_enc  = [r['ins_enc_ms'] for r in resultados] 
    ins_sl   = [r['ins_sl_ms']  for r in resultados] 
    ins_py   = [r['ins_py_ms']  for r in resultados] 

    fig, axs = plt.subplots(1, 2, figsize=(12, 5)) 

    # Gráfico 1: Colisiones vs. tamaño de tabla 
    axs[0].plot(tamanios, col_enc, 'b-o', label='Encadenamiento') 
    axs[0].plot(tamanios, col_sl,  'r-s', label='Sondeo Lineal') 
    axs[0].set_title('Colisiones vs. Tamaño de Tabla') 
    axs[0].set_xlabel('Tamaño de tabla (m)') 
    axs[0].set_ylabel('Número de colisiones') 
    axs[0].legend() 
    axs[0].grid(True, alpha=0.3) 

    # Gráfico 2: Tiempo de inserción (ms) 
    axs[1].plot(tamanios, ins_enc, 'b-o', label='Encadenamiento') 
    axs[1].plot(tamanios, ins_sl,  'r-s', label='Sondeo Lineal') 
    axs[1].plot(tamanios, ins_py,  'g-^', label='dict Python') 
    axs[1].set_title('Tiempo de Inserción (ms)') 
    axs[1].set_xlabel('Tamaño de tabla (m)') 
    axs[1].set_ylabel('Tiempo (ms)') 
    axs[1].legend() 
    axs[1].grid(True, alpha=0.3) 

    plt.tight_layout() 
    plt.savefig('hash_benchmark.png', dpi=150) 
    plt.show() 
    print('Gráfico guardado: hash_benchmark.png') 

# ─────────────────────────────────────────────────────────────── 
# 7. EJECUCIÓN PRINCIPAL 
# ─────────────────────────────────────────────────────────────── 
if __name__ == '__main__': 
    # OPCIÓN A: Datos reales de tu CSV local
    print("Cargando dataset local...")
    datos = cargar_datos('AI_Impact_Student_Life_2026.csv', 'Student_ID', 'Main_Usage_Case') 

    if datos:
        print(f'Procesando {len(datos)} registros de Student_ID / Main_Usage_Case...')
        resultados = benchmark_completo(datos)  # Ejecuta benchmark 
        mostrar_tabla(resultados)               # Muestra tabla 
        graficar_resultados(resultados)         # Genera gráficos

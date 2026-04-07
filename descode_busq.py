# Importa librerías necesarias para el programa
import random     # Para generar números aleatorios y barajar listas
import time       # Para medir tiempo de ejecución de las funciones
import bisect     # Módulo especializado en búsqueda binaria (muy eficiente)
import statistics as stats  # Para calcular promedios estadísticos (stats.mean)

# Función de búsqueda lineal: revisa elemento por elemento, O(n)
def linear_search(a, x):
    # enumerate(a) genera pares (índice, valor) para cada elemento del arreglo
    for i, v in enumerate(a):
        # Si el valor actual (v) coincide con el buscado (x), devuelve su índice
        if v == x:
            return i
    # Si recorre todo sin encontrar, devuelve -1
    return -1

# Función de búsqueda binaria usando el módulo bisect (muy eficiente, O(log n))
def binary_search(a, x):
    # bisect.bisect_left busca la posición de inserción para x en arreglo ordenado
    # Devuelve el índice más a la izquierda donde podría ir x
    i = bisect.bisect_left(a, x)
    # Verifica si en esa posición efectivamente está x, sino devuelve -1
    return i if i < len(a) and a[i] == x else -1

# Búsqueda exponencial: útil cuando no se conoce el tamaño o está mal distribuido
def exponential_search(a, x):
    # Si el arreglo está vacío, no hay nada que buscar
    if not a:
        return -1
    # Si el primer elemento es el buscado, devuelve 0
    if a[0] == x:
        return 0

    i = 1  # Empieza duplicando desde posición 1
    n = len(a)  # Guarda la longitud del arreglo

    # Duplica i (i <<= 1 es i = i * 2) mientras esté dentro del arreglo
    # y el valor en esa posición sea menor que x
    while i < n and a[i] < x:
        i <<= 1  # Operador bit a bit: i = i * 2

    # Define el rango de búsqueda: desde la mitad de la última i hasta i
    lo, hi = i >> 1, min(i, n - 1)  # i >> 1 es i // 2

    # Aplica búsqueda binaria normal dentro de ese rango
    while lo <= hi:
        m = (lo + hi) // 2  # Punto medio del rango
        if a[m] == x:
            return m
        if a[m] < x:
            lo = m + 1  # Busca en la mitad derecha
        else:
            hi = m - 1  # Busca en la mitad izquierda

    return -1

# Búsqueda por interpolación: estima la posición según el valor (mejor para datos uniformes)
def interpolation_search(a, x):
    lo, hi = 0, len(a) - 1  # Límites iniciales del arreglo

    # Mientras x esté dentro del rango de valores posibles...
    while lo <= hi and a[lo] <= x <= a[hi]:
        # Si todos los valores del rango son iguales...
        if a[lo] == a[hi]:
            # Solo puede ser x si coincide con ese valor
            return lo if a[lo] == x else -1

        # FÓRMULA DE INTERPOLACIÓN: estima dónde debería estar x
        # pos = lo + (x - a[lo]) * (hi - lo) / (a[hi] - a[lo])
        pos = lo + int((x - a[lo]) * (hi - lo) / (a[hi] - a[lo]))

        # Si la posición calculada sale del rango, se detiene
        if pos < lo or pos > hi:
            break

        # Si encuentra x exactamente, devuelve su posición
        if a[pos] == x:
            return pos
        elif a[pos] < x:
            lo = pos + 1  # Busca a la derecha
        else:
            hi = pos - 1  # Busca a la izquierda

    return -1

# Función para medir el rendimiento (benchmarking) de cualquier buscador
def bench(a, queries, fn, reps=1):
    # Lista para guardar los tiempos de cada repetición
    t = []

    # Repite el experimento 'reps' veces para mayor precisión
    for _ in range(reps):
        # time.perf_counter(): reloj de alta precisión (mejor que time.time())
        t0 = time.perf_counter()
        
        # Variable acumuladora para evitar que Python optimice el ciclo
        s = 0

        # Ejecuta la función de búsqueda para cada consulta
        for x in queries:
            s += fn(a, x)  # fn es la función que se mide (linear_search, etc.)

        t1 = time.perf_counter()
        
        # Calcula el tiempo total y lo convierte a milisegundos
        # (t1 - t0) / len(queries) * 1000.0 = ms por búsqueda
        t.append((t1 - t0) / len(queries) * 1000.0)

    # Devuelve el promedio de todos los tiempos medidos
    return stats.mean(t)

# Genera diferentes tipos de datos de prueba
def make_data(n, kind):
    # "uniform_sorted": números ordenados del 0 al n-1
    if kind == "uniform_sorted":
        a = list(range(n))

    # "biased_sorted": 80% valores pequeños, 20% valores grandes (distribución sesgada)
    elif kind == "biased_sorted":
        a = []
        for _ in range(n):
            # 80% probabilidad: valores cercanos al inicio (0 a 10% de n)
            if random.random() < 0.8:
                a.append(random.randint(0, int(0.1 * n)))
            # 20% probabilidad: valores dispersos y grandes
            else:
                a.append(random.randint(int(0.1 * n), 5 * n))
        a.sort()  # Ordena el arreglo para búsquedas binarias

    # "shuffled": números ordenados pero revueltos
    elif kind == "shuffled":
        a = list(range(n))
        random.shuffle(a)  # Baraja completamente el arreglo

    return a

# Genera consultas de búsqueda (queries)
def make_queries(a, hits=700, misses=300):
    q = []

    # 'hits': valores que SÍ existen en el arreglo (70% de las consultas)
    for _ in range(hits):
        # random.choice(a) elige un elemento al azar del arreglo
        q.append(random.choice(a))

    # 'misses': valores que PROBABLEMENTE NO existen (30% de las consultas)
    for i in range(misses):
        # Valores muy grandes que no están en el arreglo
        q.append(len(a) * 10 + i)

    # Mezcla las consultas para que no estén ordenadas
    random.shuffle(q)
    return q

# ------------------------- SECCIÓN PRINCIPAL ----------------------

# Fija la semilla del generador aleatorio para resultados reproducibles
random.seed(123)

# Tamaños de prueba: 10k, 100k, 500k elementos
sizes = [10_000, 100_000, 500_000]

# Recorre cada tamaño de prueba
for n in sizes:
    # Prueba tres tipos de datos para cada tamaño
    for kind in ["uniform_sorted", "biased_sorted", "shuffled"]:
        # Genera el arreglo de datos
        a = make_data(n, kind)
        
        # Genera las consultas de búsqueda
        q = make_queries(a)

        # Imprime información del experimento actual
        print(f"n={n}, dataset={kind}")
        
        # Mide búsqueda lineal (siempre funciona, no necesita orden)
        print(" lineal :", bench(a, q, linear_search))

        # Si el dataset está ordenado, mide las búsquedas avanzadas
        if kind != "shuffled":
            print(" binaria :", bench(a, q, binary_search))
            print(" exponencial :", bench(a, q, exponential_search))
            print(" interpolacion :", bench(a, q, interpolation_search))
        else:
            # Si está desordenado, avisa que no se pueden usar búsquedas avanzadas
            print(" (no ordenado: ordenar o usar lineal)")

        # Separador visual entre experimentos
        print("-" * 32)

import random
import time

# Búsqueda lineal: recorre todo el arreglo elemento por elemento
# Complejidad: O(n)
def busqueda_lineal(a, x):
    for i, v in enumerate(a):   # recorrer con índice y valor
        if v == x:              # si encuentra el valor
            return i            # devuelve posición
    return -1                   # no encontrado


# Búsqueda binaria: divide el espacio de búsqueda en mitades
# Requiere que el arreglo esté ordenado
# Complejidad: O(log n)
def busqueda_binaria(a, x):
    l, r = 0, len(a) - 1        # límites del intervalo de búsqueda

    while l <= r:
        m = (l + r) // 2        # punto medio

        if a[m] == x:
            return m
        elif a[m] < x:
            l = m + 1           # buscar en la mitad derecha
        else:
            r = m - 1           # buscar en la mitad izquierda

    return -1                   # no encontrado


# Búsqueda exponencial: encuentra un rango donde puede estar x
# y luego aplica búsqueda binaria
# Complejidad: O(log k), donde k es la posición del elemento
def busqueda_exponencial(a, x):
    if not a:
        return -1               # arreglo vacío

    if a[0] == x:
        return 0                # optimización: revisar primer elemento

    i = 1
    # duplicar el rango: 1,2,4,8,...
    while i < len(a) and a[i] < x:
        i *= 2

    # definir rango donde puede estar x
    l = i // 2
    r = min(i, len(a) - 1)

    # búsqueda binaria en ese rango
    while l <= r:
        m = (l + r) // 2
        if a[m] == x:
            return m
        elif a[m] < x:
            l = m + 1
        else:
            r = m - 1

    return -1


# Búsqueda por interpolación: estima la posición del elemento
# Funciona mejor si los datos están uniformemente distribuidos
def busqueda_interpolacion(a, x):
    low, high = 0, len(a) - 1

    # condición: x debe estar dentro del rango de valores
    while low <= high and x >= a[low] and x <= a[high]:

        # evitar división por cero si todos los valores son iguales
        if a[low] == a[high]:
            return low if a[low] == x else -1

        # fórmula de interpolación (estimación de posición)
        pos = low + int((high - low) * (x - a[low]) / (a[high] - a[low]))

        # si la estimación se sale del rango, se aborta
        if pos < low or pos > high:
            break

        if a[pos] == x:
            return pos
        elif a[pos] < x:
            low = pos + 1
        else:
            high = pos - 1

    return -1


# ----------------------
# Medición de tiempo
# ----------------------

# Calcula el tiempo promedio por búsqueda
def medir(a, queries, buscador):
    t0 = time.perf_counter()    # inicio

    checksum = 0                # evita optimizaciones del intérprete
    for x in queries:
        checksum += buscador(a, x)

    t1 = time.perf_counter()    # fin

    # tiempo promedio por búsqueda en milisegundos
    return (t1 - t0) * 1000 / len(queries)


# ----------------------
# MAIN
# ----------------------

def main():
    # Tamaños solicitados (muy pequeños → limitación experimental)
    ns = [104, 105, 5105]

    random.seed(123)  # reproducibilidad

    for n in ns:

        # Dataset uniforme: valores consecutivos
        uni = list(range(n))

        # Dataset sesgado: concentración en valores pequeños
        ses = []
        for _ in range(n):
            if random.random() < 0.8:
                ses.append(random.randint(0, int(0.1 * n)))
            else:
                ses.append(random.randint(int(0.1 * n), 5 * n))
        ses.sort()  # necesario para algoritmos que requieren orden

        # Dataset desordenado
        des = uni.copy()
        random.shuffle(des)

        # Generación de consultas (queries)
        def mkqueries(base):
            q = []

            # 70% valores existentes
            for _ in range(700):
                q.append(base[random.randint(0, len(base) - 1)])

            # 30% valores inexistentes
            for i in range(300):
                q.append(10 * len(base) + i)

            random.shuffle(q)
            return q

        q_uni = mkqueries(uni)
        q_ses = mkqueries(ses)
        q_des = mkqueries(des)

        # Función de reporte
        def report(nombre, arr, q, ordenado):
            print(f"n = {n}, dataset = {nombre}")

            # siempre aplicable
            print(f"  busqueda lineal      : {medir(arr, q, busqueda_lineal):.6f} ms/busq")

            if ordenado:
                print(f"  busqueda binaria     : {medir(arr, q, busqueda_binaria):.6f} ms/busq")
                print(f"  busqueda exponencial : {medir(arr, q, busqueda_exponencial):.6f} ms/busq")
                print(f"  interpolacion        : {medir(arr, q, busqueda_interpolacion):.6f} ms/busq")
            else:
                # explicación conceptual importante
                print("  NOTA: El dataset no esta ordenado.")
                print("  -> Los algoritmos binario, exponencial e interpolacion requieren orden total.")
                print("  -> Sin orden, sus decisiones (dividir o estimar posiciones) no son validas.")
                print("  -> Esto no solo afecta rendimiento, sino la CORRECTITUD del resultado.")
                print("  -> Por ello, solo la busqueda lineal es aplicable.")

        # Reportes
        report("uniforme_ordenado", uni, q_uni, True)
        report("sesgado_ordenado", ses, q_ses, True)
        report("desordenado", des, q_des, False)

        # separador visual
        print("---------------------------------------------")


if __name__ == "__main__":
    main()

import time      # Módulo para usar time.perf_counter() y medir el rendimiento con alta precisión en segundos.
import random    # Módulo para generar datos aleatorios y poblar nuestra estructura de datos inicial.
import sys       # Módulo para interactuar con el sistema, necesario para modificar límites internos del intérprete.
import csv       # Módulo para escribir los datos resultantes en un formato tabular persistente (archivo CSV).

# Aumentamos el límite de profundidad de recursión del intérprete de Python.
# Quick Sort en su peor caso (lista ya ordenada) alcanza una profundidad de recursión de N (1000).
# El límite por defecto de Python suele ser 1000, por lo que lo subimos a 2500 para evitar errores de tipo 'RecursionError'.
sys.setrecursionlimit(2500)

# ====================================================================================================
# 1. BUBBLE SORT (Ordenamiento de Burbuja)
# ====================================================================================================
# En Python, 'arr' es una referencia a una 'List', que es un arreglo dinámico internamente.
# Al ser mutable, las modificaciones hechas a 'arr' aquí se reflejan en el objeto original en memoria.
def bubble_sort(arr):
    comps = 0 # Inicializamos el contador de comparaciones (entero inmutable).
    swaps = 0 # Inicializamos el contador de intercambios (entero inmutable).
    n = len(arr) # len() accede al atributo de tamaño de la lista en O(1) ya que el arreglo dinámico mantiene su longitud interna.
    
    # Bucle externo: itera N-1 veces. Representa las pasadas sobre la estructura de datos.
    for i in range(n - 1):
        # Bucle interno: los últimos 'i' elementos ya están en su posición final, así que reducimos el rango de iteración.
        for j in range(n - i - 1):
            comps += 1 # Aumentamos en 1 el registro de comparaciones.
            # Accedemos a los elementos de la lista en memoria mediante sus índices j y j+1 (acceso aleatorio O(1)).
            if arr[j] > arr[j + 1]:
                swaps += 1 # Registramos que ocurrirá un intercambio/movimiento estructural.
                # A diferencia de C++, Python permite el intercambio (swap) rápido y directo utilizando empaquetado/desempaquetado de Tuplas.
                # Crea una tupla temporal inmutable (arr[j+1], arr[j]) en memoria y luego reasigna los punteros internos de la lista.
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                
    # Retornamos los contadores en forma de tupla (comps, swaps).
    return comps, swaps

# ====================================================================================================
# 2. INSERTION SORT (Ordenamiento por Inserción)
# ====================================================================================================
# 'arr' hace referencia directa a la estructura dinámica de lista en memoria.
def insertion_sort(arr):
    comps = 0 # Contador de operaciones lógicas de comparación.
    swaps = 0 # Contador de movimientos o desplazamientos de referencias dentro de la lista dinámica.
    n = len(arr) # O(1) tiempo de acceso para obtener la cantidad actual de elementos en la estructura.
    
    # Iteramos desde el segundo elemento (índice 1) asumiendo lógicamente que el primero (índice 0) ya es una "sub-lista ordenada".
    for i in range(1, n):
        # Guardamos el valor actual a posicionar en la variable temporal 'key'. 
        # En Python, key guarda una referencia al objeto en memoria, no el valor crudo en sí.
        key = arr[i] 
        # 'j' es el índice del elemento anterior, desde el cual empezaremos a comparar retrocediendo en la estructura de la lista.
        j = i - 1
        
        # Bucle while: iteramos hacia atrás a través de los índices de la lista mientras no salgamos de sus límites de memoria (j >= 0).
        while j >= 0:
            comps += 1 # Contamos la comparación que va a ser ejecutada justo en la siguiente línea.
            # Si el elemento almacenado en la estructura de datos en esa posición es mayor a nuestro 'key'...
            if arr[j] > key:
                swaps += 1 # Contamos este desplazamiento posicional como un movimiento dentro de la lista dinámica.
                # Copiamos la referencia de memoria un índice a la derecha, desplazándolo físicamente dentro del bloque continuo de la lista.
                arr[j + 1] = arr[j] 
                # Disminuimos j en 1 para continuar inspeccionando posiciones anteriores en la memoria del arreglo.
                j -= 1
            else:
                # Si encontramos un elemento de valor menor o igual, detenemos la búsqueda (salimos del while).
                break 
                
        # Una vez hallada la ranura correcta, insertamos allí la referencia al objeto 'key' conservado.
        arr[j + 1] = key 
        
    return comps, swaps

# ====================================================================================================
# 3. MERGE SORT (Ordenamiento por Mezcla)
# ====================================================================================================
# Algoritmo tipo Divide y Vencerás que utiliza grandes cantidades de memoria externa auxiliar temporal, pero asegura rendimiento O(N log N).
def merge_sort(arr):
    # En Python, las variables numéricas (enteros) son inmutables. Si queremos que las funciones internas y locales
    # puedan modificar de forma compartida estos contadores, los metemos en una Lista dinámica (estructura mutable).
    comps = [0]
    swaps = [0]
    
    # Función de cierre o anidada, encargada de la porción 'Conquer': Mezclar dos mitades ya ordenadas lógicamente.
    def merge(left, mid, right):
        # Slicing de listas: La sintaxis [inicio:fin] de Python provoca que se instancie OTRA NUEVA estructura dinámica.
        # Por tanto, L y R son copias físicas, alojando un bloque nuevo en la RAM del sistema.
        L = arr[left:mid + 1]
        R = arr[mid + 1:right + 1]
        
        i = j = 0 # Variables locales que nos ayudarán a iterar progresivamente sobre las sub-estructuras L y R temporalmente copiadas.
        k = left  # 'k' mantiene el rastro del índice físico que debemos sobrescribir en la estructura de lista originaria 'arr'.
        
        # Mientras no hayamos agotado los elementos presentes en los bloques de memoria asignados a L o a R.
        while i < len(L) and j < len(R):
            comps[0] += 1 # Mutamos el contador interno contenido en nuestra lista global mutable.
            
            # Realizamos una validación comparando las referencias presentes en las estructuras temporales.
            if L[i] <= R[j]:
                # Tomamos el dato del bloque L y sobrescribimos con esa referencia la memoria contigua de la lista principal 'arr'.
                arr[k] = L[i]
                i += 1 # Avanzamos nuestro puntero lógico en la sub-estructura izquierda.
            else:
                # En caso contrario, tomamos la referencia contenida en R para la memoria principal.
                arr[k] = R[j]
                j += 1 # Avanzamos nuestro puntero lógico en la sub-estructura derecha.
                
            swaps[0] += 1 # Toda escritura que altera la memoria de 'arr' se considera un movimiento funcional.
            k += 1 # Avanzamos el puntero iterador que rige la estructura de datos real.
            
        # Cuando agotamos la sub-lista R, pero a la sub-lista L le restan datos pendientes...
        # Copiamos cíclicamente esas referencias residuales ordenadas hacia nuestro bloque principal de 'arr'.
        while i < len(L):
            arr[k] = L[i]
            swaps[0] += 1
            i += 1
            k += 1
            
        # La contraparte; si fue L la sub-estructura agotada temprano, pasamos secuencialmente los sobrantes ordenados de R hacia 'arr'.
        while j < len(R):
            arr[k] = R[j]
            swaps[0] += 1
            j += 1
            k += 1
            
    # Función recursiva que realiza la fase lógica 'Divide', calculando el corte estructural y profundizando en el Stack de recursión.
    def _merge_sort(left, right):
        # Condición de retorno o base: Si nuestro índice de memoria izquierdo iguala o rebasa al derecho, tenemos
        # una subestructura aislada e indivisible de magnitud 0 o 1 (que por defecto lógico siempre es un conjunto "ordenado").
        if left >= right:
            return
        
        # Matemáticamente descubrimos la partición central restando y promediando las barreras limítrofes pasadas por argumento.
        # Es fundamental el uso de // (floor division o división entera de Python) para preservar el tipo entero indispensable para acceder a índices de listas.
        mid = left + (right - left) // 2
        
        # Recursivamente creamos nuevos marcos en el Stack pidiendo segmentar y analizar cada ramificación por separado.
        _merge_sort(left, mid)
        _merge_sort(mid + 1, right)
        
        # Finalmente, ya fraccionadas hasta la base, damos la orden a la estructura fusionadora de unirlas respetando un patrón de magnitud ascendente.
        merge(left, mid, right)
        
    # Inicializamos la ejecución recursiva pasándole explícitamente los alcances completos de indexación permisible según el espacio total en nuestro array.
    _merge_sort(0, len(arr) - 1)
    
    # Extracción y retorno funcional de los números crudos integrados dentro de su cápsula mutable respectiva.
    return comps[0], swaps[0]

# ====================================================================================================
# 4. QUICK SORT (Ordenamiento Rápido)
# ====================================================================================================
# Un algoritmo basado también en Divide y Vencerás, pero que opera y muta las referencias íntegramente 'in-place'.
# Esto quiere decir que trabaja sobre la estructura de lista sin instanciar bloques de tamaño masivo en la RAM.
def quick_sort(arr):
    # Protegemos nuestros contadores de las limitaciones de scope locales con estructuras anidables y mutables.
    comps = [0]
    swaps = [0]
    
    # Lógica central del Quick Sort que selecciona lógicamente un separador paramétrico de los objetos en memoria.
    def partition(low, high):
        # Categóricamente elegimos a la última posición indexable (el límite high) como nuestro número de corte o pivote.
        pivot = arr[high]
        
        # El iterador 'i' es nuestra frontera virtual; irá determinando en la memoria y arrinconando dónde finalizan aquellos valores menores al límite.
        i = low - 1
        
        # Ciclo lógico generado con el iterador dinámico 'range', evaluando todos los registros hasta detenerse exactamente antes de pisar el objeto Pivote.
        for j in range(low, high):
            comps[0] += 1 # Incrementar la estadística de comparaciones algorítmicas de memoria.
            
            # Verificación del contenido de memoria alojado en el vector posicional 'j'.
            if arr[j] <= pivot:
                i += 1 # Ensanchamos el espacio demarcado para datos en la sublista virtual izquierda (los más pequeños).
                swaps[0] += 1 # Suma referencial estadística de movimiento.
                
                # Explotando la mecánica funcional de empaquetado/desempaquetado (tuplas) del intérprete de Python,
                # se conmutan recíprocamente los apuntadores de 'arr[i]' y 'arr[j]' en la memoria continua subyacente a la Lista.
                arr[i], arr[j] = arr[j], arr[i]
                
        swaps[0] += 1 # Una vez validado y posicionado todo dato menor hacia la sub-región izquierda, hay que desplazar estadísticamente el pivote final.
        
        # Reposicionamos al Pivote, de su extremo temporal foráneo, e intercambiándolo para incrustarlo entre medio del sub-sector menor y el bloque mayor restante.
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        
        # Entregamos como un output la coordenada definitiva con indexación ya absoluta sobre el elemento de corte (Pivote).
        return i + 1
        
    # Método recursivo iterativo. Recibe límites espaciales indicando en qué porción indexable debe encauzar la reorganización estructural in-place.
    def _quick_sort(low, high):
        # Valida semánticamente si poseemos una carga volumétrica suficiente (al menos de grado bidimensional de 2 o más índices) como para reorganizar cosas.
        if low < high:
            # Reubica in-place a la carga del Pivote obteniendo como índice resultante su posicionamiento final intocable en memoria.
            pi = partition(low, high)
            
            # Manda a llamar repetitiva y anidadamente sobre todos los sectores del árbol recursivo segregando la zona inferior de indexaciones, a la izquierda del Pivote ordenado.
            _quick_sort(low, pi - 1)
            # Idéntica ramificación y recursividad anidada por debajo enfocada ahora en el rango del cuadrante por encima, a su estricta derecha.
            _quick_sort(pi + 1, high)
            
    # Lanzamiento global para organizar in-place desde los bordes completos de nuestra única estructura de lista.
    _quick_sort(0, len(arr) - 1)
    
    # Recuperación des-anidada del estado volumétrico numérico interno final de los arreglos contadores y retorno al scope primario.
    return comps[0], swaps[0]

# ====================================================================================================
# FUNCIÓN PRINCIPAL (MAIN)
# ====================================================================================================
def main():
    # Especificación unívoca e inmutable sobre el alcance de las muestras dimensionales en los arreglos lógicos.
    SIZE = 1000
    
    # 1. Generar arreglo aleatorio.
    # List comprehension de Python. Una abstracción sintáctica ejecutada a altísima velocidad internamente por la capa C.
    # Evita el lento sobrecosto del `append` dinámico iterado pidiendo inicialmente un bloque contiguo para todo el objeto unificado a la memoria de RAM.
    original_random = [random.randint(1, 10000) for _ in range(SIZE)]
    
    # `sorted()` no ordena la lista `in-place` (como un hipotético list.sort() local), sino que asigna y reserva íntegramente
    # una NUEVA lista dinámica autónoma para no tocar ni interferir la lista primaria enviada.
    # Internamente emplea Timsort, un híbrido estructural ultra-eficiente derivado de la mezcla simbiótica entre Insertion Sort con el Merge Sort.
    original_sorted = sorted(original_random)
    
    # Función reversed() no gasta un bloque entero RAM; sólo monta un patrón lógico tipo Iterador que se recorre virtualmente en reverso referencial.
    # Por consiguiente al forzarlo envolviéndolo explícitamente en el casting constructor list(), forzamos contundentemente a la RAM del Sistema
    # a procesar esa vista iterada virtual para que construya y cimente una lista dinámica real completa ocupando megabytes sólidos.
    original_reverse = list(reversed(original_sorted))
    
    # Arreglo de nomenclaturas a modo de string identificativo usado simplemente como alias descriptivo en salida de la terminal standard.
    names = ["Aleatorio", "Ordenado", "Inverso"]
    
    # Aquí estamos anidando listas. La matriz "sources" contiene apuntadores por referencia que dirigen transparentemente al intérprete global 
    # de memoria hacia los tres bloques estructurados reales inicializados más arriba.
    sources = [original_random, original_sorted, original_reverse]
    
    # Sintaxis segura 'with open' de Python; genera e implementa Context Managers. Mantiene un bloqueo en el puntero real descriptor de disco (File IO).
    # Protege frente a Memory Leaks y Crash-logs, dado que garantiza imperativamente que liberará su Handler físico en cuanto la indentación termine.
    with open("resultados_sort_python.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file) # Parseador que convierte un iterador o lista secuencial de parámetros Python nativos, uniéndolos separados bajo tabulación de comas.
        
        # Inserta como primera iteración al buffer binario el esqueleto inamovible (Metadata) para categorizar las casillas o celdas serializadas.
        writer.writerow(["Escenario", "Algoritmo", "Tiempo_us", "Comparaciones", "Intercambios"])
        
        # Al pasar por enumerate, nos inyecta simultánea, dinámica y paralela iteración doble: 
        # La posición del índice numeral indexado absoluto (i) a la par del objeto en dicha estática posición ('caso' es un String de la matriz lists names).
        for i, caso in enumerate(names):
            print(f"\n===========================================================")
            print(f"Evaluando estructura (Lista dinámica): {caso} ({SIZE} elementos)")
            print(f"===========================================================")
            
            # ---- Medir Bubble Sort ----
            # Operación VITAL: El casting 'list(sources[i])' fuerza un Shadow-Clone integral por valor lógico, emulando físicamente 
            # las referencias, y garantizando así la mutabilidad destructiva 'in-place' a los siguientes ordenadores sin comprometer ni corromper a nuestra lista matriz.
            arr = list(sources[i]) 
            
            # Acude a la función más veloz soportada de tu placa base o CPU a un nivel nano-micro de timing hardware real en vez de usar la abstracción lógica desajustada de system-clock.
            start = time.perf_counter() 
            
            # Traslación de bloque algorítmico asincrónico por subrutina modularizada procesando nuestra estructura temporal 'arr' list clone.
            comps, swaps = bubble_sort(arr)
            
            end = time.perf_counter()
            # La sustracción devuelve segundos expresados de manera flotante decimal pura; multiplicamos agresivamente por 1M escalándolos y casteando forzosamente a Int base truncando rastro flotante no relevante.
            t_us = int((end - start) * 1_000_000) 
            print(f"Bubble Sort:\tTiempo: {t_us} us \t| Comps: {comps} \t| Movs/Intercambios: {swaps}")
            
            # Persistencia volcada empujando y concatenando en crudo y de golpe esta lista encapsulada iterada al Stream físico buffer del handler de disco rígido interno CSV.
            writer.writerow([caso, "Bubble Sort", t_us, comps, swaps])
            
            # ---- Medir Insertion Sort ----
            arr = list(sources[i]) # Destruimos (Garbage Collector desecha el anterior) y reasignamos bloque nuevo desde la fuente intocada.
            start = time.perf_counter()
            comps, swaps = insertion_sort(arr)
            end = time.perf_counter()
            t_us = int((end - start) * 1_000_000)
            print(f"Insertion Sort:\tTiempo: {t_us} us \t| Comps: {comps} \t| Movs/Intercambios: {swaps}")
            writer.writerow([caso, "Insertion Sort", t_us, comps, swaps])
            
            # ---- Medir Merge Sort ----
            arr = list(sources[i]) # Instanciamos un nuevo list clone RAM asignado desde un bloque heap seguro.
            start = time.perf_counter()
            comps, swaps = merge_sort(arr)
            end = time.perf_counter()
            t_us = int((end - start) * 1_000_000)
            print(f"Merge Sort:\tTiempo: {t_us} us \t| Comps: {comps} \t| Movs/Intercambios: {swaps}")
            writer.writerow([caso, "Merge Sort", t_us, comps, swaps])
            
            # ---- Medir Quick Sort ----
            arr = list(sources[i]) # Asignamos la última iteración destructiva local clonada list()
            start = time.perf_counter()
            comps, swaps = quick_sort(arr)
            end = time.perf_counter()
            t_us = int((end - start) * 1_000_000)
            print(f"Quick Sort:\tTiempo: {t_us} us \t| Comps: {comps} \t| Movs/Intercambios: {swaps}")
            writer.writerow([caso, "Quick Sort", t_us, comps, swaps])
            
    # El Descriptor Handler bloqueador tipo Context Manager (with..open) finaliza su indentación en esta línea desocupando y devolviendo la disponibilidad de File Stream binario a las capas del OS.
    print("\nResultados persistidos exitosamente en el archivo 'resultados_sort_python.csv'.")

# Cláusula de seguridad que instruye y acopla un comportamiento del Intérprete bloqueando scripts globales inestables: 
# Evalúa si la invocación compilada base fue ejecutada frontal o directamente invocada, permitiendo instanciar Main, o la frena previendo un Import externo ajeno.
if __name__ == "__main__":
    main()

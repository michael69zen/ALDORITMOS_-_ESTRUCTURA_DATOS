import heapq  # Importa una herramienta para manejar colas de prioridad (montículos)

def dijkstra(grafo, inicio):
    # Crea un diccionario donde cada nodo tiene distancia infinita al inicio
    distancias = {nodo: float('inf') for nodo in grafo}
    
    # La distancia del nodo inicial a sí mismo es 0
    distancias[inicio] = 0
    
    # Cola de prioridad donde guardamos (distancia, nodo)
    # Empieza con el nodo inicial
    cola = [(0, inicio)]
    
    # Conjunto para guardar los nodos que ya fueron visitados
    visitados = set()
    
    # Mientras haya elementos en la cola
    while cola:
        # Extrae el nodo con la menor distancia
        distancia_actual, nodo = heapq.heappop(cola)
        
        # Si ya visitamos este nodo, lo ignoramos
        if nodo in visitados:
            continue
        
        # Marcamos el nodo como visitado
        visitados.add(nodo)
        
        # Recorremos todos los vecinos del nodo actual
        for vecino, peso in grafo[nodo].items():
            
            # Calculamos la distancia pasando por el nodo actual
            nueva_distancia = distancia_actual + peso
            
            # Si encontramos un camino más corto hacia el vecino
            if nueva_distancia < distancias[vecino]:
                
                # Actualizamos la distancia más corta
                distancias[vecino] = nueva_distancia
                
                # Agregamos el vecino a la cola con su nueva distancia
                heapq.heappush(cola, (nueva_distancia, vecino))
    
    # Retornamos el diccionario con las distancias mínimas
    return distancias


# Definimos el grafo como un diccionario de diccionarios
# Cada nodo tiene vecinos con sus respectivos pesos (costos)
grafo = {
    'A': {'B': 4, 'C': 2},      # Desde A se puede ir a B (4) y C (2)
    'B': {'A': 4, 'C': 1, 'D': 5},  # Desde B a A, C y D
    'C': {'A': 2, 'B': 1, 'D': 8, 'E': 10},  # Desde C a varios nodos
    'D': {'B': 5, 'C': 8, 'E': 2},  # Desde D a B, C y E
    'E': {'C': 10, 'D': 2},     # Desde E a C y D
}

# Nodo desde donde comenzamos
inicio = 'A'

# Ejecutamos el algoritmo
resultado = dijkstra(grafo, inicio)

# Imprimimos las distancias desde el nodo inicial a cada nodo
for nodo, dist in resultado.items():
    print(f"Distancia desde {inicio} hasta {nodo}: {dist}")

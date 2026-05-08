from collections import deque

def recorrer_cola(cola):
    if not cola:
        print("La cola está vacía.")
        return
    # Convertimos a lista para mostrar el orden (Frente -> Final)
    print("Contenido de la cola:", list(cola))

def main():
    # Creamos la cola usando deque
    cola = deque()

    # 1. Insertar (push/enqueue): El usuario digita los 5 elementos
    print("--- Implementación de Cola en Python (FIFO) ---")
    print("Digite los 5 elementos para la cola:")
    
    for i in range(5):
        num = int(input(f"Elemento {i+1}: "))
        cola.append(num)  # Agrega al final

    # 2. Mostrar el frente
    if cola:
        print(f"\nPrimer elemento (frente): {cola[0]}")

    # 3. Recorrer
    recorrer_cola(cola)

    # 4. Eliminar (pop/dequeue) dos elementos consecutivos
    print("\nEliminando los dos primeros elementos ingresados...")
    for _ in range(2):
        if cola:
            eliminado = cola.popleft()  # popleft() elimina el primer elemento (frente)
            print(f"Pop: {eliminado}")

    # 5. Mostrar el estado final
    print("\n--- ESTADO FINAL ---")
    if cola:
        print(f"Nuevo frente: {cola[0]}")
        print(f"Último elemento: {cola[-1]}")
    recorrer_cola(cola)

if __name__ == "__main__":
    main()

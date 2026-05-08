# Función para recorrer y mostrar la pila sin destruirla
def recorrer_pila(pila):
    if not pila:
        print("La pila está vacía.")
        return
    # Mostramos una copia invertida para simular el orden de la pila (Tope -> Fondo)
    elementos = list(pila)
    elementos.reverse()
    print("Contenido de la pila (Tope -> Fondo):", elementos)

def main():
    pila = []

    # 1. Insertar (push): El usuario digita los 5 elementos
    print("--- Implementación de Pila en Python ---")
    print("Digite los 5 elementos solicitados (ej. 5, 10, 15, 20, 25):")
    
    for i in range(5):
        num = int(input(f"Elemento {i+1}: "))
        pila.append(num)  # append() actúa como push

    # 2. Mostrar el tope
    if pila:
        print(f"\nTope actual: {pila[-1]}") # El índice -1 accede al último elemento

    # 3. Recorrer
    recorrer_pila(pila)

    # 4. Eliminar (pop) dos elementos consecutivos
    print("\nEliminando los dos últimos elementos...")
    for _ in range(2):
        if pila:
            eliminado = pila.pop()  # pop() elimina y devuelve el último
            print(f"Pop: {eliminado}")

    # 5. Mostrar el estado final
    print("\n--- ESTADO FINAL ---")
    if pila:
        print(f"Nuevo tope: {pila[-1]}")
    recorrer_pila(pila)

if __name__ == "__main__":
    main()

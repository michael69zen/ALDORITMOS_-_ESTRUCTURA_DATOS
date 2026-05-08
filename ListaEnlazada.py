class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None  # Equivale al nullptr de C++

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None

    # Insertar al inicio (Equivalente a push en una pila)
    def insertar_inicio(self, dato):
        nuevo_nodo = Nodo(dato)
        nuevo_nodo.siguiente = self.cabeza
        self.cabeza = nuevo_nodo
        print(f"Elemento {dato} insertado.")

    # Recorrer la lista
    def mostrar_lista(self):
        actual = self.cabeza
        print("\nLista actual:", end=" ")
        while actual:
            print(f"[{actual.dato}] ->", end=" ")
            actual = actual.siguiente
        print("None")

def main():
    mi_lista = ListaEnlazada()
    
    # El usuario digita los datos
    try:
        cantidad = int(input("¿Cuántos números desea ingresar a la lista? "))
        
        for i in range(cantidad):
            valor = int(input(f"Digite el valor {i+1}: "))
            mi_lista.insertar_inicio(valor)
        
        mi_lista.mostrar_lista()
    except ValueError:
        print("Error: Por favor ingrese solo números enteros.")

if __name__ == "__main__":
    main()

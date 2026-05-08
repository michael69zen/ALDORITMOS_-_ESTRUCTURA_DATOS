#include <iostream>

using namespace std;

struct Nodo {
    int dato;
    Nodo* siguiente;
};

// Función para insertar elementos al inicio
void insertarInicio(Nodo*& lista, int n) {
    Nodo* nuevo_nodo = new Nodo(); // 1. Crear espacio en memoria
    nuevo_nodo->dato = n;          // 2. Asignar el dato
    nuevo_nodo->siguiente = lista; // 3. Apuntar al antiguo inicio
    lista = nuevo_nodo;            // 4. El nuevo nodo ahora es el inicio
    cout << "Elemento " << n << " insertado correctamente.\n";
}

// Función para mostrar la lista
void mostrarLista(Nodo* lista) {
    Nodo* actual = lista;
    cout << "\nLista completa: ";
    while (actual != nullptr) {
        cout << "[" << actual->dato << "] -> ";
        actual = actual->siguiente;
    }
    cout << "NULL" << endl;
}

int main() {
    Nodo* lista = nullptr; // Inicializamos la lista vacía
    int valor, cantidad;

    cout << "¿Cuantos numeros desea ingresar? ";
    cin >> cantidad;

    for (int i = 0; i < cantidad; i++) {
        cout << "Digite un numero: ";
        cin >> valor;
        insertarInicio(lista, valor);
    }

    mostrarLista(lista);

    return 0;
}

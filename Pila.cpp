#include <iostream>
#include <stack>

using namespace std;

// Función para mostrar la pila sin borrar los datos originales
void recorrerPila(stack<int> pila) {
    if (pila.empty()) {
        cout << "La pila esta vacia." << endl;
        return;
    }
    while (!pila.empty()) {
        cout << "[" << pila.top() << "] ";
        pila.pop();
    }
    cout << endl;
}

int main() {
    stack<int> miPila;
    int numero;

    // 1. Insertar (push): El usuario digita los 5 elementos solicitados
    cout << "Implementacion de una Pila (Referencia: image_1a6315.png)" << endl;
    cout << "Por favor, ingrese 5 numeros:" << endl;
    
    for (int i = 0; i < 5; i++) {
        cout << "Digite valor para la posicion " << i + 1 << ": ";
        cin >> numero;
        miPila.push(numero);
    }

    // 2. Mostrar el tope
    cout << "\nEl elemento en el tope es: " << miPila.top() << endl;

    // 3. Recorrer la pila (Estado inicial)
    cout << "Estado actual de la pila: ";
    recorrerPila(miPila);

    // 4. Eliminar (pop) dos elementos consecutivos
    cout << "\nEliminando los dos ultimos elementos ingresados..." << endl;
    for (int i = 0; i < 2; i++) {
        if (!miPila.empty()) {
            cout << "Eliminando (pop): " << miPila.top() << endl;
            miPila.pop();
        }
    }

    // 5. Mostrar el estado final
    cout << "\n--- ESTADO FINAL ---" << endl;
    if (!miPila.empty()) {
        cout << "Nuevo tope: " << miPila.top() << endl;
    }
    cout << "Elementos que quedaron en la pila: ";
    recorrerPila(miPila);

    return 0;
}

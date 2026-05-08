#include <iostream>
#include <queue> // Librería para colas

using namespace std;

// Función para recorrer la cola sin destruirla (usa una copia)
void recorrerCola(queue<int> cola) {
    if (cola.empty()) {
        cout << "La cola esta vacia." << endl;
        return;
    }
    while (!cola.empty()) {
        cout << "[" << cola.front() << "] ";
        cola.pop(); // Al ser copia, no afecta a la cola original
    }
    cout << endl;
}

int main() {
    queue<int> miCola;
    int numero;

    // 1. Insertar (push): El usuario digita los 5 elementos
    cout << "--- Implementacion de una Cola (FIFO) ---" << endl;
    cout << "Ingrese 5 numeros para la cola:" << endl;
    
    for (int i = 0; i < 5; i++) {
        cout << "Digite valor " << i + 1 << ": ";
        cin >> numero;
        miCola.push(numero); // Inserta al final
    }

    // 2. Mostrar el frente (en colas el "tope" inicial es el frente)
    cout << "\nEl primer elemento (frente) es: " << miCola.front() << endl;

    // 3. Recorrer la cola
    cout << "Estado actual de la cola (Frente -> Final): ";
    recorrerCola(miCola);

    // 4. Eliminar (pop) dos elementos consecutivos
    cout << "\nEliminando los dos primeros elementos ingresados..." << endl;
    for (int i = 0; i < 2; i++) {
        if (!miCola.empty()) {
            cout << "Eliminando (pop): " << miCola.front() << endl;
            miCola.pop(); // Elimina el que está al frente
        }
    }

    // 5. Mostrar el estado final
    cout << "\n--- ESTADO FINAL ---" << endl;
    if (!miCola.empty()) {
        cout << "Nuevo frente: " << miCola.front() << endl;
        cout << "Ultimo elemento: " << miCola.back() << endl;
    }
    cout << "Elementos restantes: ";
    recorrerCola(miCola);

    return 0;
}

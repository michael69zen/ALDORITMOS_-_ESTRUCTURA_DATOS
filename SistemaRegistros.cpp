#include <iostream>
#include <fstream>
#include <string>

using namespace std;

// Clase que representa el Registro
class Registro {
public:
    int id;
    string nombre;

    void mostrar() {
        cout << "ID: " << id << " | Nombre: " << nombre << endl;
    }
};

// Clase Nodo de la Lista Doble
struct Nodo {
    Registro dato;
    Nodo* siguiente;
    Nodo* anterior;
};

// Clase Gestor de Registros (POO)
class GestorRegistros {
private:
    Nodo* cabeza;
    Nodo* cola;

public:
    GestorRegistros() : cabeza(nullptr), cola(nullptr) {}

    // Agregar registro al final
    void agregar(int id, string nombre) {
        Nodo* nuevo = new Nodo();
        nuevo->dato = {id, nombre};
        nuevo->siguiente = nullptr;

        if (!cabeza) {
            nuevo->anterior = nullptr;
            cabeza = cola = nuevo;
        } else {
            nuevo->anterior = cola;
            cola->siguiente = nuevo;
            cola = nuevo;
        }
    }

    // Almacenamiento en Archivo
    void guardarEnArchivo(string nombreArchivo) {
        ofstream archivo(nombreArchivo);
        Nodo* actual = cabeza;
        while (actual) {
            archivo << actual->dato.id << "," << actual->dato.nombre << endl;
            actual = actual->siguiente;
        }
        archivo.close();
        cout << "Datos guardados en " << nombreArchivo << endl;
    }

    // Recuperación desde Archivo
    void cargarDesdeArchivo(string nombreArchivo) {
        ifstream archivo(nombreArchivo);
        string linea, nom;
        int id;
        while (archivo >> id) {
            archivo.ignore(); // saltar la coma
            getline(archivo, nom);
            agregar(id, nom);
        }
        archivo.close();
    }

    void mostrarTodo() {
        Nodo* actual = cabeza;
        while (actual) {
            actual->dato.mostrar();
            actual = actual->siguiente;
        }
    }
};

int main() {
    GestorRegistros sistema;

    // 1. Recuperar datos previos
    sistema.cargarDesdeArchivo("registros.txt");

    // 2. Interacción
    cout << "--- Sistema de Gestion de Registros ---" << endl;
    sistema.agregar(101, "Ana Garcia");
    sistema.agregar(102, "Luis Perez");

    cout << "\nRegistros actuales:" << endl;
    sistema.mostrarTodo();

    // 3. Almacenamiento persistente
    sistema.guardarEnArchivo("registros.txt");

    return 0;
}

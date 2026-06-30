// Biblioteca para entrada y salida de datos (cout, endl)
#include <iostream>

// Biblioteca que permite utilizar listas enlazadas (list)
#include <list>

// Biblioteca que permite utilizar vectores dinámicos (vector)
#include <vector>

// Permite utilizar los elementos de la biblioteca estándar
// sin escribir std:: delante de cada uno.
using namespace std;

// Definición de la clase HashTable
class HashTable {

    // Número total de cubetas (buckets) de la tabla hash
    int buckets;

    // Vector donde cada posición contiene una lista enlazada.
    // Se utiliza encadenamiento separado para manejar colisiones.
    vector<list<int>> table;

    // Función hash privada.
    // Calcula el índice donde se almacenará una clave.
    int hashFunction(int key) {
        return key % buckets;   // Residuo de la división
    }

public:

    // Constructor de la clase.
    // Recibe el número de cubetas que tendrá la tabla.
    HashTable(int size) : buckets(size), table(size) {}

    // Función para insertar un elemento en la tabla hash.
    void insertItem(int key) {

        // Calcula la posición utilizando la función hash.
        int idx = hashFunction(key);

        // Inserta el elemento al final de la lista correspondiente.
        table[idx].push_back(key);
    }

    // Función para buscar un elemento.
    // Devuelve true si existe y false si no existe.
    bool searchItem(int key) {

        // Calcula el índice donde debería encontrarse.
        int idx = hashFunction(key);

        // Recorre todos los elementos de la lista.
        for (int val : table[idx])

            // Si encuentra el valor buscado
            if (val == key)
                return true;

        // Si termina el recorrido y no lo encontró
        return false;
    }

    // Función para mostrar toda la tabla hash.
    void display() {

        // Recorre todas las cubetas.
        for (int i = 0; i < buckets; i++) {

            // Imprime el número de la cubeta.
            cout << i << ": ";

            // Recorre todos los elementos almacenados en esa cubeta.
            for (int val : table[i])

                // Imprime cada valor seguido de una flecha.
                cout << val << " -> ";

            // Marca el final de la lista.
            cout << "NULL\n";
        }
    }
};

// Función principal del programa.
int main() {

    // Crea una tabla hash con 7 cubetas.
    HashTable ht(7);

    // Inserta el número 15.
    ht.insertItem(15);

    // Inserta el número 11.
    ht.insertItem(11);

    // Inserta el número 27.
    ht.insertItem(27);

    // Inserta el número 8.
    ht.insertItem(8);

    // Inserta el número 12.
    ht.insertItem(12);

    // Muestra el contenido completo de la tabla.
    ht.display();

    // Busca el número 27 e imprime si existe o no.
    cout << "¿Existe 27? "
         << (ht.searchItem(27) ? "Sí" : "No")
         << endl;

    // Finaliza correctamente el programa.
    return 0;
}

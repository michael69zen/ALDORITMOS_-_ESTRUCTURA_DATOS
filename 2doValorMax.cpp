#include <iostream>
#include <limits> // Para usar el valor mínimo posible

using namespace std;

void buscarSegundoMasAlto(int arreglo[], int n) {
    if (n < 2) {
        cout << "El arreglo debe tener al menos dos elementos." << endl;
        return;
    }

    // Inicializamos con el valor más pequeño posible para un entero
    int maximo = numeric_limits<int>::min();
    int segundoMaximo = numeric_limits<int>::min();

    for (int i = 0; i < n; i++) {
        // Caso 1: El elemento actual es mayor que el máximo actual
        if (arreglo[i] > maximo) {
            segundoMaximo = maximo; // El anterior máximo pasa a ser el segundo
            maximo = arreglo[i];    // El actual se convierte en el nuevo máximo
        }
        // Caso 2: Es mayor que el segundo pero menor que el máximo
        else if (arreglo[i] > segundoMaximo && arreglo[i] != maximo) {
            segundoMaximo = arreglo[i];
        }
    }

    if (segundoMaximo == numeric_limits<int>::min()) {
        cout << "No existe un segundo valor distinto al maximo." << endl;
    } else {
        cout << "El maximo es: " << maximo << endl;
        cout << "El segundo valor mas alto es: " << segundoMaximo << endl;
    }
}

int main() {
    int n;
    cout << "Ingrese la cantidad de elementos (N): ";
    cin >> n;

    if (n <= 0) return 0;

    int* arreglo = new int[n]; // Memoria dinámica para N elementos

    for (int i = 0; i < n; i++) {
        cout << "Elemento [" << i << "]: ";
        cin >> arreglo[i];
    }

    buscarSegundoMasAlto(arreglo, n);

    delete[] arreglo; // Liberar memoria
    return 0;
}

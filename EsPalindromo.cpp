#include <iostream>

using namespace std;

bool esPalindromo(char cadena[]) {
    int longitud = 0;

    // 1. Calcular la longitud manualmente
    while (cadena[longitud] != '\0') {
        longitud++;
    }

    // 2. Comparar caracteres desde los extremos
    int inicio = 0;
    int fin = longitud - 1;

    while (inicio < fin) {
        // Si los caracteres en las posiciones opuestas no coinciden
        if (cadena[inicio] != cadena[fin]) {
            return false; 
        }
        inicio++;
        fin--;
    }

    return true;
}

int main() {
    char palabra[100];

    cout << "Ingrese una palabra: ";
    cin >> palabra;

    if (esPalindromo(palabra)) {
        cout << "Es un palindromo." << endl;
    } else {
        cout << "No es un palindromo." << endl;
    }

    return 0;
}

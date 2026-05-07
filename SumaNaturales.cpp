#include <iostream>
#include <chrono>

using namespace std;
using namespace std::chrono;

// Implementación O(n) - Bucle
long long sumaLineal(int n) {
    long long suma = 0;
    for (int i = 1; i <= n; i++) {
        suma += i;
    }
    return suma;
}

// Implementación O(1) - Fórmula
long long sumaConstante(long long n) {
    return (n * (n + 1)) / 2;
}

int main() {
    int valores[] = {1000, 10000, 100000, 1000000};

    for (int n : valores) {
        cout << "--- N = " << n << " ---" << endl;

        // Medir O(n)
        auto inicio = high_resolution_clock::now();
        long long resN = sumaLineal(n);
        auto fin = high_resolution_clock::now();
        auto durN = duration_cast<nanoseconds>(fin - inicio).count();

        // Medir O(1)
        inicio = high_resolution_clock::now();
        long long res1 = sumaConstante(n);
        fin = high_resolution_clock::now();
        auto dur1 = duration_cast<nanoseconds>(fin - inicio).count();

        cout << "O(n) Tiempo: " << durN << " ns | Resultado: " << resN << endl;
        cout << "O(1) Tiempo: " << dur1 << " ns | Resultado: " << res1 << endl << endl;
    }
    return 0;
}

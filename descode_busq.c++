#include <bits/stdc++.h> 
// Incluye casi todas las librerías estándar de C++.
// Se usa mucho en programación competitiva y pruebas rápidas.

using namespace std;
// Permite escribir vector, cout, string, etc. sin poner "std::" antes.

// Búsqueda lineal: O(n), no requiere orden
int busquedaLineal(const vector<int>& a, int x) {
    // Recorre el arreglo desde el primer elemento hasta el último.
    for (size_t i = 0; i < a.size(); ++i)
        // Si el elemento actual es igual al valor buscado, devuelve su índice.
        if (a[i] == x) return (int)i;

    // Si termina el recorrido y no lo encuentra, devuelve -1.
    return -1;
}

// Búsqueda binaria: O(log n), REQUIERE arreglo ordenado
int busquedaBinaria(const vector<int>& a, int x) {
    // l = límite izquierdo, r = límite derecho.
    int l = 0, r = (int)a.size() - 1;

    // Mientras el intervalo de búsqueda siga siendo válido...
    while (l <= r) {
        // Calcula la mitad del intervalo de forma segura.
        int m = l + (r - l) / 2;

        // Si el elemento central es el buscado, devuelve su posición.
        if (a[m] == x) return m;

        // Si el valor de la mitad es menor que x, busca en la parte derecha.
        else if (a[m] < x) l = m + 1;

        // Si el valor de la mitad es mayor que x, busca en la parte izquierda.
        else r = m - 1;
    }

    // Si no se encontró, devuelve -1.
    return -1;
}

// Búsqueda exponencial: O(log k), útil cuando no se conoce tamaño efectivo
int busquedaExponencial(const vector<int>& a, int x) {
    // Si el arreglo está vacío, no hay nada que buscar.
    if (a.empty()) return -1;

    // Si el primer elemento ya es el buscado, devuelve la posición 0.
    if (a[0] == x) return 0;

    // Empieza en 1 para ir duplicando la posición.
    int i = 1;

    // Duplica i mientras esté dentro del arreglo y el valor sea menor que x.
    while (i < (int)a.size() && a[i] < x) i <<= 1;
    // i <<= 1 equivale a i = i * 2.

    // Define el rango donde probablemente está el valor.
    int l = i / 2, r = min(i, (int)a.size() - 1);

    // Ahora aplica búsqueda binaria dentro de ese rango.
    while (l <= r) {
        int m = l + (r - l) / 2;

        if (a[m] == x) return m;
        else if (a[m] < x) l = m + 1;
        else r = m - 1;
    }

    return -1;
}

// Búsqueda por interpolación: depende de distribución (idealmente uniforme)
int busquedaInterpolacion(const vector<int>& a, int x) {
    // low y high representan los extremos del intervalo actual.
    int low = 0, high = (int)a.size() - 1;

    // Mientras x esté dentro del rango de valores actuales...
    while (low <= high && x >= a[low] && x <= a[high]) {

        // Si todos los valores del intervalo son iguales...
        if (a[low] == a[high])
            // Entonces solo puede ser x si coincide con ese valor.
            return (a[low] == x ? low : -1);

        // Estima la posición donde podría estar x según su valor.
        long long pos = low + (long long)((double)(high - low) *
                                          ((double)(x - a[low]) /
                                           (double)(a[high] - a[low])));

        // Si la posición calculada sale del rango, se detiene.
        if (pos < low || pos > high) break;

        // Si encontró el valor, devuelve la posición.
        if (a[pos] == x) return (int)pos;

        // Si el valor en pos es menor que x, busca a la derecha.
        if (a[pos] < x) low = (int)pos + 1;

        // Si el valor en pos es mayor que x, busca a la izquierda.
        else high = (int)pos - 1;
    }

    // Si no se encontró, devuelve -1.
    return -1;
}

// ----------------------
// Medición de tiempo
// ----------------------

template <class F>
double medir(const vector<int>& a, const vector<int>& queries, F buscador) {
    // Alias del reloj de alta resolución para medir tiempos.
    using clk = chrono::high_resolution_clock;

    // Guarda el tiempo inicial.
    auto t0 = clk::now();

    // volatile evita que el compilador elimine el cálculo por optimización.
    volatile long long checksum = 0;

    // Ejecuta la función de búsqueda para cada query.
    for (int x : queries) checksum += buscador(a, x);

    // Guarda el tiempo final.
    auto t1 = clk::now();

    // Calcula el tiempo transcurrido en milisegundos.
    chrono::duration<double, milli> ms = t1 - t0;

    // Devuelve el promedio de tiempo por búsqueda.
    return ms.count() / (double)queries.size();
}

// ----------------------
// MAIN
// ----------------------

int main() {
    // Desactiva sincronización con stdio para acelerar entrada/salida.
    ios::sync_with_stdio(false);

    // Desvincula cin de cout para mejorar rendimiento.
    cin.tie(nullptr);

    // Tamaños de prueba: 10^4, 10^5, 5×10^5
    vector<int> ns = {10000, 100000, 500000};

    // Generador aleatorio con semilla fija para que los resultados sean reproducibles.
    mt19937 rng(123);

    // Recorre cada tamaño de prueba.
    for (int n : ns) {

        // Dataset uniforme: números ordenados de 0 a n-1.
        vector<int> uni(n);
        iota(uni.begin(), uni.end(), 0);

        // Dataset sesgado: muchos valores pequeños y algunos grandes.
        vector<int> ses(n);
        for (int i = 0; i < n; i++) {
            // Genera un número real aleatorio entre 0 y 1.
            double u = uniform_real_distribution<double>(0, 1)(rng);

            // Si u < 0.8, genera un valor cercano al inicio.
            if (u < 0.8)
                ses[i] = uniform_int_distribution<int>(0, (int)(0.1 * n))(rng);
            // Si no, genera un valor más disperso y más grande.
            else
                ses[i] = uniform_int_distribution<int>((int)(0.1 * n), 5 * n)(rng);
        }

        // Ordena el dataset sesgado para poder usar búsquedas que requieren orden.
        sort(ses.begin(), ses.end());

        // Dataset desordenado: copia del uniforme.
        vector<int> des = uni;

        // Mezcla aleatoriamente los elementos.
        shuffle(des.begin(), des.end(), rng);

        // Generador de consultas de búsqueda.
        auto mkqueries = [&](const vector<int>& base) {
            // Vector donde se guardarán las consultas.
            vector<int> q;
            q.reserve(1000);

            // Distribución para elegir índices válidos dentro del arreglo.
            uniform_int_distribution<int> idx(0, (int)base.size() - 1);

            // 700 consultas sí existentes en el arreglo.
            for (int i = 0; i < 700; i++) q.push_back(base[idx(rng)]);

            // 300 consultas que probablemente no existan.
            for (int i = 0; i < 300; i++) q.push_back(10 * (int)base.size() + i);

            // Mezcla las consultas para que no estén ordenadas.
            shuffle(q.begin(), q.end(), rng);

            // Devuelve las consultas generadas.
            return q;
        };

        // Crea consultas para cada dataset.
        auto q_uni = mkqueries(uni);
        auto q_ses = mkqueries(ses);
        auto q_des = mkqueries(des);

        // Función que imprime el reporte de tiempos.
        auto report = [&](const string& nombre, const vector<int>& arr, const vector<int>& q) {
            cout << "n = " << n << ", dataset = " << nombre << "\n";

            // Mide búsqueda lineal.
            cout << "  busqueda lineal      : " << medir(arr, q, busquedaLineal) << " ms/busq\n";

            // Si el arreglo está ordenado, puede usar las otras búsquedas.
            if (is_sorted(arr.begin(), arr.end())) {
                cout << "  busqueda binaria     : " << medir(arr, q, busquedaBinaria) << " ms/busq\n";
                cout << "  busqueda exponencial : " << medir(arr, q, busquedaExponencial) << " ms/busq\n";
                cout << "  interpolacion        : " << medir(arr, q, busquedaInterpolacion) << " ms/busq\n";
            } else {
                // Si no está ordenado, explica por qué no se aplican otros métodos.
                cout << "  NOTA: El dataset no esta ordenado.\n";
                cout << "  -> La busqueda binaria, exponencial e interpolacion requieren orden total.\n";
                cout << "  -> Sin orden, no pueden descartar mitades del espacio de busqueda correctamente.\n";
                cout << "  -> Usarlas produciria resultados incorrectos (no solo mas lentos).\n";
                cout << "  -> Por lo tanto, solo la busqueda lineal es valida en este caso.\n";
            }
        };

        // Reporte para cada tipo de dataset.
        report("uniforme_ordenado", uni, q_uni);
        report("sesgado_ordenado", ses, q_ses);
        report("desordenado", des, q_des);

        // Separador entre tamaños de prueba.
        cout << "---------------------------------------------\n";
    }

    // Fin del programa.
    return 0;
}

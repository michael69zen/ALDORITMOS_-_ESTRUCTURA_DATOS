#include <bits/stdc++.h> // STL completa (válido para experimentación)
using namespace std;

// ----------------------
// Algoritmos de búsqueda
// ----------------------

// Búsqueda lineal: O(n), no requiere orden
int busquedaLineal(const vector<int>& a, int x) {
    for (size_t i = 0; i < a.size(); ++i)
        if (a[i] == x) return (int)i;
    return -1;
}

// Búsqueda binaria: O(log n), REQUIERE arreglo ordenado
int busquedaBinaria(const vector<int>& a, int x) {
    int l = 0, r = (int)a.size() - 1;
    while (l <= r) {
        int m = l + (r - l) / 2;
        if (a[m] == x) return m;
        else if (a[m] < x) l = m + 1;
        else r = m - 1;
    }
    return -1;
}

// Búsqueda exponencial: O(log k), útil cuando no se conoce tamaño efectivo
int busquedaExponencial(const vector<int>& a, int x) {
    if (a.empty()) return -1;
    if (a[0] == x) return 0;

    int i = 1;
    while (i < (int)a.size() && a[i] < x) i <<= 1;

    int l = i / 2, r = min(i, (int)a.size() - 1);

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
    int low = 0, high = (int)a.size() - 1;

    while (low <= high && x >= a[low] && x <= a[high]) {
        if (a[low] == a[high])
            return (a[low] == x ? low : -1);

        long long pos = low + (long long)((double)(high - low) *
                                          ((double)(x - a[low]) /
                                           (double)(a[high] - a[low])));

        if (pos < low || pos > high) break;

        if (a[pos] == x) return (int)pos;
        if (a[pos] < x) low = (int)pos + 1;
        else high = (int)pos - 1;
    }
    return -1;
}

// ----------------------
// Medición de tiempo
// ----------------------

template <class F>
double medir(const vector<int>& a, const vector<int>& queries, F buscador) {
    using clk = chrono::high_resolution_clock;
    auto t0 = clk::now();

    volatile long long checksum = 0;
    for (int x : queries) checksum += buscador(a, x);

    auto t1 = clk::now();
    chrono::duration<double, milli> ms = t1 - t0;

    return ms.count() / (double)queries.size(); // ms por búsqueda
}

// ----------------------
// MAIN
// ----------------------

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // Tamaños: 10^4, 10^5, 5×10^5
    vector<int> ns = {10000, 100000, 500000};

    mt19937 rng(123); // semilla fija → reproducibilidad

    for (int n : ns) {

        // Dataset uniforme (ideal para interpolación)
        vector<int> uni(n);
        iota(uni.begin(), uni.end(), 0);

        // Dataset sesgado
        vector<int> ses(n);
        for (int i = 0; i < n; i++) {
            double u = uniform_real_distribution<double>(0, 1)(rng);
            if (u < 0.8)
                ses[i] = uniform_int_distribution<int>(0, (int)(0.1 * n))(rng);
            else
                ses[i] = uniform_int_distribution<int>((int)(0.1 * n), 5 * n)(rng);
        }
        sort(ses.begin(), ses.end());

        // Dataset desordenado
        vector<int> des = uni;
        shuffle(des.begin(), des.end(), rng);

        // Generador de queries
        auto mkqueries = [&](const vector<int>& base) {
            vector<int> q;
            q.reserve(1000);

            uniform_int_distribution<int> idx(0, (int)base.size() - 1);

            for (int i = 0; i < 700; i++) q.push_back(base[idx(rng)]);
            for (int i = 0; i < 300; i++) q.push_back(10 * (int)base.size() + i);

            shuffle(q.begin(), q.end(), rng);
            return q;
        };

        auto q_uni = mkqueries(uni);
        auto q_ses = mkqueries(ses);
        auto q_des = mkqueries(des);

        // Reporte
        auto report = [&](const string& nombre, const vector<int>& arr, const vector<int>& q) {
            cout << "n = " << n << ", dataset = " << nombre << "\n";

            cout << "  busqueda lineal      : " << medir(arr, q, busquedaLineal) << " ms/busq\n";

            if (is_sorted(arr.begin(), arr.end())) {
                cout << "  busqueda binaria     : " << medir(arr, q, busquedaBinaria) << " ms/busq\n";
                cout << "  busqueda exponencial : " << medir(arr, q, busquedaExponencial) << " ms/busq\n";
                cout << "  interpolacion        : " << medir(arr, q, busquedaInterpolacion) << " ms/busq\n";
            } else {
                cout << "  NOTA: El dataset no esta ordenado.\n";
                cout << "  -> La busqueda binaria, exponencial e interpolacion requieren orden total.\n";
                cout << "  -> Sin orden, no pueden descartar mitades del espacio de busqueda correctamente.\n";
                cout << "  -> Usarlas produciria resultados incorrectos (no solo mas lentos).\n";
                cout << "  -> Por lo tanto, solo la busqueda lineal es valida en este caso.\n";
            }
        };

        report("uniforme_ordenado", uni, q_uni);
        report("sesgado_ordenado", ses, q_ses);
        report("desordenado", des, q_des);

        cout << "---------------------------------------------\n";
    }

    return 0;
}

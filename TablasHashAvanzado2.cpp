#include <iostream>
#include <vector>
#include <list>
#include <string>
#include <chrono>
#include <iomanip>
#include <fstream> // Necesario para leer archivos

using namespace std;
using namespace chrono;

/* =========================
   Hash con encadenamiento
   ========================= */
class HashTableChaining {
private:
    int size;
    vector<list<pair<string, string>>> table;

public:
    int collisions = 0;

    HashTableChaining(int s) : size(s), table(s) {}

    int hash_function(const string& key) {
        return std::hash<string>{}(key) % size;
    }

    void insert(const string& key, const string& value) {
        int index = hash_function(key);
        if (!table[index].empty()) collisions++;
        table[index].push_back({key, value});
    }

    string search(const string& key) {
        int index = hash_function(key);
        for (auto& kv : table[index]) {
            if (kv.first == key) return kv.second;
        }
        return "";
    }
};

/* =========================
   Lineal
   ========================= */
class HashTableLinearProbing {
private:
    int size;
    vector<pair<string, string>> table;
    vector<bool> occupied;

public:
    int collisions = 0;

    HashTableLinearProbing(int s) : size(s) {
        table.resize(s);
        occupied.resize(s, false);
    }

    int hash_function(const string& key) {
        return std::hash<string>{}(key) % size;
    }

    void insert(const string& key, const string& value) {
        int index = hash_function(key);
        while (occupied[index]) {
            collisions++;
            index = (index + 1) % size;
        }
        table[index] = {key, value};
        occupied[index] = true;
    }

    string search(const string& key) {
        int index = hash_function(key);
        int start = index;
        while (occupied[index]) {
            if (table[index].first == key)
                return table[index].second;
            index = (index + 1) % size;
            if (index == start) break;
        }
        return "";
    }
};

/* =========================
   Cuadrático
   ========================= */
class HashTableQuadraticProbing {
private:
    int size;
    vector<pair<string, string>> table;
    vector<bool> occupied;

public:
    int collisions = 0;

    HashTableQuadraticProbing(int s) : size(s) {
        table.resize(s);
        occupied.resize(s, false);
    }

    int hash_function(const string& key) {
        return std::hash<string>{}(key) % size;
    }

    void insert(const string& key, const string& value) {
        int index = hash_function(key);
        int i = 0;
        while (occupied[(index + i * i) % size]) {
            collisions++;
            i++;
        }
        int newIndex = (index + i * i) % size;
        table[newIndex] = {key, value};
        occupied[newIndex] = true;
    }

    string search(const string& key) {
        int index = hash_function(key);
        int i = 0;
        while (occupied[(index + i * i) % size]) {
            int current = (index + i * i) % size;
            if (table[current].first == key)
                return table[current].second;
            i++;
            if (i == size) break;
        }
        return "";
    }
};

/* =========================
   Doble hashing
   ========================= */
class HashTableDoubleHashing {
private:
    int size;
    vector<pair<string, string>> table;
    vector<bool> occupied;

public:
    int collisions = 0;

    HashTableDoubleHashing(int s) : size(s) {
        table.resize(s);
        occupied.resize(s, false);
    }

    int hash1(const string& key) {
        return std::hash<string>{}(key) % size;
    }

    int hash2(const string& key) {
        return 1 + (std::hash<string>{}(key) % (size - 1));
    }

    void insert(const string& key, const string& value) {
        int index = hash1(key);
        int step = hash2(key);
        int i = 0;
        while (occupied[(index + i * step) % size]) {
            collisions++;
            i++;
        }
        int newIndex = (index + i * step) % size;
        table[newIndex] = {key, value};
        occupied[newIndex] = true;
    }

    string search(const string& key) {
        int index = hash1(key);
        int step = hash2(key);
        int i = 0;
        while (occupied[(index + i * step) % size]) {
            int current = (index + i * step) % size;
            if (table[current].first == key)
                return table[current].second;
            i++;
            if (i == size) break;
        }
        return "";
    }
};

/* =========================
   MAIN
   ========================= */
int main() {
    vector<string> keys;

    // ---> LECTURA DEL ARCHIVO EXPORTADO <---
    ifstream archivo("sessions_exportadas.txt");

    if (!archivo.is_open()) {
        cout << "Error: No se pudo abrir 'sessions_exportadas.txt'." << endl;
        cout << "Asegurate de que el archivo este en la misma carpeta que este ejecutable (.exe)." << endl;
        return 1;
    }

    string session;
    while (getline(archivo, session)) {
        // Limpiar posible retorno de carro al final (común al pasar texto entre sistemas)
        if (!session.empty() && session.back() == '\r') {
            session.pop_back();
        }
        keys.push_back(session);
    }
    archivo.close();

    cout << "Datos cargados: " << keys.size() << " sesiones leidas exitosamente.\n\n";
    
    // Si por alguna razon no leyo 10000, limitarlo o avisar
    if(keys.size() == 0) {
        cout << "El archivo esta vacio." << endl;
        return 1;
    }

    int table_size = 20011;

    double insert[4], search_time[4];
    int collisions[4];

    auto start = high_resolution_clock::now();
    auto end = start;

    // Encadenamiento
    HashTableChaining chain(table_size);
    start = high_resolution_clock::now();
    for (auto& k : keys) chain.insert(k, k);
    end = high_resolution_clock::now();
    insert[0] = duration<double>(end - start).count();
    
    start = high_resolution_clock::now();
    // Buscar los primeros 1000 elementos (como en Python)
    int search_limit = min(1000, (int)keys.size()); 
    for (int i = 0; i < search_limit; i++) chain.search(keys[i]);
    end = high_resolution_clock::now();
    search_time[0] = duration<double>(end - start).count();
    collisions[0] = chain.collisions;

    // Lineal
    HashTableLinearProbing linear(table_size);
    start = high_resolution_clock::now();
    for (auto& k : keys) linear.insert(k, k);
    end = high_resolution_clock::now();
    insert[1] = duration<double>(end - start).count();
    
    start = high_resolution_clock::now();
    for (int i = 0; i < search_limit; i++) linear.search(keys[i]);
    end = high_resolution_clock::now();
    search_time[1] = duration<double>(end - start).count();
    collisions[1] = linear.collisions;

    // Cuadrático
    HashTableQuadraticProbing quad(table_size);
    start = high_resolution_clock::now();
    for (auto& k : keys) quad.insert(k, k);
    end = high_resolution_clock::now();
    insert[2] = duration<double>(end - start).count();
    
    start = high_resolution_clock::now();
    for (int i = 0; i < search_limit; i++) quad.search(keys[i]);
    end = high_resolution_clock::now();
    search_time[2] = duration<double>(end - start).count();
    collisions[2] = quad.collisions;

    // Doble hashing
    HashTableDoubleHashing dbl(table_size);
    start = high_resolution_clock::now();
    for (auto& k : keys) dbl.insert(k, k);
    end = high_resolution_clock::now();
    insert[3] = duration<double>(end - start).count();
    
    start = high_resolution_clock::now();
    for (int i = 0; i < search_limit; i++) dbl.search(keys[i]);
    end = high_resolution_clock::now();
    search_time[3] = duration<double>(end - start).count();
    collisions[3] = dbl.collisions;

    string names[4] = {
        "Encadenamiento",
        "Lineal",
        "Cuadratico",
        "Doble Hashing"
    };

    cout << " Tabla Comparativa de Rendimiento \n";
    cout << "---------------------------------------------------------------\n";
    cout << left << setw(20) << "Metodo"
         << setw(15) << "Insert (s)"
         << setw(15) << "Search (s)"
         << setw(10) << "Colisiones" << "\n";

    cout << "---------------------------------------------------------------\n";

    for (int i = 0; i < 4; i++) {
        // Usamos fixed y setprecision para evitar ver los tiempos en formato cientifico (ej: 1e-05)
        cout << left << setw(20) << names[i]
             << fixed << setprecision(6) << setw(15) << insert[i]
             << fixed << setprecision(6) << setw(15) << search_time[i]
             << setw(10) << collisions[i] << "\n";
    }

    cout << "---------------------------------------------------------------\n";

    return 0;
}

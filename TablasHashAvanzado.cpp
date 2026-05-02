#include <iostream>
#include <vector>
#include <list>
#include <string>
#include <chrono>
#include <iomanip>

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
    for (int i = 0; i < 10000; i++)
        keys.push_back("user_" + to_string(i));

    int table_size = 20011;

    double insert[4], search[4];
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
    for (int i = 0; i < 1000; i++) chain.search(keys[i]);
    end = high_resolution_clock::now();
    search[0] = duration<double>(end - start).count();
    collisions[0] = chain.collisions;

    // Lineal
    HashTableLinearProbing linear(table_size);
    start = high_resolution_clock::now();
    for (auto& k : keys) linear.insert(k, k);
    end = high_resolution_clock::now();
    insert[1] = duration<double>(end - start).count();
    start = high_resolution_clock::now();
    for (int i = 0; i < 1000; i++) linear.search(keys[i]);
    end = high_resolution_clock::now();
    search[1] = duration<double>(end - start).count();
    collisions[1] = linear.collisions;

    // Cuadrático
    HashTableQuadraticProbing quad(table_size);
    start = high_resolution_clock::now();
    for (auto& k : keys) quad.insert(k, k);
    end = high_resolution_clock::now();
    insert[2] = duration<double>(end - start).count();
    start = high_resolution_clock::now();
    for (int i = 0; i < 1000; i++) quad.search(keys[i]);
    end = high_resolution_clock::now();
    search[2] = duration<double>(end - start).count();
    collisions[2] = quad.collisions;

    // Doble hashing
    HashTableDoubleHashing dbl(table_size);
    start = high_resolution_clock::now();
    for (auto& k : keys) dbl.insert(k, k);
    end = high_resolution_clock::now();
    insert[3] = duration<double>(end - start).count();
    start = high_resolution_clock::now();
    for (int i = 0; i < 1000; i++) dbl.search(keys[i]);
    end = high_resolution_clock::now();
    search[3] = duration<double>(end - start).count();
    collisions[3] = dbl.collisions;

    string names[4] = {
        "Encadenamiento",
        "Lineal",
        "Cuadratico",
        "Doble Hashing"
    };

    cout << "\n Tabla Comparativa de Rendimiento \n";
    cout << "---------------------------------------------------------------\n";
    cout << left << setw(20) << "Metodo"
         << setw(15) << "Insert (s)"
         << setw(15) << "Search (s)"
         << setw(10) << "Colisiones" << "\n";

    cout << "---------------------------------------------------------------\n";

    for (int i = 0; i < 4; i++) {
        cout << left << setw(20) << names[i]
             << setw(15) << insert[i]
             << setw(15) << search[i]
             << setw(10) << collisions[i] << "\n";
    }

    cout << "---------------------------------------------------------------\n";

    return 0;
}

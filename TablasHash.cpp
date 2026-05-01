// ================================================================ 
// PRÁCTICA: TABLAS HASH EN C++ (DATOS KAGGLE)
// Curso: Estructuras de Datos | Semanas 5-6 
// Compilar: g++ -O2 -std=c++17 -o hash_tabla hash_tabla.cpp 
// ================================================================ 
 
#include <iostream> 
#include <fstream> 
#include <sstream> 
#include <string> 
#include <vector> 
#include <list> 
#include <chrono> 
#include <iomanip> 
#include <algorithm>

using namespace std; 
using namespace std::chrono; 
 
// ─────────────────────────────────────────────────────────────── 
// ESTRUCTURA: Registro de datos del CSV 
// ─────────────────────────────────────────────────────────────── 
struct Registro { 
    string clave;    // Campo usado como clave hash (Student_ID) 
    string valor;    // Campo auxiliar (Main_Usage_Case) 
}; 
 
// ─────────────────────────────────────────────────────────────── 
// FUNCIÓN HASH PERSONALIZADA (Polinomial) 
// ─────────────────────────────────────────────────────────────── 
size_t funcionHash(const string& clave, size_t tamanio) { 
    size_t hash = 0;                                          
    for (char c : clave)                                      
        hash = (hash * 31 + (size_t)c) % tamanio;  
    return hash;                                              
} 
 
// ─────────────────────────────────────────────────────────────── 
// CLASE: Tabla Hash con Encadenamiento Separado 
// ─────────────────────────────────────────────────────────────── 
class TablaHashEncadenamiento { 
public: 
    size_t tamanio;                                           
    vector<list<Registro>> tabla;                             
    long long colisiones = 0;                                 
    long long elementos  = 0;                                 
 
    TablaHashEncadenamiento(size_t m) : tamanio(m), tabla(m) {} 
 
    void insertar(const Registro& reg) { 
        size_t idx = funcionHash(reg.clave, tamanio);  
        if (!tabla[idx].empty())                                        
            colisiones++;                                               
        tabla[idx].push_back(reg);                                     
        elementos++; 
    } 
 
    Registro* buscar(const string& clave) { 
        size_t idx = funcionHash(clave, tamanio);               
        for (auto& reg : tabla[idx])                            
            if (reg.clave == clave) return &reg;                
        return nullptr;                                                 
    } 
 
    double factorDeCarga() const { 
        return (double)elementos / tamanio;                     
    } 
}; 
 
// ─────────────────────────────────────────────────────────────── 
// CLASE: Tabla Hash con Sondeo Lineal 
// ─────────────────────────────────────────────────────────────── 
class TablaHashSondeoLineal { 
    enum Estado { VACIO, OCUPADO, ELIMINADO };  
public: 
    size_t tamanio; 
    vector<Registro> tabla;                                     
    vector<Estado>   estados;                                   
    long long colisiones = 0; 
    long long elementos  = 0; 
 
    TablaHashSondeoLineal(size_t m) 
        : tamanio(m), tabla(m), estados(m, VACIO) {} 
 
    bool insertar(const Registro& reg) { 
        if ((double)elementos / tamanio >= 0.75)  
            return false;                                         
        
        size_t idx = funcionHash(reg.clave, tamanio);  
        size_t pasos = 0; 
        
        while (estados[idx] == OCUPADO) {                         
            colisiones++;                                         
            idx = (idx + 1) % tamanio;                           
            if (++pasos >= tamanio) return false; 
        } 
        
        tabla[idx] = reg;                                         
        estados[idx] = OCUPADO;                                   
        elementos++; 
        return true; 
    } 
 
    Registro* buscar(const string& clave) { 
        size_t idx = funcionHash(clave, tamanio); 
        size_t pasos = 0; 
        
        while (estados[idx] != VACIO) {                           
            if (estados[idx] == OCUPADO && tabla[idx].clave == clave) 
                return &tabla[idx];                               
            idx = (idx + 1) % tamanio; 
            if (++pasos >= tamanio) break; 
        } 
        return nullptr;                                           
    } 
}; 

// ─────────────────────────────────────────────────────────────── 
// LECTURA DE CSV INTELIGENTE (Por nombres de columna)
// ─────────────────────────────────────────────────────────────── 
vector<Registro> leerCSV(const string& ruta, const string& nombre_clave, const string& nombre_valor) { 
    vector<Registro> registros; 
    ifstream archivo(ruta);                                         
    
    if (!archivo.is_open()) { 
        cerr << "Error: no se pudo abrir el archivo " << ruta << endl; 
        return registros; 
    } 
    
    string linea; 
    // 1. Leer encabezado para mapear índices
    if (!getline(archivo, linea)) return registros;
    
    stringstream ss_head(linea);
    string col_name;
    int idx_clave = -1, idx_valor = -1, i = 0;
    
    while (getline(ss_head, col_name, ',')) {
        // Limpiar posible salto de línea (\r) al final del nombre
        if (!col_name.empty() && col_name.back() == '\r') col_name.pop_back();
        
        if (col_name == nombre_clave) idx_clave = i;
        if (col_name == nombre_valor) idx_valor = i;
        i++;
    }
    
    if (idx_clave == -1 || idx_valor == -1) {
        cerr << "Error: No se encontraron las columnas '" << nombre_clave << "' o '" << nombre_valor << "' en el CSV." << endl;
        return registros;
    }

    // 2. Leer resto de los datos
    while (getline(archivo, linea)) {                               
        stringstream ss(linea); 
        string campo; 
        vector<string> campos; 
        
        // Manejo básico de comas (nota: no maneja comas dentro de comillas si las hubiera)
        while (getline(ss, campo, ',')) {
            if (!campo.empty() && campo.back() == '\r') campo.pop_back();
            campos.push_back(campo); 
        }
            
        if ((int)campos.size() > max(idx_clave, idx_valor)) { 
            Registro r; 
            r.clave = campos[idx_clave];                            
            r.valor = campos[idx_valor];                            
            if (!r.clave.empty())                                   
                registros.push_back(r); 
        } 
    } 
    archivo.close(); 
    return registros; 
} 
 
// ─────────────────────────────────────────────────────────────── 
// BENCHMARK Y COMPARACIÓN 
// ─────────────────────────────────────────────────────────────── 
void benchmark(const vector<Registro>& datos, vector<size_t> tamanios) { 
    cout << left 
         << setw(8)  << "m" 
         << setw(8)  << "n" 
         << setw(10) << "Col_Enc" 
         << setw(12) << "Ins_Enc(us)" 
         << setw(10) << "Col_SL" 
         << setw(12) << "Ins_SL(us)" << endl; 
    cout << string(60, '-') << endl; 
 
    for (size_t m : tamanios) { 
        size_t n = min(datos.size(), (size_t)(m * 0.65));  // 65% de llenado 
 
        // --- Encadenamiento --- 
        TablaHashEncadenamiento th_enc(m); 
        auto t0 = high_resolution_clock::now();                  // Inicio 
        for (size_t i = 0; i < n; i++) th_enc.insertar(datos[i]); 
        auto t1 = high_resolution_clock::now();                  // Fin 
        auto dur_enc = duration_cast<microseconds>(t1-t0).count(); 
 
        // --- Sondeo Lineal --- 
        TablaHashSondeoLineal th_sl(m); 
        t0 = high_resolution_clock::now(); 
        for (size_t i = 0; i < n; i++) th_sl.insertar(datos[i]); 
        t1 = high_resolution_clock::now(); 
        auto dur_sl = duration_cast<microseconds>(t1-t0).count(); 
 
        cout << left 
             << setw(8)  << m
             << setw(8)  << n 
             << setw(10) << th_enc.colisiones 
             << setw(12) << dur_enc 
             << setw(10) << th_sl.colisiones 
             << setw(12) << dur_sl << endl; 
    } 
} 
 
// ─────────────────────────────────────────────────────────────── 
// FUNCIÓN PRINCIPAL 
// ─────────────────────────────────────────────────────────────── 
int main() { 
    cout << "=== BENCHMARK TABLAS HASH (C++) ===" << endl; 
 
    // Cargar tu dataset real
    string archivo = "AI_Impact_Student_Life_2026.csv";
    cout << "Cargando datos desde: " << archivo << "..." << endl;
    
    vector<Registro> datos = leerCSV(archivo, "Student_ID", "Main_Usage_Case"); 
 
    if (datos.empty()) {
        cout << "No se pudieron cargar los datos. Verifica el archivo CSV." << endl;
        return 1;
    }

    cout << "Registros cargados exitosamente: " << datos.size() << endl << endl; 
 
    vector<size_t> tamanios = {1009, 2003, 4001, 8009};  // Primos 
    benchmark(datos, tamanios);                          // Ejecuta benchmark
 
    return 0; 
}

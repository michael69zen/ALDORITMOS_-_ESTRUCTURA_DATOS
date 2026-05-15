#include <iostream>  // Incluimos iostream para operaciones de entrada y salida
#include <chrono>    // Incluimos chrono para medir el tiempo de ejecución con alta precisión
#include <random>    // Incluimos random para generar números aleatorios
#include <algorithm> // Incluimos algorithm para usar utilidades como std::sort y std::reverse

using namespace std; // Usamos el espacio de nombres estándar para evitar escribir std:: constantemente

// ====================================================================================================
// 1. BUBBLE SORT (Ordenamiento de Burbuja)
// ====================================================================================================
// Recibe un puntero 'arr', el tamaño 'n', y punteros para contabilizar comparaciones e intercambios.
// El uso de punteros (*comps y *swaps) permite modificar las variables originales del 'main' pasadas por referencia.
void bubbleSort(int* arr, int n, long long* comps, long long* swaps) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            
            // Usamos desreferenciación de punteros (*comps) para incrementar el valor en la memoria original.
            (*comps)++; 
            
            // Evaluamos adyacentes a través de la aritmética de índices/punteros.
            if (arr[j] > arr[j + 1]) {
                (*swaps)++; // Incrementamos los intercambios.

                // Intercambio de valores usando una variable temporal
                int temp = arr[j];       
                arr[j] = arr[j + 1];     
                arr[j + 1] = temp;       
            }
        }
    }
}

// ====================================================================================================
// 2. INSERTION SORT (Ordenamiento por Inserción)
// ====================================================================================================
void insertionSort(int* arr, int n, long long* comps, long long* swaps) {
    for (int i = 1; i < n; i++) {
        int key = arr[i]; // 'key' almacena el valor a insertar en la sub-lista.
        int j = i - 1;

        // Evaluamos cuántas veces comparamos al recorrer hacia atrás la sublista ordenada.
        while (j >= 0) {
            (*comps)++; // Incrementamos las comparaciones antes de evaluar en el 'if'.
            if (arr[j] > key) {
                (*swaps)++; // Un desplazamiento en memoria cuenta funcionalmente como un intercambio/movimiento.
                arr[j + 1] = arr[j]; // Desplazamiento.
                j = j - 1;
            } else {
                break; // Ya no hay elementos mayores, salimos.
            }
        }
        arr[j + 1] = key; // Insertamos finalmente el valor de la variable key.
    }
}

// ====================================================================================================
// 3. MERGE SORT (Ordenamiento por Mezcla)
// ====================================================================================================
void merge(int* arr, int left, int mid, int right, long long* comps, long long* swaps) {
    int n1 = mid - left + 1;
    int n2 = right - mid;

    // Memoria dinámica para sub-arreglos temporales
    int* L = new int[n1]; 
    int* R = new int[n2]; 

    for (int i = 0; i < n1; i++) L[i] = arr[left + i];
    for (int j = 0; j < n2; j++) R[j] = arr[mid + 1 + j];

    int i = 0; 
    int j = 0; 
    int k = left; 

    // Mezclamos arreglos
    while (i < n1 && j < n2) {
        (*comps)++; // Comparación al decidir de qué sub-arreglo sacar el número.
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        } else {
            arr[k] = R[j];
            j++;
        }
        (*swaps)++; // Mover un dato de un sub-arreglo al arreglo principal se cuenta como un movimiento de datos.
        k++; 
    }

    // Copiamos los restantes (son simples movimientos de datos)
    while (i < n1) {
        arr[k] = L[i];
        (*swaps)++;
        i++;
        k++;
    }
    while (j < n2) {
        arr[k] = R[j];
        (*swaps)++;
        j++;
        k++;
    }

    // Liberamos la memoria dinámica (CRÍTICO)
    delete[] L;
    delete[] R;
}

void mergeSort(int* arr, int left, int right, long long* comps, long long* swaps) {
    if (left >= right) return; 

    int mid = left + (right - left) / 2; 

    // Propagamos los punteros de contadores a las llamadas recursivas
    mergeSort(arr, left, mid, comps, swaps);       
    mergeSort(arr, mid + 1, right, comps, swaps);  

    merge(arr, left, mid, right, comps, swaps); 
}

// ====================================================================================================
// 4. QUICK SORT (Ordenamiento Rápido)
// ====================================================================================================
int partition(int* arr, int low, int high, long long* comps, long long* swaps) {
    int pivot = arr[high]; // Pivote en la última posición
    int i = (low - 1);     

    for (int j = low; j <= high - 1; j++) {
        (*comps)++; // Contamos la comparación contra el pivote
        if (arr[j] <= pivot) {
            i++; 
            (*swaps)++; // Ocurre un intercambio
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }
    (*swaps)++; // Intercambio final del pivote a su posición correcta
    int temp = arr[i + 1];
    arr[i + 1] = arr[high];
    arr[high] = temp;
    
    return (i + 1); 
}

void quickSort(int* arr, int low, int high, long long* comps, long long* swaps) {
    if (low < high) {
        int pi = partition(arr, low, high, comps, swaps); 

        quickSort(arr, low, pi - 1, comps, swaps); 
        quickSort(arr, pi + 1, high, comps, swaps); 
    }
}

// ====================================================================================================
// FUNCIONES AUXILIARES PARA COPIAR ARREGLOS Y MEDIR TIEMPO
// ====================================================================================================
// Copia memoria de un origen a un destino usando la aritmética base de punteros a arreglos.
void copyArray(int* source, int* dest, int n) {
    for (int i = 0; i < n; i++) {
        dest[i] = source[i];
    }
}

// ====================================================================================================
// FUNCIÓN PRINCIPAL (MAIN)
// ====================================================================================================
int main() {
    // Definimos el tamaño de la estructura de datos: 1000 elementos.
    const int SIZE = 1000; 

    // Asignación de memoria dinámica usando 'new'. Devuelve un puntero al inicio del bloque de memoria.
    int* originalRandom = new int[SIZE];
    int* originalSorted = new int[SIZE];
    int* originalReverse = new int[SIZE];

    // Configuración para la generación de números aleatorios usando <random>
    random_device rd; 
    mt19937 gen(rd()); 
    uniform_int_distribution<> distrib(1, 10000); // Números entre 1 y 10,000

    // 1. Generar Arreglo Aleatorio
    for (int i = 0; i < SIZE; i++) {
        originalRandom[i] = distrib(gen); 
    }

    // 2. Generar Arreglo Ordenado
    copyArray(originalRandom, originalSorted, SIZE);
    sort(originalSorted, originalSorted + SIZE); // punteros inicio y fin de la memoria

    // 3. Generar Arreglo Inverso
    copyArray(originalSorted, originalReverse, SIZE);
    reverse(originalReverse, originalReverse + SIZE); // punteros inicio y fin de la memoria

    // Arreglo temporal
    int* testArray = new int[SIZE]; 

    // Cadenas y punteros en un arreglo para poder iterar en el ciclo for
    string names[] = {"Aleatorio", "Ordenado", "Inverso"};
    int* sources[] = {originalRandom, originalSorted, originalReverse};

    // Variables base para almacenar comparaciones e intercambios
    long long comps = 0, swaps = 0;

    // Bucle para iterar a través de los tres escenarios
    for (int caso = 0; caso < 3; caso++) {
        cout << "\n======================================================================================\n";
        cout << "Evaluando arreglo: " << names[caso] << " (" << SIZE << " elementos)" << endl;
        cout << "======================================================================================\n";

        // ---- Medir Bubble Sort ----
        copyArray(sources[caso], testArray, SIZE);
        comps = 0; swaps = 0; // Reinicio de contadores
        auto start = chrono::high_resolution_clock::now(); 
        // Pasamos '&comps' y '&swaps' para entregar las direcciones de memoria de nuestras variables
        bubbleSort(testArray, SIZE, &comps, &swaps); 
        auto end = chrono::high_resolution_clock::now(); 
        auto duration = chrono::duration_cast<chrono::microseconds>(end - start); 
        cout << "Bubble Sort:\tTiempo: " << duration.count() << " us \t| Comps: " << comps << " \t| Movs/Intercambios: " << swaps << "\n";

        // ---- Medir Insertion Sort ----
        copyArray(sources[caso], testArray, SIZE);
        comps = 0; swaps = 0;
        start = chrono::high_resolution_clock::now();
        insertionSort(testArray, SIZE, &comps, &swaps);
        end = chrono::high_resolution_clock::now();
        duration = chrono::duration_cast<chrono::microseconds>(end - start);
        cout << "Insertion Sort:\tTiempo: " << duration.count() << " us \t| Comps: " << comps << " \t| Movs/Intercambios: " << swaps << "\n";

        // ---- Medir Merge Sort ----
        copyArray(sources[caso], testArray, SIZE);
        comps = 0; swaps = 0;
        start = chrono::high_resolution_clock::now();
        mergeSort(testArray, 0, SIZE - 1, &comps, &swaps);
        end = chrono::high_resolution_clock::now();
        duration = chrono::duration_cast<chrono::microseconds>(end - start);
        cout << "Merge Sort:\tTiempo: " << duration.count() << " us \t| Comps: " << comps << " \t| Movs/Intercambios: " << swaps << "\n";

        // ---- Medir Quick Sort ----
        copyArray(sources[caso], testArray, SIZE);
        comps = 0; swaps = 0;
        start = chrono::high_resolution_clock::now();
        quickSort(testArray, 0, SIZE - 1, &comps, &swaps);
        end = chrono::high_resolution_clock::now();
        duration = chrono::duration_cast<chrono::microseconds>(end - start);
        cout << "Quick Sort:\tTiempo: " << duration.count() << " us \t| Comps: " << comps << " \t| Movs/Intercambios: " << swaps << "\n";
    }

    // MUY IMPORTANTE: Liberar la memoria dinámica de todos los arreglos utilizados.
    delete[] originalRandom;
    delete[] originalSorted;
    delete[] originalReverse;
    delete[] testArray;

    return 0; 
}

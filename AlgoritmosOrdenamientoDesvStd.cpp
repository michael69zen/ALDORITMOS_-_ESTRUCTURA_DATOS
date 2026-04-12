#include <iostream>
#include <vector>
#include <chrono>
#include <random>
#include <algorithm>
#include <cmath>

using namespace std;
using Clock = chrono::high_resolution_clock;

// ======================= SORTS =======================
void bubbleSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; i++) {
        bool swapped = false;
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
                swapped = true;
            }
        }
        if (!swapped) break;
    }
}

void selectionSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; i++) {
        int minIdx = i;
        for (int j = i + 1; j < n; j++)
            if (arr[j] < arr[minIdx]) minIdx = j;
        swap(arr[i], arr[minIdx]);
    }
}

void insertionSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 1; i < n; i++) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}

void shellSort(vector<int>& arr) {
    int n = arr.size();
    for (int gap = n / 2; gap > 0; gap /= 2) {
        for (int i = gap; i < n; i++) {
            int temp = arr[i];
            int j;
            for (j = i; j >= gap && arr[j - gap] > temp; j -= gap)
                arr[j] = arr[j - gap];
            arr[j] = temp;
        }
    }
}

// ======================= VALIDACIÓN =======================
bool isSorted(const vector<int>& arr) {
    for (size_t i = 1; i < arr.size(); i++)
        if (arr[i] < arr[i - 1]) return false;
    return true;
}

// ======================= BENCHMARK =======================
void benchmark(
    const vector<int>& data,
    void(*func)(vector<int>&),
    const string& name,
    int repetitions = 10
) {
    vector<long long> times;

    // Warm-up (no se mide)
    {
        auto temp = data;
        func(temp);
    }

    for (int i = 0; i < repetitions; i++) {
        auto arr = data;

        auto t1 = Clock::now();
        func(arr);
        auto t2 = Clock::now();

        // Validación
        if (!isSorted(arr)) {
            cout << name << " ERROR: no ordena correctamente\n";
            return;
        }

        auto duration = chrono::duration_cast<chrono::microseconds>(t2 - t1).count();
        times.push_back(duration);
    }

    // Promedio
    double sum = 0;
    for (auto t : times) sum += t;
    double mean = sum / repetitions;

    // Desviación estándar
    double variance = 0;
    for (auto t : times)
        variance += (t - mean) * (t - mean);
    variance /= repetitions;
    double stddev = sqrt(variance);

    cout << name
         << " -> mean: " << mean
         << " μs | stddev: " << stddev << "\n";
}

// ======================= MAIN =======================
int main() {

    vector<int> sizes = {10, 100, 1000};

    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dist(0, 100000);

    for (int n : sizes) {

        vector<int> data(n);
        for (int i = 0; i < n; i++)
            data[i] = dist(gen);

        cout << "\n****** Size: " << n << " ******\n";

        benchmark(data, bubbleSort, "Bubble Sort");
        benchmark(data, selectionSort, "Selection Sort");
        benchmark(data, insertionSort, "Insertion Sort");
        benchmark(data, shellSort, "Shell Sort");
    }

    return 0;
}

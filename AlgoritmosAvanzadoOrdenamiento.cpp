#include <iostream>
#include <vector>
#include <chrono>
#include <algorithm>
#include <random>
#include <iomanip>

using namespace std;
using Clock = chrono::high_resolution_clock;

// 1. QUICK SORT

int partition(vector<int>& arr, int low, int high) {
    int mid = low + (high - low) / 2;
    swap(arr[mid], arr[high]);
    int pivot = arr[high];
    
    int i = (low - 1);
    for (int j = low; j <= high - 1; j++) {
        if (arr[j] < pivot) {
            i++;
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[high]);
    return (i + 1);
}

void quickSortHelper(vector<int>& arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quickSortHelper(arr, low, pi - 1);
        quickSortHelper(arr, pi + 1, high);
    }
}

void quickSort(vector<int>& arr) {
    if(!arr.empty()) quickSortHelper(arr, 0, arr.size() - 1);
}


// 2. MERGE SORT

void merge(vector<int>& arr, int l, int m, int r) {
    int n1 = m - l + 1;
    int n2 = r - m;
    vector<int> L(n1), R(n2);
    
    for(int i = 0; i < n1; i++) L[i] = arr[l + i];
    for(int j = 0; j < n2; j++) R[j] = arr[m + 1 + j];
    
    int i = 0, j = 0, k = l;
    while(i < n1 && j < n2) {
        if(L[i] <= R[j]) arr[k++] = L[i++];
        else arr[k++] = R[j++];
    }
    while(i < n1) arr[k++] = L[i++];
    while(j < n2) arr[k++] = R[j++];
}

void mergeSortHelper(vector<int>& arr, int l, int r) {
    if(l >= r) return;
    int m = l + (r - l) / 2;
    mergeSortHelper(arr, l, m);
    mergeSortHelper(arr, m + 1, r);
    merge(arr, l, m, r);
}

void mergeSort(vector<int>& arr) {
    if(!arr.empty()) mergeSortHelper(arr, 0, arr.size() - 1);
}


// 3. TIM SORT (Híbrido Merge + Insertion)

const int RUN = 32;

void insertionSortTim(vector<int>& arr, int left, int right) {
    for (int i = left + 1; i <= right; i++) {
        int temp = arr[i];
        int j = i - 1;
        while (j >= left && arr[j] > temp) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = temp;
    }
}

void timSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n; i += RUN)
        insertionSortTim(arr, i, min(i + RUN - 1, n - 1));
        
    for (int size = RUN; size < n; size = 2 * size) {
        for (int left = 0; left < n; left += 2 * size) {
            int mid = left + size - 1;
            int right = min((left + 2 * size - 1), (n - 1));
            if(mid < right)
                merge(arr, left, mid, right);
        }
    }
}


// 4. COUNTING SORT

void countingSort(vector<int>& arr) {
    if(arr.empty()) return;
    int max_val = *max_element(arr.begin(), arr.end());
    int min_val = *min_element(arr.begin(), arr.end());
    int range = max_val - min_val + 1;
    
    vector<int> count(range, 0), output(arr.size());
    for (int i = 0; i < arr.size(); i++) 
        count[arr[i] - min_val]++;
        
    for (int i = 1; i < count.size(); i++) 
        count[i] += count[i - 1];
        
    for (int i = arr.size() - 1; i >= 0; i--) {
        output[count[arr[i] - min_val] - 1] = arr[i];
        count[arr[i] - min_val]--;
    }
    
    for (int i = 0; i < arr.size(); i++) 
        arr[i] = output[i];
}


// 5. RADIX SORT

void countSortForRadix(vector<int>& arr, int exp) {
    int n = arr.size();
    vector<int> output(n);
    int count[10] = {0};
    
    for (int i = 0; i < n; i++) count[(arr[i] / exp) % 10]++;
    for (int i = 1; i < 10; i++) count[i] += count[i - 1];
    for (int i = n - 1; i >= 0; i--) {
        output[count[(arr[i] / exp) % 10] - 1] = arr[i];
        count[(arr[i] / exp) % 10]--;
    }
    for (int i = 0; i < n; i++) arr[i] = output[i];
}

void radixSort(vector<int>& arr) {
    if(arr.empty()) return;
    int m = *max_element(arr.begin(), arr.end());
    for (int exp = 1; m / exp > 0; exp *= 10)
        countSortForRadix(arr, exp);
}


// 6. BUCKET SORT

void bucketSort(vector<int>& arr) {
    if(arr.empty()) return;
    int max_val = *max_element(arr.begin(), arr.end());
    int min_val = *min_element(arr.begin(), arr.end());
    
    int bucket_count = arr.size(); 
    vector<vector<int>> buckets(bucket_count);
    
    double range = (double)(max_val - min_val + 1) / bucket_count;
    
    for(int i = 0; i < arr.size(); i++) {
        int b_idx = (arr[i] - min_val) / range;
        if(b_idx >= bucket_count) b_idx = bucket_count - 1;
        buckets[b_idx].push_back(arr[i]);
    }
    
    int idx = 0;
    for(int i = 0; i < bucket_count; i++) {
        sort(buckets[i].begin(), buckets[i].end()); 
        for(int j = 0; j < buckets[i].size(); j++) {
            arr[idx++] = buckets[i][j];
        }
    }
}


// Analisis de complejidad temporal
void test(const vector<int>& data, void(*func)(vector<int>&), const string& name) {
    vector<int> arr = data; 

    auto t1 = Clock::now();
    func(arr);
    auto t2 = Clock::now();

    cout << left << setw(18) << name << " tomó " 
         << right << setw(10) << chrono::duration_cast<chrono::microseconds>(t2 - t1).count() 
         << " μs\n";
}

int main() {
    vector<int> sizes = {10000, 100000, 1000000};
    
    random_device rd;
    mt19937 gen(42); // Semilla fija para reproducibilidad
    uniform_int_distribution<> dis(1, 10000000); 

    for (int n : sizes) {
        vector<int> data(n);
        for (int i = 0; i < n; i++) data[i] = dis(gen);

        cout << "\n============================================\n";
        cout << "****** Probando con N = " << n << " elementos ******\n";
        cout << "============================================\n";

        test(data, quickSort,     "Quick Sort");
        test(data, mergeSort,     "Merge Sort");
        test(data, timSort,       "Tim Sort");
        test(data, radixSort,     "Radix Sort");
        test(data, bucketSort,    "Bucket Sort");
        test(data, countingSort,  "Counting Sort");
    }

    return 0;
}

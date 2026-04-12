#include <iostream>
#include <vector>
#include <chrono>

using namespace std;

using Clock = chrono::high_resolution_clock;

void bubbleSort(vector<int>& arr) {
    int n = arr.size();
    bool swapped;

    for (int i = 0; i < n - 1; i++) {
        swapped = false;

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

        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[minIdx])
                minIdx = j;
        }

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

void test(vector<int> data, void(*func)(vector<int>&), const string& name) {

    auto arr = data;

    auto t1 = Clock::now();

    func(arr);

    auto t2 = Clock::now();

    cout << name << " took "
         << chrono::duration_cast<chrono::microseconds>(t2 - t1).count()
         << " μs\n";
}

int main() {

    vector<int> sizes = {10, 100, 1000};

    for (int n : sizes) {

        vector<int> data(n);

        for (int i = 0; i < n; i++)
            data[i] = rand();

        cout << "****** Size: " << n << " ******\n";

        test(data, bubbleSort, "Bubble Sort");
        test(data, selectionSort, "Selection Sort");
        test(data, insertionSort, "Insertion Sort");
        test(data, shellSort, "Shell Sort");
    }

    return 0;
}

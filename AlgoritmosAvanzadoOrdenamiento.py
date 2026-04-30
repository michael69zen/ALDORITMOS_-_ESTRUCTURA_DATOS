import time
import random
import sys

# Aumentar el límite de recursión por seguridad con arreglos gigantes
sys.setrecursionlimit(2000000)


# 1. QUICK SORT

def partition(arr, low, high):
    mid = low + (high - low) // 2
    # Intercambiamos el medio con el final para usarlo como pivote
    arr[mid], arr[high] = arr[high], arr[mid]
    pivot = arr[high]
    
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quick_sort_helper(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quick_sort_helper(arr, low, pi - 1)
        quick_sort_helper(arr, pi + 1, high)

def quick_sort(arr):
    if arr:
        quick_sort_helper(arr, 0, len(arr) - 1)


# 2. MERGE SORT

def merge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m
    
    L = arr[l : l + n1]
    R = arr[m + 1 : m + 1 + n2]
    
    i = 0
    j = 0
    k = l
    
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
        
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
        
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

def merge_sort_helper(arr, l, r):
    if l < r:
        m = l + (r - l) // 2
        merge_sort_helper(arr, l, m)
        merge_sort_helper(arr, m + 1, r)
        merge(arr, l, m, r)

def merge_sort(arr):
    if arr:
        merge_sort_helper(arr, 0, len(arr) - 1)


# 3. TIM SORT (Híbrido)

RUN = 32

def insertion_sort_tim(arr, left, right):
    for i in range(left + 1, right + 1):
        temp = arr[i]
        j = i - 1
        while j >= left and arr[j] > temp:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = temp

def tim_sort(arr):
    n = len(arr)
    for i in range(0, n, RUN):
        insertion_sort_tim(arr, i, min(i + RUN - 1, n - 1))
        
    size = RUN
    while size < n:
        for left in range(0, n, 2 * size):
            mid = left + size - 1
            right = min((left + 2 * size - 1), (n - 1))
            if mid < right:
                merge(arr, left, mid, right)
        size *= 2


# 4. COUNTING SORT

def counting_sort(arr):
    if not arr:
        return
        
    max_val = max(arr)
    min_val = min(arr)
    rango = max_val - min_val + 1
    
    count = [0] * rango
    output = [0] * len(arr)
    
    for i in range(len(arr)):
        count[arr[i] - min_val] += 1
        
    for i in range(1, len(count)):
        count[i] += count[i - 1]
        
    for i in range(len(arr) - 1, -1, -1):
        output[count[arr[i] - min_val] - 1] = arr[i]
        count[arr[i] - min_val] -= 1
        
    for i in range(len(arr)):
        arr[i] = output[i]


# 5. RADIX SORT

def count_sort_for_radix(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    
    for i in range(n):
        index = arr[i] // exp
        count[index % 10] += 1
        
    for i in range(1, 10):
        count[i] += count[i - 1]
        
    i = n - 1
    while i >= 0:
        index = arr[i] // exp
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1
        
    for i in range(n):
        arr[i] = output[i]

def radix_sort(arr):
    if not arr:
        return
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        count_sort_for_radix(arr, exp)
        exp *= 10


# 6. BUCKET SORT

def bucket_sort(arr):
    if not arr:
        return
        
    max_val = max(arr)
    min_val = min(arr)
    
    bucket_count = len(arr)
    buckets = [[] for _ in range(bucket_count)]
    
    if max_val == min_val:
        return
        
    rango = (max_val - min_val + 1) / bucket_count
    
    for i in range(len(arr)):
        b_idx = int((arr[i] - min_val) / rango)
        if b_idx >= bucket_count:
            b_idx = bucket_count - 1
        buckets[b_idx].append(arr[i])
        
    idx = 0
    for i in range(bucket_count):
        # Ordenamos los sub-buckets (equivalente al std::sort en C++)
        buckets[i].sort()
        for j in range(len(buckets[i])):
            arr[idx] = buckets[i][j]
            idx += 1


# Analisis temporal

def test(data, func, name):
    # Hacemos una copia para no ordenar los datos originales
    arr = data.copy()
    
    t1 = time.perf_counter()
    func(arr)
    t2 = time.perf_counter()
    
    # Calcular duración en microsegundos y formatear
    duracion_us = int((t2 - t1) * 1_000_000)
    print(f"{name:<18} tomó {duracion_us:>10} μs")

def main():
    sizes = [10000, 100000, 1000000]
    
    # Semilla para que las pruebas sean predecibles (igual al mt19937)
    random.seed(42)
    
    for n in sizes:
        # Llenar la lista con N números aleatorios grandes (de 1 a 10 Millones)
        data = [random.randint(1, 10000000) for _ in range(n)]

        print("\n============================================")
        print(f"****** Probando con N = {n} elementos ******")
        print("============================================")

        test(data, quick_sort,     "Quick Sort")
        test(data, merge_sort,     "Merge Sort")
        test(data, tim_sort,       "Tim Sort")
        test(data, radix_sort,     "Radix Sort")
        test(data, bucket_sort,    "Bucket Sort")
        test(data, counting_sort,  "Counting Sort")

if __name__ == "__main__":
    main()

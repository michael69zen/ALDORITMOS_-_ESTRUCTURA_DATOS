import time
import matplotlib.pyplot as plt

def suma_lineal(n):
    suma = 0
    for i in range(1, n + 1):
        suma += i
    return suma

def suma_constante(n):
    return (n * (n + 1)) // 2

# Valores de N para la prueba
valores = [1000, 10000, 100000, 500000, 1000000]
tiempos_n = []
tiempos_1 = []

for n in valores:
    print(f"Procesando N = {n}...")
    
    # Medir O(n)
    inicio = time.perf_counter_ns()
    suma_lineal(n)
    fin = time.perf_counter_ns()
    tiempos_n.append(fin - inicio)
    
    # Medir O(1)
    inicio = time.perf_counter_ns()
    suma_constante(n)
    fin = time.perf_counter_ns()
    tiempos_1.append(fin - inicio)

# --- Configuración de la Gráfica ---
plt.figure(figsize=(10, 6))

# Graficar ambas líneas
plt.plot(valores, tiempos_n, marker='o', linestyle='-', color='red', label='O(n) - Bucle For')
plt.plot(valores, tiempos_1, marker='s', linestyle='--', color='blue', label='O(1) - Fórmula Gauss')

# Formatear la gráfica
plt.title('Comparación de Complejidad Temporal: Suma de N Números', fontsize=14)
plt.xlabel('Valor de N (Tamaño de la entrada)', fontsize=12)
plt.ylabel('Tiempo de Ejecución (Nanosegundos)', fontsize=12)
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)

# Mostrar anotaciones para resaltar la diferencia
plt.annotate(f'O(n) aumenta linealmente', xy=(valores[-1], tiempos_n[-1]), 
             xytext=(valores[-1]*0.7, tiempos_n[-1]*0.8),
             arrowprops=dict(arrowstyle='->', color='red'))

plt.annotate(f'O(1) se mantiene constante', xy=(valores[-1], tiempos_1[-1]), 
             xytext=(valores[-1]*0.6, tiempos_n[-1]*0.1),
             arrowprops=dict(arrowstyle='->', color='blue'))

plt.tight_layout()
plt.show()

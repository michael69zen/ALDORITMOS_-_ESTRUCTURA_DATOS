import time

# Implementación O(n) - Bucle
def suma_lineal(n):
    suma = 0
    for i in range(1, n + 1):
        suma += i
    return suma

# Implementación O(1) - Fórmula
def suma_constante(n):
    return (n * (n + 1)) // 2

def medir_tiempo(funcion, n):
    inicio = time.perf_counter_ns()
    resultado = funcion(n)
    fin = time.perf_counter_ns()
    duracion = fin - inicio
    return resultado, duracion

def main():
    valores = [1000, 10000, 100000, 1000000]

    for n in valores:
        print(f"--- N = {n} ---")

        # Medir O(n)
        res_n, dur_n = medir_tiempo(suma_lineal, n)

        # Medir O(1)
        res_1, dur_1 = medir_tiempo(suma_constante, n)

        print(f"O(n) Tiempo: {dur_n} ns | Resultado: {res_n}")
        print(f"O(1) Tiempo: {dur_1} ns | Resultado: {res_1}")
        print()

if __name__ == "__main__":
    main()

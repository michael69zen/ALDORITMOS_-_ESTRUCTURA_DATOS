def quicksort(lista):
    if len(lista) <= 1:
        return lista
    
    pivote = lista[0]  # elegimos el primer elemento como pivote
    menores = [x for x in lista[1:] if x < pivote]
    iguales = [x for x in lista if x == pivote]
    mayores = [x for x in lista[1:] if x > pivote]
    
    return quicksort(menores) + iguales + quicksort(mayores)


# Lista de 9 elementos desordenados
numeros = [6, 3, 8, 1, 9, 4, 2, 7, 5]

print("Lista original:", numeros)
ordenada = quicksort(numeros)
print("Lista ordenada:", ordenada)

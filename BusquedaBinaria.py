def busqueda_binaria(lista, objetivo):
    izquierda = 0
    derecha = len(lista) - 1
    
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        valor_medio = lista[medio]
        
        if valor_medio == objetivo:
            return medio    # retorna el índice donde se encontró
        elif valor_medio < objetivo:
            izquierda = medio + 1   # buscar en la mitad derecha
        else:
            derecha = medio - 1     # buscar en la mitad izquierda
    
    return -1   # no se encontró el elemento


# Lista ordenada de 9 elementos
numeros = [1, 3, 5, 7, 9, 11, 13, 15, 17]

# Número a buscar
buscado = 9

# Llamar a la función
indice = busqueda_binaria(numeros, buscado)

if indice != -1:
    print(f"El número {buscado} se encuentra en la posición {indice}.")
else:
    print(f"El número {buscado} no se encuentra en la lista.")

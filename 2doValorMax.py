def buscar_segundo_mas_alto(numeros):
    # Verificar que el arreglo tenga suficientes elementos
    if len(numeros) < 2:
        return "El arreglo debe tener al menos dos elementos."

    # Inicializar con el valor más bajo posible
    maximo = float('-inf')
    segundo_maximo = float('-inf')

    for n in numeros:
        # Caso 1: Encontramos un nuevo máximo
        if n > maximo:
            segundo_maximo = maximo # El anterior máximo baja a segundo lugar
            maximo = n              # Actualizamos el máximo
        
        # Caso 2: Es mayor que el segundo pero menor que el máximo
        # El 'and n != maximo' evita duplicados si el máximo se repite
        elif n > segundo_maximo and n != maximo:
            segundo_maximo = n

    # Verificar si se encontró un segundo valor distinto
    if segundo_maximo == float('-inf'):
        return "No se encontró un segundo valor distinto al máximo."
    
    return maximo, segundo_maximo

# Ejemplo de uso
try:
    entrada = input("Ingrese los números separados por espacios: ")
    # Convertir la entrada de texto a una lista de enteros
    lista_numeros = [int(x) for x in entrada.split()]
    
    resultados = buscar_segundo_mas_alto(lista_numeros)
    
    if isinstance(resultados, tuple):
        max_val, segundo_val = resultados
        print(f"El valor máximo es: {max_val}")
        print(f"El segundo valor más alto es: {segundo_val}")
    else:
        print(resultados)
        
except ValueError:
    print("Error: Por favor, ingrese solo números enteros.")

def es_palindromo(cadena):
    # 1. Calcular la longitud manualmente
    longitud = 0
    for caracter in cadena:
        longitud += 1
    
    # 2. Comparar desde los extremos hacia el centro
    inicio = 0
    fin = longitud - 1
    
    while inicio < fin:
        # Si encontramos una diferencia, no es palíndromo
        if cadena[inicio] != cadena[fin]:
            return False
        
        inicio += 1
        fin -= 1
        
    return True

# Prueba del algoritmo
palabra = input("Ingrese una palabra o frase: ")

# Limpieza básica para ignorar espacios y mayúsculas (opcional)
# palabra = palabra.replace(" ", "").lower() 

if es_palindromo(palabra):
    print("Es un palíndromo.")
else:
    print("No es un palíndromo.")

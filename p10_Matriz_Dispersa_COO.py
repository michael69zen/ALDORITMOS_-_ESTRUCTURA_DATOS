# Definición de la clase SparseMatrix (Matriz Dispersa)
class SparseMatrix:

    # Constructor de la clase
    def __init__(self, rows, cols):

        # Número de filas de la matriz
        self.rows = rows

        # Número de columnas de la matriz
        self.cols = cols

        # Diccionario donde se almacenan únicamente
        # los elementos diferentes de cero.
        # La clave será una tupla (fila, columna)
        # y el valor será el elemento almacenado.
        self.data = {}

    # Método para agregar un elemento a la matriz
    def add(self, r, c, val):

        # Solo se almacenan los valores distintos de cero
        if val != 0:

            # Guarda el valor usando como clave
            # la posición (fila, columna)
            self.data[(r, c)] = val

    # Método para obtener el valor de una posición
    def get(self, r, c):

        # Busca la posición (r,c) en el diccionario.
        # Si existe, devuelve el valor almacenado.
        # Si no existe, devuelve 0.
        return self.data.get((r, c), 0)

    # Método para mostrar la matriz completa
    def display(self):

        # Recorre todas las filas
        for r in range(self.rows):

            # Lista temporal donde se almacenarán
            # los valores de la fila actual
            row = []

            # Recorre todas las columnas
            for c in range(self.cols):

                # Obtiene el valor de la posición (r,c)
                # y lo convierte en cadena de texto
                row.append(str(self.get(r, c)))

            # Une todos los elementos de la fila
            # separados por espacios y los imprime
            print(" ".join(row))


# ==========================
# Programa principal
# ==========================

# Se crea una matriz dispersa de 4 filas y 4 columnas
A = SparseMatrix(4, 4)

# Se agrega el valor 5 en la posición (0,1)
A.add(0, 1, 5)

# Se agrega el valor 8 en la posición (1,3)
A.add(1, 3, 8)

# Se agrega el valor 3 en la posición (2,2)
A.add(2, 2, 3)

# Se muestra la matriz completa
A.display()

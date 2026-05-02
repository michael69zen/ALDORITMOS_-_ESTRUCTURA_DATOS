import pandas as pd
import time
import matplotlib.pyplot as plt

class HashTableChaining:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.collisions = 0

    def hash_function(self, key):
        return hash(str(key)) % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        if len(self.table[index]) > 0:
            # Simplificación para conteo visual: si ya hay elementos, contamos colisión
            self.collisions += 1
        self.table[index].append((key, value))

    def search(self, key):
        index = self.hash_function(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None

    def load_factor(self, total_elements):
        return total_elements / self.size


class HashTableLinearProbing:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size
        self.collisions = 0

    def hash_function(self, key):
        return hash(str(key)) % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        while self.table[index] is not None:
            self.collisions += 1
            index = (index + 1) % self.size
        self.table[index] = (key, value)

    def search(self, key):
        index = self.hash_function(key)
        start = index
        while self.table[index] is not None:
            if self.table[index][0] == key:
                return self.table[index][1]
            index = (index + 1) % self.size
            if index == start:
                break
        return None

    def load_factor(self, total_elements):
        return total_elements / self.size


class HashTableQuadraticProbing:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size
        self.collisions = 0

    def hash_function(self, key):
        return hash(str(key)) % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        i = 0
        # h(k, i) = (h'(k) + i^2) mod m
        while self.table[(index + i**2) % self.size] is not None:
            self.collisions += 1
            i += 1
            if i == self.size:
                # Evitar bucles infinitos si no encuentra hueco
                raise Exception("La tabla hash está llena o no se puede resolver la colisión")
        
        self.table[(index + i**2) % self.size] = (key, value)

    def search(self, key):
        index = self.hash_function(key)
        i = 0
        while self.table[(index + i**2) % self.size] is not None:
            if self.table[(index + i**2) % self.size][0] == key:
                return self.table[(index + i**2) % self.size][1]
            i += 1
            if i == self.size:
                break
        return None

    def load_factor(self, total_elements):
        return total_elements / self.size


class HashTableDoubleHashing:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size
        self.collisions = 0
        # Elegimos un número primo menor al tamaño de la tabla para el segundo hash
        self.prime = 19997 

    def hash_function1(self, key):
        return hash(str(key)) % self.size

    def hash_function2(self, key):
        # h2(k) = PRIME - (hash(k) % PRIME)
        # Esto asegura que nunca devuelva 0 (lo cual causaría un bucle infinito)
        return self.prime - (hash(str(key)) % self.prime)

    def insert(self, key, value):
        index = self.hash_function1(key)
        step_size = self.hash_function2(key)
        i = 0
        
        # h(k, i) = (h1(k) + i * h2(k)) mod m
        while self.table[(index + i * step_size) % self.size] is not None:
            self.collisions += 1
            i += 1
            if i == self.size:
                raise Exception("La tabla hash está llena")
                
        self.table[(index + i * step_size) % self.size] = (key, value)

    def search(self, key):
        index = self.hash_function1(key)
        step_size = self.hash_function2(key)
        i = 0
        
        while self.table[(index + i * step_size) % self.size] is not None:
            if self.table[(index + i * step_size) % self.size][0] == key:
                return self.table[(index + i * step_size) % self.size][1]
            i += 1
            if i == self.size:
                break
        return None

    def load_factor(self, total_elements):
        return total_elements / self.size


# ---------------- PREPARACIÓN DE DATOS ----------------
# Cargar dataset descargado desde Kaggle.
df = pd.read_csv("events.csv")

# Limpieza básica enfocada en las columnas que nos interesan
df = df.dropna(subset=["user_session", "category_id", "price"])

# Tomamos las primeras 10000 filas
df_subset = df.head(10000)

# Preparar las listas de datos (Clave = user_session, Valor = [category_id, price])
data = []
for _, row in df_subset.iterrows():
    key = str(row["user_session"])
    value = [row["category_id"], row["price"]]
    data.append((key, value))

n_elements = len(data)
table_size = 20011 # Es un número primo, ideal para tablas Hash

# Lista de claves solo para la prueba de búsqueda (primeras 1000)
search_keys = [item[0] for item in data[:1000]]


# ---------------- PRUEBAS DE RENDIMIENTO ----------------

# 1. Prueba con Encadenamiento
hash_chain = HashTableChaining(table_size)
start_time = time.time()
for key, value in data:
    hash_chain.insert(key, value)
insert_time_chain = time.time() - start_time

start_time = time.time()
for key in search_keys:
    hash_chain.search(key)
search_time_chain = time.time() - start_time

# 2. Prueba con Sondeo Lineal
hash_linear = HashTableLinearProbing(table_size)
start_time = time.time()
for key, value in data:
    hash_linear.insert(key, value)
insert_time_linear = time.time() - start_time

start_time = time.time()
for key in search_keys:
    hash_linear.search(key)
search_time_linear = time.time() - start_time

# 3. Prueba con Sondeo Cuadrático
hash_quadratic = HashTableQuadraticProbing(table_size)
start_time = time.time()
for key, value in data:
    hash_quadratic.insert(key, value)
insert_time_quadratic = time.time() - start_time

start_time = time.time()
for key in search_keys:
    hash_quadratic.search(key)
search_time_quadratic = time.time() - start_time

# 4. Prueba con Doble Hashing
hash_double = HashTableDoubleHashing(table_size)
start_time = time.time()
for key, value in data:
    hash_double.insert(key, value)
insert_time_double = time.time() - start_time

start_time = time.time()
for key in search_keys:
    hash_double.search(key)
search_time_double = time.time() - start_time

# 5. Comparación con Diccionario Nativo de Python
native_dict = {}
start_time = time.time()
for key, value in data:
    native_dict[key] = value
insert_time_dict = time.time() - start_time

start_time = time.time()
for key in search_keys:
    native_dict.get(key)
search_time_dict = time.time() - start_time


# ---------------- RESULTADOS ----------------

# Tabla comparativa de resultados.
results = pd.DataFrame({
    "Método": [
        "Encadenamiento", 
        "Sondeo lineal", 
        "Sondeo cuadrático", 
        "Doble Hashing", 
        "Diccionario Python"
    ],
    "Tiempo inserción": [
        insert_time_chain, 
        insert_time_linear, 
        insert_time_quadratic, 
        insert_time_double, 
        insert_time_dict
    ],
    "Tiempo búsqueda": [
        search_time_chain, 
        search_time_linear, 
        search_time_quadratic, 
        search_time_double, 
        search_time_dict
    ],
    "Colisiones": [
        hash_chain.collisions, 
        hash_linear.collisions, 
        hash_quadratic.collisions, 
        hash_double.collisions, 
        0 # Python maneja colisiones internamente en C
    ],
    "Factor de carga": [
        hash_chain.load_factor(n_elements),
        hash_linear.load_factor(n_elements),
        hash_quadratic.load_factor(n_elements),
        hash_double.load_factor(n_elements),
        n_elements / table_size
    ]
})

print(results)

# ---------------- GRÁFICOS ----------------
metodos = results["Método"]
tiempos_insercion = results["Tiempo inserción"]
tiempos_busqueda = results["Tiempo búsqueda"]
colisiones = results["Colisiones"]

# 1. Gráfico de tiempo de inserción.
plt.figure(figsize=(10, 5))
plt.bar(metodos, tiempos_insercion, color='skyblue')
plt.title("Comparación de Tiempo de Inserción")
plt.xlabel("Método")
plt.ylabel("Tiempo en segundos")
plt.xticks(rotation=15)
plt.tight_layout()
plt.show()

# 2. Gráfico de tiempo de búsqueda.
plt.figure(figsize=(10, 5))
plt.bar(metodos, tiempos_busqueda, color='lightgreen')
plt.title("Comparación de Tiempo de Búsqueda")
plt.xlabel("Método")
plt.ylabel("Tiempo en segundos")
plt.xticks(rotation=15)
plt.tight_layout()
plt.show()

# 3. Gráfico de Colisiones (NUEVO)
plt.figure(figsize=(10, 5))
plt.bar(metodos, colisiones, color='salmon')
plt.title("Comparación de Colisiones por Método")
plt.xlabel("Método")
plt.ylabel("Cantidad de colisiones")
plt.xticks(rotation=15)
# Añadir los valores encima de las barras para mayor claridad
for i, v in enumerate(colisiones):
    plt.text(i, v + (max(colisiones)*0.01), str(v), ha='center', va='bottom', fontweight='bold')
plt.tight_layout()
plt.show()

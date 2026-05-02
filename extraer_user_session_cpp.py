import pandas as pd
import time
import matplotlib.pyplot as plt

# ... (código anterior)

# ---------------- PREPARACIÓN DE DATOS ----------------
# Cargar dataset descargado desde Kaggle.
df = pd.read_csv("events.csv")

# Limpieza básica enfocada en las columnas que nos interesan
df = df.dropna(subset=["user_session", "category_id", "price"])

# Tomamos las primeras 10000 filas
df_subset = df.head(10000)

# --> AÑADE ESTA LÍNEA <--
# Exportar la columna 'user_session' a un archivo de texto plano
df_subset["user_session"].to_csv("sessions_exportadas.txt", index=False, header=False)
print("¡Archivo sessions_exportadas.txt creado con éxito!")


# Preparar las listas de datos (Clave = user_session, Valor = [category_id, price])
# ... (resto de tu código Python)
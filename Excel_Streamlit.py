import streamlit as st
import pandas as pd
from collections import deque
import copy

# ============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================================
st.set_page_config(
    page_title="Academic Spreadsheet Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS para mejorar la estética visual
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# INICIALIZACIÓN DEL ESTADO GLOBAL (Equivalente al almacenamiento global de C++)
# ============================================================================
if 'hoja' not in st.session_state:
    st.session_state.hoja = []  # vector<Estudiante>
if 'indiceHash' not in st.session_state:
    st.session_state.indiceHash = {}  # unordered_map<string, int>
if 'historial' not in st.session_state:
    st.session_state.historial = []  # stack<vector<Estudiante>>
if 'colaAtencion' not in st.session_state:
    st.session_state.colaAtencion = deque()  # queue<string>

# ============================================================================
# FUNCIONES DE CORE LOGIC Y UTILIDAD
# ============================================================================

def calcular_promedio(n1, n2, n3):
    return round((n1 + n2 + n3) / 3.0, 2)

def actualizar_hash():
    st.session_state.indiceHash = {
        estudiante['codigo']: idx for idx, estudiante in enumerate(st.session_state.hoja)
    }

def guardar_historial():
    # Hacemos una copia profunda (deep copy) para evitar problemas de referencia en las listas de Python
    st.session_state.historial.append(copy.deepcopy(st.session_state.hoja))

# --- ALGORITMOS DE ORDENAMIENTO ---

# QuickSort Descendente por Promedio (Lomuto)
def particion_quicksort(arr, bajo, alto):
    pivote = arr[alto]['promedio']
    i = bajo - 1
    for j in range(bajo, alto):
        if arr[j]['promedio'] >= pivote: # >= para Descendente
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[alto] = arr[alto], arr[i + 1]
    return i + 1

def quicksort(arr, bajo, alto):
    if bajo < alto:
        pi = particion_quicksort(arr, bajo, alto)
        quicksort(arr, bajo, pi - 1)
        quicksort(arr, pi + 1, alto)

# MergeSort Ascendente por Código
def merge(arr, izq, medio, der):
    L = arr[izq:medio + 1]
    R = arr[medio + 1:der + 1]
    i = j = 0
    k = izq
    
    while i < len(L) and j < len(R):
        if L[i]['codigo'] <= R[j]['codigo']:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
        
    while i < len(L):
        arr[k] = L[i]
        i += 1
        k += 1
    while j < len(R):
        arr[k] = R[j]
        j += 1
        k += 1

def mergesort(arr, izq, der):
    if izq < der:
        medio = izq + (der - izq) // 2
        mergesort(arr, izq, medio)
        mergesort(arr, medio + 1, der)
        merge(arr, izq, medio, der)

# --- RECURSIVIDAD PURA ---
def suma_promedios_recursiva(hoja_calculo, i):
    if i == len(hoja_calculo):
        return 0.0
    return hoja_calculo[i]['promedio'] + suma_promedios_recursiva(hoja_calculo, i + 1)


# ============================================================================
# INTERFAZ GRÁFICA DE STREAMLIT
# ============================================================================

st.title("📊 Mini Hoja de Cálculo Académica")
st.write("Estructuras de Datos y Algoritmos Avanzados aplicados de forma visual.")
st.divider() # Corrección aplicada aquí de st.hr() a st.divider()

# --- SIDEBAR: OPERACIONES DE GESTIÓN (REGISTRO, ACCIONES Y COLA) ---
with st.sidebar:
    st.header("⚙️ Panel de Operaciones")
    
    # 1. Registrar Estudiante
    with st.expander("📝 Registrar Estudiante", expanded=False):
        with st.form("form_registro", clear_on_submit=True):
            codigo = st.text_input("Código Único:").strip()
            nombre = st.text_input("Apellidos y Nombres:")
            n1 = st.number_input("Nota 1:", min_value=0.0, max_value=20.0, step=0.5)
            n2 = st.number_input("Nota 2:", min_value=0.0, max_value=20.0, step=0.5)
            n3 = st.number_input("Nota 3:", min_value=0.0, max_value=20.0, step=0.5)
            btn_registrar = st.form_submit_button("Guardar en Hoja")
            
            if btn_registrar:
                if not codigo or not nombre:
                    st.error("El código y el nombre son obligatorios.")
                elif codigo in st.session_state.indiceHash:
                    st.error(f"¡ERROR! El código {codigo} ya existe (Validación Hash O(1)).")
                else:
                    guardar_historial()
                    prom = calcular_promedio(n1, n2, n3)
                    nuevo_estudiante = {
                        "codigo": codigo, "nombre": nombre,
                        "nota1": n1, "nota2": n2, "nota3": n3, "promedio": prom
                    }
                    st.session_state.hoja.append(nuevo_estudiante)
                    actualizar_hash()
                    st.success("¡Registro insertado con éxito!")
                    st.rerun()

    # 2. Sistema Undo (Stack)
    st.subheader("⏪ Acciones de Control")
    if st.button("Deshacer Última Modificación (Undo)"):
        if st.session_state.historial:
            st.session_state.hoja = st.session_state.historial.pop()
            actualizar_hash()
            st.warning("Deshacer completado. Estado anterior restaurado.")
            st.rerun()
        else:
            st.info("No hay acciones en el historial para deshacer.")

    # 3. Gestión de la Cola FIFO (Secretaría)
    st.subheader("🏢 Cola de Atención (Secretaría)")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        cod_cola = st.text_input("Código para Cola:", key="cod_cola").strip()
        if st.button("Añadir a Cola"):
            if cod_cola in st.session_state.indiceHash:
                st.session_state.colaAtencion.append(cod_cola)
                st.success("Añadido a la cola.")
                st.rerun()
            else:
                st.error("El código no existe en el sistema.")
    with col_c2:
        st.write("Siguiente en espera:")
        if st.session_state.colaAtencion:
            st.code(st.session_state.colaAtencion[0])
        else:
            st.caption("Cola vacía")
            
        if st.button("Atender Próximo"):
            if st.session_state.colaAtencion:
                proximo_cod = st.session_state.colaAtencion.popleft()
                if proximo_cod in st.session_state.indiceHash:
                    pos = st.session_state.indiceHash[proximo_cod]
                    st.balloons()
                    st.success(f"Atendiendo a: {st.session_state.hoja[pos]['nombre']}")
                else:
                    st.warning("El estudiante en cola ya no existe en el sistema.")
            else:
                st.info("No hay estudiantes pendientes.")


# --- CUERPO PRINCIPAL: VISUALIZACIÓN, BÚSQUEDAS Y MÉTRICAS ---

# Bloque 1: Métricas Analíticas por Recursividad Pura
if st.session_state.hoja:
    total_alumnos = len(st.session_state.hoja)
    suma_total = suma_promedios_recursiva(st.session_state.hoja, 0)
    promedio_global = round(suma_total / total_alumnos, 2)
else:
    total_alumnos, promedio_global = 0, 0.0

col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.markdown(f"<div class='metric-card'><h3>Alumnos Registrados</h3><h2>{total_alumnos}</h2></div>", unsafe_allow_html=True)
with col_m2:
    st.markdown(f"<div class='metric-card'><h3>Promedio de Cohorte</h3><h2>{promedio_global}</h2></div>", unsafe_allow_html=True)
with col_m3:
    st.markdown(f"<div class='metric-card'><h3>En Cola de Espera</h3><h2>{len(st.session_state.colaAtencion)} alumnos</h2></div>", unsafe_allow_html=True)

st.write("")

# Bloque 2: Herramientas de búsqueda y ordenamiento de la Tabla
col_t1, col_t2, col_t3 = st.columns([2, 2, 2])

with col_t1:
    # Búsqueda O(1) vía Hash
    search_query = st.text_input("🔍 Búsqueda Instantánea O(1) por Código:").strip()
    if search_query:
        if search_query in st.session_state.indiceHash:
            pos = st.session_state.indiceHash[search_query]
            est = st.session_state.hoja[pos]
            st.info(f"**Resultado:** {est['nombre']} | **Promedio:** {est['promedio']}")
        else:
            st.error("Código no encontrado en el índice Hash.")

with col_t2:
    st.write("⚡ **Algoritmos de Ordenación**")
    if st.button("QuickSort Descendente [Por Promedio]"):
        if st.session_state.hoja:
            guardar_historial()
            quicksort(st.session_state.hoja, 0, len(st.session_state.hoja) - 1)
            actualizar_hash()
            st.success("¡Ordenado por Promedio (Mayor a Menor)!")
            st.rerun()

with col_t3:
    st.write("📂 **Organización de Datos**")
    if st.button("MergeSort Ascendente [Por Código]"):
        if st.session_state.hoja:
            guardar_historial()
            mergesort(st.session_state.hoja, 0, len(st.session_state.hoja) - 1)
            actualizar_hash()
            st.success("¡Ordenado por Código Alfanumérico!")
            st.rerun()


# Bloque 3: Visualización de la Hoja de Cálculo
st.subheader("📋 Datos en la Hoja de Cálculo")
if st.session_state.hoja:
    # Convertimos la lista de dicts a un DataFrame de Pandas únicamente para renderizar la tabla de forma nativa y estética
    df = pd.DataFrame(st.session_state.hoja)
    df.columns = ["Código", "Nombre Completo", "Nota 1", "Nota 2", "Nota 3", "Promedio Final"]
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("La hoja de cálculo está vacía. Utiliza el panel de la izquierda para registrar estudiantes.")

from practica9_bst import ArbolAcademico, cargar_datos_prueba

# Cargar datos de prueba
datos = cargar_datos_prueba()

# Crear árbol
arbol = ArbolAcademico()

# Insertar datos
for e in datos:
    arbol.insertar(e)

# ============================================
# VERIFICACIÓN P1: In-Order ordenado
# ============================================

def es_ordenada(lista):
    return all(
        lista[i] <= lista[i + 1]
        for i in range(len(lista) - 1)
    )

recorrido = arbol.in_order()

# Si in_order devuelve objetos Estudiante
codigos = [e.codigo for e in recorrido]

assert es_ordenada(codigos), 'P1 violada'

print('P1 VERIFICADA: In-Order ordenado ✓')


# ============================================
# VERIFICACIÓN P3: Conteo recursivo
# ============================================

def contar(raiz):
    if raiz is None:
        return 0

    return (
        contar(raiz.izquierdo)
        + contar(raiz.derecho)
        + 1
    )

assert contar(arbol._raiz) == len(arbol.in_order()), 'P3 violada'

print('P3 VERIFICADA: |T| = |T_L| + |T_R| + 1 ✓')


# ============================================
# VERIFICACIÓN P4: Invariante BST
# ============================================

def es_bst(n, mn=float('-inf'), mx=float('inf')):
    if n is None:
        return True

    if not (mn < n.dato.codigo < mx):
        return False

    return (
        es_bst(n.izquierdo, mn, n.dato.codigo)
        and
        es_bst(n.derecho, n.dato.codigo, mx)
    )


# Verificar BST del árbol completo
assert es_bst(arbol._raiz), 'P4 violada'

print('P4 VERIFICADA: BST válido ✓')


# ============================================
# VERIFICACIÓN P4 TRAS CADA INSERCIÓN
# ============================================

arbol2 = ArbolAcademico()

for e in datos:
    arbol2.insertar(e)

    assert es_bst(arbol2._raiz), (
        f'P4 violada tras insertar {e.codigo}'
    )

print('P4 VERIFICADA tras todas las inserciones ✓')


# ============================================
# RESUMEN
# ============================================

print('\nTODAS LAS PROPIEDADES VERIFICADAS ✓')

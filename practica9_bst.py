from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, List
from collections import deque
import statistics
import time
import random


class EstadoAcademico(Enum):
    ACTIVO = auto()
    EGRESADO = auto()
    RETIRADO = auto()
    SUSPENDIDO = auto()


@dataclass
class Estudiante:
    """Expediente académico — clave del BST: codigo."""
    codigo: int
    nombre: str
    escuela: str
    ppa: float
    creditos: int
    estado: EstadoAcademico
    semestre_ingreso: str

    def __post_init__(self):
        if not (10_000_000 <= self.codigo <= 29_999_999):
            raise ValueError(f"Código inválido: {self.codigo}")
        if not (0.0 <= self.ppa <= 20.0):
            raise ValueError(f"PPA fuera de rango [0,20]: {self.ppa}")


@dataclass
class NodoBST:
    dato: Estudiante
    izquierdo: Optional["NodoBST"] = field(default=None, repr=False)
    derecho: Optional["NodoBST"] = field(default=None, repr=False)


class ArbolAcademico:
    """BST para gestión de expedientes académicos UNA-PUNO."""

    def __init__(self) -> None:
        self._raiz: Optional[NodoBST] = None

    # =========================
    # INSERTAR
    # =========================
    def insertar(self, e: Estudiante) -> None:
        self._raiz = self._insertar(self._raiz, e)

    def _insertar(self, nodo: Optional[NodoBST], e: Estudiante) -> NodoBST:
        if nodo is None:
            return NodoBST(dato=e)
        if e.codigo < nodo.dato.codigo:
            nodo.izquierdo = self._insertar(nodo.izquierdo, e)
        elif e.codigo > nodo.dato.codigo:
            nodo.derecho = self._insertar(nodo.derecho, e)
        else:
            raise ValueError(f"Código duplicado: {e.codigo}")
        return nodo

    # =========================
    # BUSCAR
    # =========================
    def buscar(self, codigo: int) -> Optional[Estudiante]:
        nodo = self._buscar(self._raiz, codigo)
        return nodo.dato if nodo else None

    def _buscar(self, nodo: Optional[NodoBST], codigo: int) -> Optional[NodoBST]:
        if nodo is None or nodo.dato.codigo == codigo:
            return nodo
        if codigo < nodo.dato.codigo:
            return self._buscar(nodo.izquierdo, codigo)
        return self._buscar(nodo.derecho, codigo)

    # =========================
    # ELIMINAR
    # =========================
    def eliminar(self, codigo: int) -> None:
        if self.buscar(codigo) is None:
            raise KeyError(f"Código no encontrado: {codigo}")
        self._raiz = self._eliminar(self._raiz, codigo)

    def _eliminar(self, nodo: Optional[NodoBST], codigo: int) -> Optional[NodoBST]:
        if nodo is None:
            return None

        if codigo < nodo.dato.codigo:
            nodo.izquierdo = self._eliminar(nodo.izquierdo, codigo)
        elif codigo > nodo.dato.codigo:
            nodo.derecho = self._eliminar(nodo.derecho, codigo)
        else:
            if nodo.izquierdo is None:
                return nodo.derecho
            if nodo.derecho is None:
                return nodo.izquierdo

            sucesor = self._minimo_nodo(nodo.derecho)
            nodo.dato = sucesor.dato
            nodo.derecho = self._eliminar(nodo.derecho, sucesor.dato.codigo)

        return nodo

    def _minimo_nodo(self, nodo: NodoBST) -> NodoBST:
        while nodo.izquierdo is not None:
            nodo = nodo.izquierdo
        return nodo

    # =========================
    # RECORRIDOS
    # =========================
    def in_order(self) -> List[Estudiante]:
        resultado: List[Estudiante] = []
        self._in_order(self._raiz, resultado)
        return resultado

    def _in_order(self, nodo: Optional[NodoBST], res: List[Estudiante]) -> None:
        if nodo is None:
            return
        self._in_order(nodo.izquierdo, res)
        res.append(nodo.dato)
        self._in_order(nodo.derecho, res)

    def pre_order(self) -> List[Estudiante]:
        resultado: List[Estudiante] = []
        self._pre_order(self._raiz, resultado)
        return resultado

    def _pre_order(self, nodo: Optional[NodoBST], res: List[Estudiante]) -> None:
        if nodo is None:
            return
        res.append(nodo.dato)
        self._pre_order(nodo.izquierdo, res)
        self._pre_order(nodo.derecho, res)

    def post_order(self) -> List[Estudiante]:
        resultado: List[Estudiante] = []
        self._post_order(self._raiz, resultado)
        return resultado

    def _post_order(self, nodo: Optional[NodoBST], res: List[Estudiante]) -> None:
        if nodo is None:
            return
        self._post_order(nodo.izquierdo, res)
        self._post_order(nodo.derecho, res)
        res.append(nodo.dato)

    def bfs(self) -> List[Estudiante]:
        if self._raiz is None:
            return []

        resultado: List[Estudiante] = []
        cola = deque([self._raiz])

        while cola:
            nodo = cola.popleft()
            resultado.append(nodo.dato)
            if nodo.izquierdo:
                cola.append(nodo.izquierdo)
            if nodo.derecho:
                cola.append(nodo.derecho)

        return resultado

    # =========================
    # UTILIDADES
    # =========================
    def altura(self) -> int:
        return self._altura(self._raiz)

    def _altura(self, nodo: Optional[NodoBST]) -> int:
        if nodo is None:
            return -1
        return 1 + max(self._altura(nodo.izquierdo), self._altura(nodo.derecho))

    def maximo(self) -> Optional[Estudiante]:
        if self._raiz is None:
            return None
        nodo = self._raiz
        while nodo.derecho is not None:
            nodo = nodo.derecho
        return nodo.dato

    def buscar_rango_codigo(self, cod_min: int, cod_max: int) -> List[Estudiante]:
        resultado: List[Estudiante] = []
        self._buscar_rango_codigo(self._raiz, cod_min, cod_max, resultado)
        return resultado

    def _buscar_rango_codigo(
        self,
        nodo: Optional[NodoBST],
        cod_min: int,
        cod_max: int,
        res: List[Estudiante],
    ) -> None:
        if nodo is None:
            return

        if cod_min < nodo.dato.codigo:
            self._buscar_rango_codigo(nodo.izquierdo, cod_min, cod_max, res)

        if cod_min <= nodo.dato.codigo <= cod_max:
            res.append(nodo.dato)

        if nodo.dato.codigo < cod_max:
            self._buscar_rango_codigo(nodo.derecho, cod_min, cod_max, res)

    # =========================
    # CONSULTAS
    # =========================
    def por_rango_ppa(self, ppa_min: float, ppa_max: float = 20.0) -> List[Estudiante]:
        return [e for e in self.in_order() if ppa_min <= e.ppa <= ppa_max]

    def por_escuela(self, escuela: str) -> List[Estudiante]:
        return [e for e in self.in_order() if e.escuela == escuela]

    def por_estado(self, estado: EstadoAcademico) -> List[Estudiante]:
        return [e for e in self.in_order() if e.estado == estado]

    # =========================
    # ESTADÍSTICAS
    # =========================
    def estadisticas(self) -> dict:
        todos = self.in_order()
        if not todos:
            return {}

        ppas = [e.ppa for e in todos]
        return {
            "total_nodos": len(todos),
            "altura": self.altura(),
            "ppa_promedio": round(statistics.mean(ppas), 2),
            "ppa_minimo": min(ppas),
            "ppa_maximo": max(ppas),
            "total_activos": sum(1 for e in todos if e.estado == EstadoAcademico.ACTIVO),
        }

    # =========================
    # IMPRESIÓN ASCII
    # =========================
    def imprimir_arbol(self) -> None:
        print("\n── Estructura del BST ──")
        self._imprimir(self._raiz, "", False)

    def _imprimir(self, nodo: Optional[NodoBST], prefix: str, is_left: bool) -> None:
        if nodo is None:
            return
        conector = "├── " if is_left else "└── "
        print(f"{prefix}{conector}{nodo.dato.codigo} [PPA:{nodo.dato.ppa:.1f}]")
        ext = "│   " if is_left else "    "
        self._imprimir(nodo.izquierdo, prefix + ext, True)
        self._imprimir(nodo.derecho, prefix + ext, False)


# =========================
# DATOS DE PRUEBA
# =========================
def cargar_datos_prueba() -> List[Estudiante]:
    return [
        Estudiante(20210500, "Mamani Quispe, Juan", "Ing. Sistemas", 15.8, 120, EstadoAcademico.ACTIVO, "2021-I"),
        Estudiante(20210300, "Huanca Apaza, Maria", "Ing. Civil", 14.2, 110, EstadoAcademico.ACTIVO, "2021-I"),
        Estudiante(20210700, "Condori Flores, Pedro", "Medicina", 17.1, 130, EstadoAcademico.ACTIVO, "2021-I"),
        Estudiante(20210100, "Ticona Lupaca, Rosa", "Contabilidad", 12.0, 90, EstadoAcademico.SUSPENDIDO, "2021-I"),
        Estudiante(20210400, "Larico Ccama, Carlos", "Ing. Sistemas", 16.5, 115, EstadoAcademico.ACTIVO, "2021-I"),
        Estudiante(20210600, "Cutipa Vargas, Elena", "Agronomia", 13.7, 100, EstadoAcademico.ACTIVO, "2021-I"),
        Estudiante(20210900, "Pari Choque, Luis", "Ing. Sistemas", 18.3, 140, EstadoAcademico.EGRESADO, "2021-I"),
    ]


# =========================
# BENCHMARK
# =========================
def generar_datos(n: int) -> List[Estudiante]:
    codigos = random.sample(range(20_000_000, 29_999_999), n)
    return [
        Estudiante(
            cod,
            f"Estudiante_{i}",
            "Ingenieria",
            round(random.uniform(8.0, 20.0), 1),
            100,
            EstadoAcademico.ACTIVO,
            "2024-I",
        )
        for i, cod in enumerate(codigos)
    ]


def benchmark(n: int) -> None:
    datos = generar_datos(n)
    buscar_cod = datos[n // 2].codigo

    arbol_b = ArbolAcademico()
    t0 = time.perf_counter()
    for e in datos:
        arbol_b.insertar(e)
    t_ins_bst = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    arbol_b.buscar(buscar_cod)
    t_bus_bst = (time.perf_counter() - t0) * 1000

    diccionario = {}
    t0 = time.perf_counter()
    for e in datos:
        diccionario[e.codigo] = e
    t_ins_dic = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    _ = diccionario.get(buscar_cod)
    t_bus_dic = (time.perf_counter() - t0) * 1000

    print(
        f"N={n:>8} | BST ins:{t_ins_bst:8.2f} ms bus:{t_bus_bst:8.4f} ms | "
        f"Dict ins:{t_ins_dic:8.2f} ms bus:{t_bus_dic:8.4f} ms | "
        f"Altura BST: {arbol_b.altura()}"
    )


# =========================
# PROGRAMA PRINCIPAL
# =========================
if __name__ == "__main__":
    print("=== BST Sistema Académico UNA-PUNO (Python 3.11+) ===\n")

    arbol = ArbolAcademico()
    for e in cargar_datos_prueba():
        arbol.insertar(e)

    print(f"Altura del árbol: {arbol.altura()}\n")

    print("In-Order (ordenado por código):")
    for e in arbol.in_order():
        print(f"{e.codigo} {e.nombre:<35} {e.escuela:<18} PPA:{e.ppa}")

    print("\nPre-Order:")
    print([e.codigo for e in arbol.pre_order()])

    print("\nPost-Order:")
    print([e.codigo for e in arbol.post_order()])

    print("\nBFS (nivel por nivel):")
    print([e.codigo for e in arbol.bfs()])

    print("\nBúsqueda:")
    encontrado = arbol.buscar(20210700)
    if encontrado:
        print(f"Encontrado: {encontrado.codigo} {encontrado.nombre} PPA:{encontrado.ppa}")

    no_existe = arbol.buscar(99999999)
    print(f"Buscar 99999999: {no_existe}")

    print(f"\nNodos antes de eliminar: {len(arbol.in_order())}")
    arbol.eliminar(20210300)
    print(f"Nodos después de eliminar 20210300: {len(arbol.in_order())}")
    print("In-Order después:", [e.codigo for e in arbol.in_order()])

    print("\nEstudiantes con PPA >= 15.0:")
    for e in arbol.por_rango_ppa(15.0):
        print(f"{e.codigo} {e.nombre:<35} PPA:{e.ppa}")

    print("\nEstadísticas del árbol:")
    for k, v in arbol.estadisticas().items():
        print(f"{k:<20}: {v}")

    print("\nMáximo código:")
    max_est = arbol.maximo()
    if max_est:
        print(f"{max_est.codigo} {max_est.nombre}")

    print("\nBuscar rango de códigos [20210400, 20210900]:")
    print([e.codigo for e in arbol.buscar_rango_codigo(20210400, 20210900)])

    arbol.imprimir_arbol()

    print("\n=== Benchmark BST vs Dict ===")
    print("N         | BST inserción/búsqueda | Dict inserción/búsqueda | Altura")
    print("-" * 90)
    for n in [100, 1_000, 10_000, 100_000]:
        benchmark(n)

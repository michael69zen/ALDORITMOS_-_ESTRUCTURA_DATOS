#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
#include <queue>
#include <memory>           //unique_ptr
#include <optional>         //optional<NodoBST>
#include <stdexcept>        //runtime_error, invalid_argument
#include <algorithm>

using namespace std;

namespace una_puno {

enum class EstadoAcademico {
    ACTIVO,
    EGRESADO,
    RETIRADO,
    SUSPENDIDO
};

inline string estadoStr(EstadoAcademico e) {

    switch (e) {

        case EstadoAcademico::ACTIVO:
            return "ACTIVO";

        case EstadoAcademico::EGRESADO:
            return "EGRESADO";

        case EstadoAcademico::RETIRADO:
            return "RETIRADO";

        case EstadoAcademico::SUSPENDIDO:
            return "SUSPENDIDO";

        default:
            return "DESCONOCIDO";
    }
}

// Datos del estudiante
struct Estudiante {

    int codigo;
    string nombre;
    string escuela;
    float ppa;
    int creditos;
    EstadoAcademico estado;
    string semestre_ingreso;
    
    //constructor con validacion
    Estudiante(
        int cod,
        string nom,
        string esc,
        float pp,
        int cred,
        EstadoAcademico est,
        string sem
    )
        : codigo(cod),
          nombre(move(nom)),
          escuela(move(esc)),
          ppa(pp),
          creditos(cred),
          estado(est),
          semestre_ingreso(move(sem))
    {

        if (cod < 10000000 || cod > 29999999)
            throw invalid_argument(
                "Codigo invalido: " + to_string(cod)
            );

        if (pp < 0.0f || pp > 20.0f)
            throw invalid_argument(
                "PPA fuera de rango [0,20]"
            );
    }

    void print() const {

        cout << left
             << setw(10) << codigo
             << setw(35) << nombre
             << setw(20) << escuela
             << "PPA:"
             << fixed
             << setprecision(1)
             << ppa
             << "  "
             << estadoStr(estado)
             << '\n';
    }
};

// Nodo BST
struct NodoBST {

    Estudiante dato;

    unique_ptr<NodoBST> izquierdo;
    unique_ptr<NodoBST> derecho;

    explicit NodoBST(Estudiante e)
        : dato(move(e)),
          izquierdo(nullptr),
          derecho(nullptr)
    {
    }
};


// Clase ArbolAcademico
class ArbolAcademico {

public:

    ArbolAcademico() = default;

    // Insertar
    void insertar(Estudiante e) {
        insertar_(raiz, move(e));
    }

private:

    unique_ptr<NodoBST> raiz;

    void insertar_(unique_ptr<NodoBST>& nodo, Estudiante e) {

        if (!nodo) {
            nodo = make_unique<NodoBST>(move(e));
            return;
        }

        if (e.codigo < nodo->dato.codigo)
            insertar_(nodo->izquierdo, move(e));

        else if (e.codigo > nodo->dato.codigo)
            insertar_(nodo->derecho, move(e));

        else
            throw runtime_error(
                "Codigo duplicado: " + to_string(e.codigo)
            );
    }

public:
    
    // IN-ORDER
    vector<Estudiante> inOrder() const {
        vector<Estudiante> resultado;
        inOrder_(raiz.get(), resultado);
        return resultado;
    }

private:

    void inOrder_(const NodoBST* n, vector<Estudiante>& r) const {
        if (!n) return;

        inOrder_(n->izquierdo.get(), r);
        r.push_back(n->dato);
        inOrder_(n->derecho.get(), r);
    }

public:

    // PRE-ORDER
    vector<Estudiante> preOrder() const {
        vector<Estudiante> resultado;
        preOrder_(raiz.get(), resultado);
        return resultado;
    }

private:

    void preOrder_(const NodoBST* n, vector<Estudiante>& r) const {
        if (!n) return;

        r.push_back(n->dato);
        preOrder_(n->izquierdo.get(), r);
        preOrder_(n->derecho.get(), r);
    }

public:

    // BFS (Recorrido por niveles)
    vector<Estudiante> bfs() const {

        vector<Estudiante> resultado;

        if (!raiz) return resultado;

        queue<const NodoBST*> cola;
        cola.push(raiz.get());

        while (!cola.empty()) {
            
            const NodoBST* actual = cola.front();
            cola.pop();

            resultado.push_back(actual->dato);

            if (actual->izquierdo)
                cola.push(actual->izquierdo.get());

            if (actual->derecho)
                cola.push(actual->derecho.get());
        }

        return resultado;
    }

    // ALTURA
    int altura() const {
        return altura_(raiz.get());
    }

    bool estaVacio() const {
        return raiz == nullptr;
    }

private:
    int altura_(const NodoBST* n) const {
        if (!n) return -1;

        return 1 + max(altura_(n->izquierdo.get()), altura_(n->derecho.get()));
    }

public:

    // BUSCAR
    optional<Estudiante> buscar(int codigo) const {
        const NodoBST* nodo = buscar_(raiz.get(), codigo);
        
        if (nodo) return nodo->dato;
            
        return nullopt;
    }

private:

    const NodoBST* buscar_(const NodoBST* n, int cod) const {

        if (!n || n->dato.codigo == cod)
            return n;

        if (cod < n->dato.codigo)
            return buscar_(n->izquierdo.get(), cod);

        return buscar_(n->derecho.get(), cod);
    }

public:
    
    // ELIMINAR
    void eliminar(int codigo) {

        if (!buscar(codigo))
            throw runtime_error( "Codigo no encontrado: " + to_string(codigo) );

        raiz = eliminar_(move(raiz), codigo);
    }

private:

    unique_ptr<NodoBST> eliminar_( unique_ptr<NodoBST> nodo, int cod ) {

        if (!nodo) return nullptr;

        if (cod < nodo->dato.codigo) {
            nodo->izquierdo = eliminar_(move(nodo->izquierdo), cod);
        } else if (cod > nodo->dato.codigo) {
            nodo->derecho = eliminar_(move(nodo->derecho), cod);
        }
        else {

            //--------------------------------------------------
            // Caso 1: sin hijo izquierdo
            //--------------------------------------------------

            if (!nodo->izquierdo)
                return move(nodo->derecho);

            //--------------------------------------------------
            // Caso 2: sin hijo derecho
            //--------------------------------------------------

            if (!nodo->derecho)
                return move(nodo->izquierdo);

            //--------------------------------------------------
            // Caso 3: dos hijos
            //--------------------------------------------------

            NodoBST* sucesor =
                minimo_(nodo->derecho.get());

            nodo->dato = sucesor->dato;

            nodo->derecho =
                eliminar_( move(nodo->derecho), sucesor->dato.codigo );
        }

        return nodo;
    }

    // MÍNIMO
    NodoBST* minimo_(NodoBST* nodo) const {
        while (nodo->izquierdo)
            nodo = nodo->izquierdo.get();

        return nodo;
    }

public:

    // CONSULTA POR RANGO DE PPA
    vector<Estudiante> porRangoPPA(
        float ppa_min,
        float ppa_max = 20.0f
    ) const {

        auto todos = inOrder();

        vector<Estudiante> resultado;

        copy_if(
            todos.begin(),
            todos.end(),
            back_inserter(resultado),

            [ppa_min, ppa_max](const Estudiante& e)
            {
                return e.ppa >= ppa_min &&
                       e.ppa <= ppa_max;
            }
        );

        return resultado;
    }

public:
    
    // ESTADÍSTICAS
    void estadisticas() const {

        auto todos = inOrder();

        if (todos.empty()) {
            cout << "Arbol vacio\n";
            return;
        }

        float suma = 0.0f;
        float minimo = 20.0f;
        float maximo = 0.0f;
        int activos = 0;

        for (const auto& e : todos) {

            suma += e.ppa;

            if (e.ppa < minimo)
                minimo = e.ppa;

            if (e.ppa > maximo)
                maximo = e.ppa;

            if (e.estado == EstadoAcademico::ACTIVO)
                activos++;
        }

        cout << fixed << setprecision(2);

        cout << "  Total nodos  : "
             << todos.size() << '\n';

        cout << "  Altura       : "
             << altura() << '\n';

        cout << "  PPA promedio : "
             << suma / todos.size() << '\n';

        cout << "  PPA minimo   : "
             << minimo << '\n';

        cout << "  PPA maximo   : "
             << maximo << '\n';

        cout << "  Activos      : "
             << activos << '\n';
    }

    //------------------------------------------------------
    // IMPRIMIR ÁRBOL
    //------------------------------------------------------

    void imprimirArbol() const {

        cout << "\n-- Estructura del BST --\n";

        imprimir_(raiz.get(), "", false);
    }

private:

    void imprimir_(const NodoBST* nodo,
                   string prefijo,
                   bool izquierdo) const {

        if (!nodo) return;

        string conector;

        if (izquierdo)
            conector = "+-- ";
        else
            conector = "`-- ";

        cout << prefijo
             << conector
             << nodo->dato.codigo
             << " [PPA:"
             << fixed
             << setprecision(1)
             << nodo->dato.ppa
             << "]"
             << '\n';

        string extension;

        if (izquierdo)
            extension = "|   ";
        else
            extension = "    ";

        imprimir_(
            nodo->izquierdo.get(),
            prefijo + extension,
            true
        );

        imprimir_(
            nodo->derecho.get(),
            prefijo + extension,
            false
        );
    }

}; // Fin clase ArbolAcademico

} // namespace una_puno

using namespace una_puno;

int main() {

    cout << "==============================================\n";
    cout << " BST - Sistema Academico UNA-PUNO (C++17)\n";
    cout << "==============================================\n\n";

    ArbolAcademico arbol;

    //------------------------------------------------------
    // Inserción de estudiantes
    //------------------------------------------------------

    arbol.insertar(
        Estudiante(
            20210500,
            "Mamani Quispe, Juan",
            "Ing. Sistemas",
            15.8f,
            120,
            EstadoAcademico::ACTIVO,
            "2021-I"
        )
    );

    arbol.insertar(
        Estudiante(
            20210300,
            "Huanca Apaza, Maria",
            "Ing. Civil",
            14.2f,
            110,
            EstadoAcademico::ACTIVO,
            "2021-I"
        )
    );

    arbol.insertar(
        Estudiante(
            20210700,
            "Condori Flores, Pedro",
            "Medicina",
            17.1f,
            130,
            EstadoAcademico::ACTIVO,
            "2021-I"
        )
    );

    arbol.insertar(
        Estudiante(
            20210100,
            "Ticona Lupaca, Rosa",
            "Contabilidad",
            12.0f,
            90,
            EstadoAcademico::SUSPENDIDO,
            "2021-I"
        )
    );

    arbol.insertar(
        Estudiante(
            20210400,
            "Larico Ccama, Carlos",
            "Ing. Sistemas",
            16.5f,
            115,
            EstadoAcademico::ACTIVO,
            "2021-I"
        )
    );

    arbol.insertar(
        Estudiante(
            20210600,
            "Cutipa Vargas, Elena",
            "Agronomia",
            13.7f,
            100,
            EstadoAcademico::ACTIVO,
            "2021-I"
        )
    );

    arbol.insertar(
        Estudiante(
            20210900,
            "Pari Choque, Luis",
            "Ing. Sistemas",
            18.3f,
            140,
            EstadoAcademico::EGRESADO,
            "2021-I"
        )
    );

    //------------------------------------------------------
    // Mostrar estructura del árbol
    //------------------------------------------------------

    arbol.imprimirArbol();

    //------------------------------------------------------
    // Recorrido In-Order
    //------------------------------------------------------

    cout << "\n";
    cout << "============== IN-ORDER ==============\n";

    cout << left
         << setw(12) << "CODIGO"
         << setw(35) << "NOMBRE"
         << setw(20) << "ESCUELA"
         << "PPA\n";

    cout << string(80, '-') << '\n';

    for (const auto& e : arbol.inOrder())
        e.print();

    //------------------------------------------------------
    // Búsquedas
    //------------------------------------------------------

    cout << "\n";
    cout << "============== BUSQUEDA ==============\n";

    auto encontrado = arbol.buscar(20210700);

    if (encontrado) {

        cout << "Encontrado:\n";

        encontrado->print();
    }

    auto inexistente = arbol.buscar(99999999);

    cout << "\nBuscar codigo 99999999: ";

    if (inexistente)
        cout << "Encontrado\n";
    else
        cout << "No encontrado\n";

    //------------------------------------------------------
    // Consulta por rango de PPA
    //------------------------------------------------------

    cout << "\n";
    cout << "======= ESTUDIANTES CON PPA >= 15 =======\n";

    for (const auto& e : arbol.porRangoPPA(15.0f))
        e.print();

    //------------------------------------------------------
    // Estadísticas
    //------------------------------------------------------

    cout << "\n";
    cout << "============== ESTADISTICAS ==============\n";

    arbol.estadisticas();

    //------------------------------------------------------
    // Eliminar un nodo con dos hijos
    //------------------------------------------------------

    cout << "\n";
    cout << "Eliminando codigo 20210300...\n";

    arbol.eliminar(20210300);

    //------------------------------------------------------
    // Mostrar InOrder después de eliminar
    //------------------------------------------------------

    cout << "\n";
    cout << "========== IN-ORDER DESPUES DE ELIMINAR ==========\n";

    cout << left
         << setw(12) << "CODIGO"
         << setw(35) << "NOMBRE"
         << setw(20) << "ESCUELA"
         << "PPA\n";

    cout << string(80, '-') << '\n';

    for (const auto& e : arbol.inOrder())
        e.print();

    //------------------------------------------------------
    // Mostrar cantidad de nodos
    //------------------------------------------------------

    cout << "\n";

    cout << "Nodos restantes: "
         << arbol.inOrder().size()
         << "\n";

    //------------------------------------------------------
    // Mostrar solamente los códigos
    //------------------------------------------------------

    cout << "Codigos en InOrder: ";

    for (const auto& e : arbol.inOrder())
        cout << e.codigo << " ";

    cout << "\n";

    //------------------------------------------------------
    // Recorrido BFS
    //------------------------------------------------------

    cout << "\n";
    cout << "============== BFS ==============\n";

    for (const auto& e : arbol.bfs())
        cout << e.codigo << " ";

    cout << "\n";

    //------------------------------------------------------
    // Altura del árbol
    //------------------------------------------------------

    cout << "\n";

    cout << "Altura del arbol: "
         << arbol.altura()
         << "\n";

    //------------------------------------------------------
    // Árbol final
    //------------------------------------------------------

    cout << "\n";
    cout << "===== ESTRUCTURA FINAL DEL ARBOL =====\n";

    arbol.imprimirArbol();

    cout << "\nPrograma finalizado correctamente.\n";

    return 0;
}

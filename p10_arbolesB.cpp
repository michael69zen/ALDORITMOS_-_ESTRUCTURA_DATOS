//=========================================================
// Biblioteca para entrada y salida de datos
// Permite utilizar cout, cin y endl.
//=========================================================
#include <iostream>

// Permite utilizar los elementos de la biblioteca estándar
// sin escribir std:: delante de cada uno.
using namespace std;

//=========================================================
// Definición del grado mínimo del Árbol B.
//
// T = 3 significa:
// - Cada nodo puede tener como máximo 5 claves (2*T-1)
// - Cada nodo puede tener como máximo 6 hijos (2*T)
//=========================================================
const int T = 3;

//=========================================================
// Clase que representa un nodo del Árbol B.
//=========================================================
class BTreeNode {

public:

    //-----------------------------------------------------
    // Arreglo donde se almacenan las claves del nodo.
    // El máximo número de claves es (2*T-1).
    //-----------------------------------------------------
    int keys[2 * T - 1];

    //-----------------------------------------------------
    // Arreglo de punteros a los hijos.
    // Un nodo puede tener hasta (2*T) hijos.
    //-----------------------------------------------------
    BTreeNode* children[2 * T];

    //-----------------------------------------------------
    // Número actual de claves almacenadas.
    //-----------------------------------------------------
    int n;

    //-----------------------------------------------------
    // Indica si el nodo es hoja.
    //-----------------------------------------------------
    bool leaf;

    //-----------------------------------------------------
    // Constructor
    //-----------------------------------------------------
    BTreeNode(bool _leaf) {

        // Indica si será hoja o nodo interno
        leaf = _leaf;

        // Inicialmente el nodo no contiene claves
        n = 0;

        // Todos los hijos comienzan apuntando a NULL
        for (int i = 0; i < 2 * T; i++)
            children[i] = nullptr;
    }

    //-----------------------------------------------------
    // Recorre el árbol en orden (InOrder).
    //-----------------------------------------------------
    void traverse() {

        int i;

        // Recorre todas las claves del nodo
        for (i = 0; i < n; i++) {

            // Si no es hoja, primero visita
            // el hijo izquierdo.
            if (!leaf)
                children[i]->traverse();

            // Imprime la clave actual.
            cout << keys[i] << " ";
        }

        // Recorre el último hijo.
        if (!leaf)
            children[i]->traverse();
    }

    //-----------------------------------------------------
    // Busca una clave dentro del árbol.
    //-----------------------------------------------------
    BTreeNode* search(int k) {

        // Empieza desde la primera clave.
        int i = 0;

        // Avanza mientras la clave buscada
        // sea mayor que la clave actual.
        while (i < n && k > keys[i])
            i++;

        // Si encontró la clave devuelve el nodo.
        if (i < n && keys[i] == k)
            return this;

        // Si llegó a una hoja y no la encontró
        if (leaf)
            return nullptr;

        // Continúa buscando en el hijo correspondiente.
        return children[i]->search(k);
    }

    //-----------------------------------------------------
    // Declaración de funciones.
    //-----------------------------------------------------
    void insertNonFull(int k);

    void splitChild(int i, BTreeNode* y);
};

//=========================================================
// Clase Árbol B.
//=========================================================
class BTree {

public:

    //-----------------------------------------------------
    // Raíz del árbol.
    //-----------------------------------------------------
    BTreeNode* root;

    //-----------------------------------------------------
    // Constructor.
    //-----------------------------------------------------
    BTree() {

        // Inicialmente el árbol está vacío.
        root = nullptr;
    }

    //-----------------------------------------------------
    // Recorre el árbol completo.
    //-----------------------------------------------------
    void traverse() {

        if (root)
            root->traverse();

        cout << endl;
    }

    //-----------------------------------------------------
    // Busca un elemento.
    //-----------------------------------------------------
    BTreeNode* search(int k) {

        if (root == nullptr)
            return nullptr;

        return root->search(k);
    }

    //-----------------------------------------------------
    // Inserta una nueva clave.
    //-----------------------------------------------------
    void insert(int k);
};

//=========================================================
// Inserción cuando el nodo NO está lleno.
//=========================================================
void BTreeNode::insertNonFull(int k) {

    // Última posición ocupada.
    int i = n - 1;

    //-----------------------------------------------------
    // Si el nodo es hoja.
    //-----------------------------------------------------
    if (leaf) {

        // Desplaza las claves mayores
        // una posición hacia la derecha.
        while (i >= 0 && keys[i] > k) {

            keys[i + 1] = keys[i];

            i--;
        }

        // Inserta la nueva clave.
        keys[i + 1] = k;

        // Incrementa el número de claves.
        n++;
    }

    //-----------------------------------------------------
    // Si NO es hoja.
    //-----------------------------------------------------
    else {

        // Busca el hijo adecuado.
        while (i >= 0 && keys[i] > k)
            i--;

        // Si el hijo está lleno
        if (children[i + 1]->n == 2 * T - 1) {

            // Divide el nodo.
            splitChild(i + 1, children[i + 1]);

            // Determina cuál hijo utilizar.
            if (keys[i + 1] < k)
                i++;
        }

        // Inserta en el hijo correspondiente.
        children[i + 1]->insertNonFull(k);
    }
}

//=========================================================
// Divide un nodo lleno.
//=========================================================
void BTreeNode::splitChild(int i, BTreeNode* y) {

    // Crea un nuevo nodo.
    BTreeNode* z = new BTreeNode(y->leaf);

    // El nuevo nodo tendrá T-1 claves.
    z->n = T - 1;

    // Copia las claves superiores.
    for (int j = 0; j < T - 1; j++)
        z->keys[j] = y->keys[j + T];

    // Si no es hoja copia los hijos.
    if (!y->leaf) {

        for (int j = 0; j < T; j++)
            z->children[j] = y->children[j + T];
    }

    // Reduce el número de claves.
    y->n = T - 1;

    // Desplaza los hijos del padre.
    for (int j = n; j >= i + 1; j--)
        children[j + 1] = children[j];

    // Inserta el nuevo hijo.
    children[i + 1] = z;

    // Desplaza las claves del padre.
    for (int j = n - 1; j >= i; j--)
        keys[j + 1] = keys[j];

    // Sube la clave central.
    keys[i] = y->keys[T - 1];

    // Incrementa el número de claves.
    n++;
}

//=========================================================
// Inserción en el Árbol B.
//=========================================================
void BTree::insert(int k) {

    // Si el árbol está vacío.
    if (root == nullptr) {

        // Crea la raíz.
        root = new BTreeNode(true);

        // Inserta la primera clave.
        root->keys[0] = k;

        root->n = 1;
    }

    //-----------------------------------------------------
    // Si el árbol ya contiene datos.
    //-----------------------------------------------------
    else {

        // Si la raíz está llena.
        if (root->n == 2 * T - 1) {

            // Crea una nueva raíz.
            BTreeNode* s = new BTreeNode(false);

            // La raíz antigua será hijo.
            s->children[0] = root;

            // Divide la raíz.
            s->splitChild(0, root);

            int i = 0;

            if (s->keys[0] < k)
                i++;

            // Inserta la nueva clave.
            s->children[i]->insertNonFull(k);

            // Actualiza la raíz.
            root = s;
        }

        // Si la raíz tiene espacio.
        else {

            root->insertNonFull(k);
        }
    }
}

//=========================================================
// Función principal.
//=========================================================
int main() {

    // Crea un Árbol B vacío.
    BTree t;

    // Arreglo de valores.
    int valores[] = {10, 20, 5, 6, 12, 30, 7, 17};

    // Inserta todos los valores.
    for (int v : valores)
        t.insert(v);

    // Muestra el recorrido InOrder.
    cout << "Recorrido del Árbol B: ";

    t.traverse();

    // Valor a buscar.
    int k = 6;

    // Comprueba si existe.
    if (t.search(k) != nullptr)
        cout << "\nEncontrado " << k << endl;
    else
        cout << "\nNo encontrado" << endl;

    return 0;
}

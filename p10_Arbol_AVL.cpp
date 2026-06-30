// Biblioteca para entrada y salida de datos
#include <iostream>

// Biblioteca que proporciona funciones como max()
#include <algorithm>

// Permite usar cout, endl, max, etc., sin escribir std::
using namespace std;

// Definición de la estructura de un nodo del árbol AVL
struct Node {

    // Valor almacenado en el nodo
    int key;

    // Altura del nodo
    int height;

    // Punteros al hijo izquierdo y derecho
    Node *left, *right;

    // Constructor del nodo
    Node(int val) {

        // Asigna el valor recibido
        key = val;

        // Un nodo nuevo tiene altura 1
        height = 1;

        // Inicialmente no tiene hijos
        left = nullptr;
        right = nullptr;
    }
};

// Función que devuelve la altura de un nodo
int getHeight(Node* n) {

    // Si el nodo existe devuelve su altura,
    // en caso contrario devuelve 0.
    return (n != nullptr) ? n->height : 0;
}

// Calcula el factor de balance
int getBalance(Node* n) {

    // Altura izquierda - altura derecha
    return (n != nullptr) ?
           getHeight(n->left) - getHeight(n->right) : 0;
}

// Rotación simple hacia la derecha
Node* rightRotate(Node* y) {

    // Nuevo nodo raíz
    Node* x = y->left;

    // Subárbol temporal
    Node* T2 = x->right;

    // Realiza la rotación
    x->right = y;
    y->left = T2;

    // Actualiza alturas
    y->height = max(getHeight(y->left), getHeight(y->right)) + 1;

    x->height = max(getHeight(x->left), getHeight(x->right)) + 1;

    // Devuelve la nueva raíz
    return x;
}

// Rotación simple hacia la izquierda
Node* leftRotate(Node* x) {

    // Nuevo nodo raíz
    Node* y = x->right;

    // Subárbol temporal
    Node* T2 = y->left;

    // Realiza la rotación
    y->left = x;
    x->right = T2;

    // Actualiza alturas
    x->height = max(getHeight(x->left), getHeight(x->right)) + 1;

    y->height = max(getHeight(y->left), getHeight(y->right)) + 1;

    // Devuelve la nueva raíz
    return y;
}

// Inserta un nodo en el árbol AVL
Node* insert(Node* node, int key) {

    // Si el árbol está vacío crea un nuevo nodo
    if (node == nullptr)
        return new Node(key);

    // Inserta en el subárbol izquierdo
    if (key < node->key)
        node->left = insert(node->left, key);

    // Inserta en el subárbol derecho
    else if (key > node->key)
        node->right = insert(node->right, key);

    // No permite claves duplicadas
    else
        return node;

    // Actualiza la altura del nodo
    node->height = 1 + max(getHeight(node->left),
                           getHeight(node->right));

    // Calcula el factor de balance
    int balance = getBalance(node);

    // Caso Izquierda-Izquierda (LL)
    if (balance > 1 && key < node->left->key)
        return rightRotate(node);

    // Caso Derecha-Derecha (RR)
    if (balance < -1 && key > node->right->key)
        return leftRotate(node);

    // Caso Izquierda-Derecha (LR)
    if (balance > 1 && key > node->left->key) {

        node->left = leftRotate(node->left);

        return rightRotate(node);
    }

    // Caso Derecha-Izquierda (RL)
    if (balance < -1 && key < node->right->key) {

        node->right = rightRotate(node->right);

        return leftRotate(node);
    }

    // Si no necesita rotación
    return node;
}

// Recorrido en preorden
void preOrder(Node* root) {

    // Verifica que el nodo exista
    if (root != nullptr) {

        // Visita la raíz
        cout << root->key << " ";

        // Recorre el subárbol izquierdo
        preOrder(root->left);

        // Recorre el subárbol derecho
        preOrder(root->right);
    }
}

// Función principal
int main() {

    // Árbol inicialmente vacío
    Node* root = nullptr;

    // Inserción de elementos
    root = insert(root, 10);
    root = insert(root, 20);
    root = insert(root, 30);
    root = insert(root, 40);

    // Muestra el recorrido en preorden
    cout << "Preorden del árbol AVL: ";

    preOrder(root);

    cout << endl;

    return 0;
}

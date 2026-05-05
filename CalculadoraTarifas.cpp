#include <iostream>
#include <iomanip>

using namespace std;

int main() {
    int tipoUsuario;
    double distancia, tarifaBase, costoKm, total;

    cout << "--- CALCULADORA DE TARIFAS ---" << endl;
    cout << "1. General\n2. Estudiante\n3. Adulto Mayor" << endl;
    cout << "Seleccione tipo de usuario: ";
    cin >> tipoUsuario;

    cout << "Ingrese distancia recorrida (km): ";
    cin >> distancia;

    // Configuración de costos
    switch (tipoUsuario) {
        case 1: // General
            tarifaBase = 1.50;
            costoKm = 0.50;
            break;
        case 2: // Estudiante (50% de descuento en base y km)
            tarifaBase = 0.70;
            costoKm = 0.25;
            break;
        case 3: // Adulto Mayor (Tarifa plana preferencial)
            tarifaBase = 0.50;
            costoKm = 0.15;
            break;
        default:
            cout << "Tipo de usuario no valido." << endl;
            return 1;
    }

    total = tarifaBase + (distancia * costoKm);

    cout << fixed << setprecision(2);
    cout << "\n--- Recibo de Viaje ---" << endl;
    cout << "Tarifa Base: S/ " << tarifaBase << endl;
    cout << "Costo por Distancia: S/ " << (distancia * costoKm) << endl;
    cout << "Total a Pagar: S/ " << total << endl;

    return 0;
}

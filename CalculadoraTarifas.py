def calcular_tarifa():
    # Diccionario de tarifas: {ID: (Nombre, Tarifa Base, Costo por Km)}
    tarifas = {
        1: ("General", 1.50, 0.50),
        2: ("Estudiante", 0.70, 0.25),
        3: ("Adulto Mayor", 0.50, 0.15)
    }

    print("--- SISTEMA DE TARIFAS ---")
    for key, val in tarifas.items():
        print(f"{key}. {val[0]}")

    try:
        opcion = int(input("Seleccione su categoria: "))
        if opcion not in tarifas:
            print("Opcion invalida.")
            return

        distancia = float(input("Kilometros recorridos: "))
        
        nombre, base, km_rate = tarifas[opcion]
        total = base + (distancia * km_rate)

        print("-" * 25)
        print(f"Categoria: {nombre}")
        print(f"Distancia: {distancia} km")
        print(f"Total a pagar: S/ {total:.2f}")
        print("-" * 25)

    except ValueError:
        print("Error: Ingrese valores numericos validos.")

calcular_tarifa()

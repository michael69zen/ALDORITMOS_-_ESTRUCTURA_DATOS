import csv
import os

class Estudiante:
    def __init__(self, id, nombre, correo, escuela, anio_ingreso):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.escuela = escuela
        self.anio_ingreso = anio_ingreso
        self.siguiente = None

class ListaEstudiantes:
    def __init__(self):
        self.cabeza = None
        self.siguiente_id = 1

    def agregar_estudiante(self, nombre, correo, escuela, anio_ingreso):
        nuevo = Estudiante(self.siguiente_id, nombre, correo, escuela, anio_ingreso)
        self.siguiente_id += 1
        
        if self.cabeza is None:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo
        print(f"Estudiante agregado con éxito. ID asignado: {nuevo.id}")

    def mostrar_estudiantes(self):
        if self.cabeza is None:
            print("No hay estudiantes registrados.")
            return
        actual = self.cabeza
        print("--- Lista de Estudiantes ---")
        while actual is not None:
            print(f"ID: {actual.id}")
            print(f"Nombre: {actual.nombre}")
            print(f"Correo: {actual.correo}")
            print(f"Escuela: {actual.escuela}")
            print(f"Año de Ingreso: {actual.anio_ingreso}")
            print("---------------------------")
            actual = actual.siguiente

    def buscar_por_id(self, id_buscar):
        actual = self.cabeza
        while actual is not None:
            if actual.id == id_buscar:
                print("--- Estudiante Encontrado ---")
                print(f"ID: {actual.id}")
                print(f"Nombre: {actual.nombre}")
                print(f"Correo: {actual.correo}")
                print(f"Escuela: {actual.escuela}")
                print(f"Año de Ingreso: {actual.anio_ingreso}")
                return
            actual = actual.siguiente
        print(f"Estudiante con ID {id_buscar} no encontrado.")

    def buscar_por_nombre(self, nombre_buscar):
        actual = self.cabeza
        encontrado = False
        while actual is not None:
            if nombre_buscar.lower() in actual.nombre.lower():
                print("--- Estudiante Encontrado ---")
                print(f"ID: {actual.id}")
                print(f"Nombre: {actual.nombre}")
                print(f"Correo: {actual.correo}")
                print(f"Escuela: {actual.escuela}")
                print(f"Año de Ingreso: {actual.anio_ingreso}")
                encontrado = True
            actual = actual.siguiente
        if not encontrado:
            print(f"Ningún estudiante encontrado con el nombre: {nombre_buscar}")

    def modificar_estudiante(self, id_modificar):
        actual = self.cabeza
        while actual is not None:
            if actual.id == id_modificar:
                print(f"--- Modificando Estudiante ID {id_modificar} ---")
                print("Dejar en blanco (o presionar Enter) para no modificar el campo.")
                
                nombre = input(f"Nombre actual ({actual.nombre}): ")
                if nombre.strip(): actual.nombre = nombre
                
                correo = input(f"Correo actual ({actual.correo}): ")
                if correo.strip(): actual.correo = correo
                
                escuela = input(f"Escuela actual ({actual.escuela}): ")
                if escuela.strip(): actual.escuela = escuela
                
                anio = input(f"Año de Ingreso actual ({actual.anio_ingreso}): ")
                if anio.strip():
                    try:
                        actual.anio_ingreso = int(anio)
                    except ValueError:
                        print("Entrada inválida. El año no se modificó.")
                
                print("Datos actualizados exitosamente.")
                return
            actual = actual.siguiente
        print(f"Estudiante con ID {id_modificar} no encontrado.")

    def eliminar_estudiante(self, id_eliminar):
        if self.cabeza is None:
            print("La lista está vacía.")
            return

        if self.cabeza.id == id_eliminar:
            self.cabeza = self.cabeza.siguiente
            print("Estudiante eliminado exitosamente.")
            return

        actual = self.cabeza
        while actual.siguiente is not None and actual.siguiente.id != id_eliminar:
            actual = actual.siguiente

        if actual.siguiente is not None:
            actual.siguiente = actual.siguiente.siguiente
            print("Estudiante eliminado exitosamente.")
        else:
            print(f"Estudiante con ID {id_eliminar} no encontrado.")

    def guardar_en_archivo(self, filename):
        with open(filename, mode='w', newline='', encoding='utf-8') as archivo:
            writer = csv.writer(archivo)
            writer.writerow(['ID', 'Nombre', 'Correo', 'Escuela', 'Año_Ingreso'])
            actual = self.cabeza
            while actual is not None:
                writer.writerow([actual.id, actual.nombre, actual.correo, actual.escuela, actual.anio_ingreso])
                actual = actual.siguiente
        print(f"Datos guardados en {filename} exitosamente.")

    def cargar_desde_archivo(self, filename):
        if not os.path.exists(filename):
            return
            
        self.cabeza = None
        ultimo = None
        max_id = 0

        with open(filename, mode='r', newline='', encoding='utf-8') as archivo:
            reader = csv.reader(archivo)
            try:
                next(reader) # Saltar el encabezado
            except StopIteration:
                return
                
            for row in reader:
                if len(row) == 5:
                    nuevo = Estudiante(int(row[0]), row[1], row[2], row[3], int(row[4]))
                    if nuevo.id > max_id:
                        max_id = nuevo.id
                        
                    if self.cabeza is None:
                        self.cabeza = nuevo
                        ultimo = nuevo
                    else:
                        ultimo.siguiente = nuevo
                        ultimo = nuevo
                        
        self.siguiente_id = max_id + 1
        print(f"Datos cargados desde {filename} exitosamente.")


def mostrar_menu():
    print("\n=== SISTEMA DE REGISTRO DE ESTUDIANTES ===")
    print("1. Agregar nuevo estudiante")
    print("2. Mostrar todos los estudiantes")
    print("3. Buscar estudiante por ID o nombre")
    print("4. Modificar datos de un estudiante")
    print("5. Eliminar un estudiante")
    print("6. Guardar los datos en archivo .csv")
    print("7. Cargar los datos desde archivo")
    print("8. Salir")
    opcion = input("Seleccione una opción: ")
    return opcion


def main():
    lista = ListaEstudiantes()
    filename = "registros.csv"

    # Cargar datos al iniciar el programa
    lista.cargar_desde_archivo(filename)

    while True:
        opcion = mostrar_menu()

        if opcion == '1':
            nombre = input("Ingrese nombre completo: ")
            correo = input("Ingrese correo electrónico: ")
            escuela = input("Ingrese escuela profesional: ")
            try:
                anio = int(input("Ingrese año de ingreso: "))
                lista.agregar_estudiante(nombre, correo, escuela, anio)
            except ValueError:
                print("El año de ingreso debe ser un número entero.")
        elif opcion == '2':
            lista.mostrar_estudiantes()
        elif opcion == '3':
            subopcion = input("1. Buscar por ID\n2. Buscar por Nombre\nSeleccione: ")
            if subopcion == '1':
                try:
                    id_buscar = int(input("Ingrese ID a buscar: "))
                    lista.buscar_por_id(id_buscar)
                except ValueError:
                    print("Entrada inválida.")
            elif subopcion == '2':
                nombre_buscar = input("Ingrese nombre a buscar: ")
                lista.buscar_por_nombre(nombre_buscar)
            else:
                print("Opción inválida.")
        elif opcion == '4':
            try:
                id_modificar = int(input("Ingrese el ID del estudiante a modificar: "))
                lista.modificar_estudiante(id_modificar)
            except ValueError:
                print("Entrada inválida.")
        elif opcion == '5':
            try:
                id_eliminar = int(input("Ingrese el ID del estudiante a eliminar: "))
                lista.eliminar_estudiante(id_eliminar)
            except ValueError:
                print("Entrada inválida.")
        elif opcion == '6':
            lista.guardar_en_archivo(filename)
        elif opcion == '7':
            lista.cargar_desde_archivo(filename)
        elif opcion == '8':
            print("Guardando datos antes de salir...")
            lista.guardar_en_archivo(filename)
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    main()

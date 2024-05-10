import sqlite3


class Tarea:
    def __init__(self, id_tarea, tarea, estado=False):
        self.id_tarea = id_tarea
        self.tarea = tarea
        self.estado = estado

    def completar_tarea(self):
        self.estado = True

    def __str__(self):
        estado_tarea = "Completada" if self.estado else "Pendiente"
        return f"Tarea {self.id_tarea}: {self.tarea} - {estado_tarea}"


class ListaTareas:
    # Inicializar conexión con BBDD y creación de tabla
    def __init__(self, base_datos):
        self.conexion = sqlite3.connect(base_datos)
        self.cursor = self.conexion.cursor()
        self._crear_tabla()

    def _crear_tabla(self):
        # Creación de la tabla para la lista de tareas
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS tareas (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tarea TEXT NOT NULL,
                    estado INTEGER DEFAULT 0)""")
        self.conexion.commit()

    # ***********FUNCIONES PARA GESTIONAR LA TABLA INSERT, BORRAR, MODIFICAR Y MOSTRAR LISTADO*******************
    def nueva_tarea(self, tarea):
        self.cursor.execute("INSERT INTO tareas (tarea) VALUES (?)", (tarea,))
        self.conexion.commit()

    def borrar_tarea(self, id_tarea):
        try:
            self.cursor.execute("SELECT * FROM tareas WHERE id=?", (id_tarea,))
            tarea = self.cursor.fetchone()
            if tarea is None:
                raise IndexError("La tarea no existe. Consulte el listado y busque la tarea a eliminar.")
            else:
                self.cursor.execute("DELETE FROM tareas WHERE id=?", (id_tarea,))
                self.conexion.commit()
                print("Tarea anotada como completada.")
        except IndexError as e:
            print(str(e))
        except Exception as e:
            print("Error", e)

    def completar_tarea(self, id_tarea):
        # Se envuelve la función en un try que lanzará una excepción en caso de que el id tarea sea erróneo
        try:
            self.cursor.execute("SELECT * FROM tareas WHERE id=?", (id_tarea,))
            tarea = self.cursor.fetchone()
            if tarea is None:
                raise IndexError("La tarea no existe. Consulte el listado y busque la tarea a completar.")
            else:
                self.cursor.execute("UPDATE tareas SET estado=1 WHERE id=?", (id_tarea,))
                self.conexion.commit()
                print("Tarea anotada como completada.")
        except IndexError as e:
            print(str(e))
        except Exception as e:
            print("Error", e)

    # Funciones que obtienen y muestran el listado.
    def listado_tareas(self):
        self.cursor.execute("SELECT * FROM tareas")
        tareas = []
        for fila in self.cursor.fetchall():
            tarea = Tarea(fila[0], fila[1], fila[2])
            tareas.append(tarea)
        return tareas

    def mostrar_listado(self):
        tareas = self.listado_tareas()
        if not tareas:
            print("No hay tareas")
        else:
            for tarea in tareas:
                print(tarea)


lista_tareas = ListaTareas("tareas.db")  # Instanciamos ListaTareas


# menu_tareas crea un menú que permite gestionar todas las funciones mediante consola
def menu_tareas():
    opcion = ""
    while opcion != "0":
        print("\n")
        print("-" * 15 + "LISTADO DE TAREAS" + "-" * 15)
        lista_tareas.mostrar_listado()
        print("\n")
        print("-" * 20 + "MENÚ TAREAS" + "-" * 20)
        print("1. Nueva tarea \n2. Lista tareas \n3. Completar tarea \n4. Borrar tarea \n0. Salir del programa")
        print("-" * 40)
        opcion = input("ELEGIR OPCIÓN: ")
        try:
            opcion = int(opcion)
            if opcion == 1:
                tarea = input("Ingrese tarea: ")
                lista_tareas.nueva_tarea(tarea)
            elif opcion == 2:
                lista_tareas.mostrar_listado()
            elif opcion == 3:
                completa_tarea = int(input("ID de tarea a completar: "))
                lista_tareas.completar_tarea(completa_tarea)
            elif opcion == 4:
                borra_tarea = int(input("ID de tarea a eliminar: "))
                lista_tareas.borrar_tarea(borra_tarea)
            elif opcion == 0:
                print("Hasta pronto!")
                break
            else:
                print("Opción errónea, elija una opción válida")
        except ValueError:
            print("Por favor, ingrese un número válido")
        except IndexError as e:
            print(str(e))
        except Exception as e:
            print("Error", e)


if __name__ == "__main__":
    menu_tareas()

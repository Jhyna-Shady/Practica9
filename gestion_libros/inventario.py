# inventario.py

import pandas as pd
from gestion_libros.libros import Libro

class Inventario:
    def __init__(self, archivo_csv):
        self.libros = {}
        self.archivo_csv = archivo_csv
        self.cargar_libros()

    def cargar_libros(self):
        try:
            datos = pd.read_csv(self.archivo_csv)
            for _, fila in datos.iterrows():
                libro = Libro(fila['titulo'], fila['autor'], str(fila['anio']), fila['genero'], fila['isbn'])
                self.agregar_libro(libro)
        except FileNotFoundError:
            pass

    def guardar_libros(self):
        datos = []
        for libro in self.libros.values():
            datos.append({
                'titulo': libro.titulo,
                'autor': libro.autor,
                'anio': libro.anio,
                'genero': libro.genero,
                'isbn': libro.isbn
            })
        df = pd.DataFrame(datos)
        df.to_csv(self.archivo_csv, index=False)

    def agregar_libro(self, libro):
        if libro.isbn in self.libros:
            raise ValueError("El libro con este ISBN ya existe.")
        self.libros[libro.isbn] = libro
        self.guardar_libros()

    def eliminar_libro(self, titulo):
        for isbn, libro in self.libros.items():
            if libro.titulo.lower() == titulo.lower():
                del self.libros[isbn]
                self.guardar_libros()
                return
        raise ValueError("El libro con este título no se encuentra en el inventario.")

    def buscar_libro(self, titulo):
        for libro in self.libros.values():
            if libro.titulo.lower() == titulo.lower():
                return libro
        return None

    def listar_libros(self):
        if not self.libros:
            print("No hay libros en el inventario.")
        else:
            for libro in self.libros.values():
                print(libro)

    def actualizar_libro(self, titulo, **input):
        libro = self.buscar_libro(titulo)
        if libro:
            for key, value in input.items():
                if hasattr(libro, key):
                    setattr(libro, key, value)
            self.guardar_libros()  # Guardar los cambios al libro en el archivo CSV
        else:
            raise ValueError("El libro con este título no se encuentra en el inventario.")

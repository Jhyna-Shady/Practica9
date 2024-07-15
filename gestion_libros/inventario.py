# inventario.py

import pandas as pd  # Importa Pandas para la manipulación de datos, como leer y escribir archivos CSV
from gestion_libros.libros import Libro  # Importa la clase Libro desde el módulo libros

class Inventario:
    def __init__(self, archivo_csv):
        # Constructor de la clase Inventario
        self.libros = {}  # Inicializa un diccionario vacío para almacenar los libros, usando el ISBN como clave
        self.archivo_csv = archivo_csv  # Guarda la ruta del archivo CSV donde se almacenan los datos del inventario
        self.cargar_libros()  # Llama al método para cargar los libros desde el archivo CSV

    def cargar_libros(self):
        # Método para cargar los libros desde el archivo CSV
        try:
            datos = pd.read_csv(self.archivo_csv)  # Lee el archivo CSV en un DataFrame de Pandas
            for _, fila in datos.iterrows():  # Itera sobre cada fila del DataFrame
                # Crea una instancia de Libro con los datos de la fila
                libro = Libro(fila['titulo'], fila['autor'], str(fila['anio']), fila['genero'], fila['isbn'])
                self.agregar_libro(libro)  # Agrega el libro al inventario
        except FileNotFoundError:
            # Si el archivo CSV no existe, no hace nada (solo pasa)
            pass

    def guardar_libros(self):
        # Método para guardar los libros en el archivo CSV
        datos = []  # Crea una lista vacía para almacenar los datos de los libros
        for libro in self.libros.values():  # Itera sobre todos los libros en el inventario
            datos.append({
                'titulo': libro.titulo,  # Agrega el título del libro
                'autor': libro.autor,  # Agrega el autor del libro
                'anio': libro.anio,  # Agrega el año de publicación del libro
                'genero': libro.genero,  # Agrega el género del libro
                'isbn': libro.isbn  # Agrega el ISBN del libro
            })
        df = pd.DataFrame(datos)  # Crea un DataFrame de Pandas con la lista de datos
        df.to_csv(self.archivo_csv, index=False)  # Guarda el DataFrame en el archivo CSV, sin el índice

    def agregar_libro(self, libro):
        # Método para agregar un nuevo libro al inventario
        if libro.isbn in self.libros:
            # Si el libro ya existe en el inventario (según el ISBN), lanza una excepción
            raise ValueError("El libro con este ISBN ya existe.")
        self.libros[libro.isbn] = libro  # Agrega el libro al diccionario de libros
        self.guardar_libros()  # Guarda los cambios en el archivo CSV

    def eliminar_libro(self, titulo):
        # Método para eliminar un libro del inventario según su título
        for isbn, libro in self.libros.items():  # Itera sobre los libros en el inventario
            if libro.titulo.lower() == titulo.lower():  # Compara el título del libro (ignorando mayúsculas/minúsculas)
                del self.libros[isbn]  # Elimina el libro del diccionario
                self.guardar_libros()  # Guarda los cambios en el archivo CSV
                return  # Sale del método después de eliminar el libro
        raise ValueError("El libro con este título no se encuentra en el inventario.")  # Lanza una excepción si el libro no se encuentra

    def buscar_libro(self, titulo):
        # Método para buscar un libro en el inventario según su título
        for libro in self.libros.values():  # Itera sobre los libros en el inventario
            if libro.titulo.lower() == titulo.lower():  # Compara el título del libro (ignorando mayúsculas/minúsculas)
                return libro  # Devuelve el libro encontrado
        return None  # Devuelve None si el libro no se encuentra

    def listar_libros(self):
        # Método para listar todos los libros en el inventario
        if not self.libros:  # Verifica si el inventario está vacío
            print("No hay libros en el inventario.")  # Imprime un mensaje si no hay libros
        else:
            for libro in self.libros.values():  # Itera sobre los libros en el inventario
                print(libro)  # Imprime la información del libro

    def actualizar_libro(self, titulo, **input):
        # Método para actualizar los datos de un libro existente
        libro = self.buscar_libro(titulo)  # Busca el libro por su título
        if libro:
            for key, value in input.items():  # Itera sobre los pares clave-valor de los datos a actualizar
                if hasattr(libro, key):  # Verifica si el libro tiene el atributo especificado
                    setattr(libro, key, value)  # Actualiza el atributo del libro con el nuevo valor
            self.guardar_libros()  # Guarda los cambios en el archivo CSV
        else:
            raise ValueError("El libro con este título no se encuentra en el inventario.")  # Lanza una excepción si el libro no se encuentra

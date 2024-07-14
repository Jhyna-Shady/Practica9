# inventario.py
# importamos las librerias a usar, para la manipulacion de datos
import pandas as pd

# Importamos la clase Libro desde el módulo gestion_libros.libros
from gestion_libros.libros import Libro

#definimos la clase inventario
class Inventario:
    # constructor que se ejecuta al crear una instancia de la clase
    def _init_(self, archivo_csv):
        self.libros = {} #inicializa vacio, para poder almacenar los libros
        self.archivo_csv = archivo_csv #almacena la ruta del archivo csv
        self.cargar_libros() #llama al metodo cargar libros

    # metodo para cargar los libros desde el archivo csv
    def cargar_libros(self):
        try:
            #lee el archivo csv 
            datos = pd.read_csv(self.archivo_csv)
            #itera sobre cada fila
            for _, fila in datos.iterrows():
                #se crea una instancia de libro 
                libro = Libro(fila['titulo'], fila['autor'], str(fila['anio']), fila['genero'], fila['isbn'])
                #agrega el libro al inventario
                self.agregar_libro(libro)
        except FileNotFoundError:
            # si el archivo no se encuentra no pasa nada
            pass
#metodo para guardar libros 
    
    def guardar_libros(self):
        datos = []
        for libro in self.libros.values():
            #agrega un diccionario con los datos del libro a la lista 
            datos.append({
                'titulo': libro.titulo,
                'autor': libro.autor,
                'anio': libro.anio,
                'genero': libro.genero,
                'isbn': libro.isbn
            })
            #dataframe de pandas con los datos de los libros
        df = pd.DataFrame(datos)
        #guarda el dataframe
        df.to_csv(self.archivo_csv, index=False)
        
    def convertir_csv_a_excel(self):
        df = pd.read_csv(self.archivo_csv)
        df.to_excel(self.archivo_excel, index=False)
    
#metodo para agregar un libro al inventario
    def agregar_libro(self, libro):
        if libro.isbn in self.libros:
            raise ValueError("El libro con este ISBN ya existe.")
        self.libros[libro.isbn] = libro #agrega el libro
        self.guardar_libros()
        
#metod para eliminar un libro
    def eliminar_libro(self, titulo):
        for isbn, libro in self.libros.items():
            if libro.titulo.lower() == titulo.lower():
                del self.libros[isbn] #elimina el libro
                self.guardar_libros()
                return
        raise ValueError("El libro con este título no se encuentra en el inventario.")

    #metodo para buscar un libro
    def buscar_libro(self, titulo):
        #itera sobre cada libro del inventario por su titulo
        for libro in self.libros.values():
            if libro.titulo.lower() == titulo.lower():
                return libro
        return None

    #metodo para listar los libros
    def listar_libros(self):
        if not self.libros:
            print("No hay libros en el inventario.")
        else:
            for libro in self.libros.values():
                print(libro)

    #metodo para actualizar los libros
    def actualizar_libro(self, titulo, **input):
        libro = self.buscar_libro(titulo)
        if libro:
            for key, value in input.items():
                if hasattr(libro, key):
                    setattr(libro, key, value)
            self.guardar_libros()  # Guardar los cambios al libro en el archivo CSV
        else:
            raise ValueError("El libro con este título no se encuentra en el inventario.")

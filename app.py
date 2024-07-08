# app.py

import streamlit as st
import pandas as pd
from administrar_libros import Libro
from administrar_libros import Inventario

# Definir la clase Inventario con funcionalidades para cargar y guardar datos desde/hacia CSV
class InventarioCSV(Inventario):
    def __init__(self, archivo_csv):
        """
        Inicializa el inventario cargando los datos desde un archivo CSV.
        
        :param archivo_csv: El archivo CSV donde se guardan los datos del inventario.
        """
        super().__init__()
        self.archivo_csv = archivo_csv
        self.cargar_libros()

    def cargar_libros(self):
        """
        Carga los libros desde el archivo CSV y los añade al inventario.
        """
        try:
            datos = pd.read_csv(self.archivo_csv)
            for _, fila in datos.iterrows():
                libro = Libro(fila['titulo'], fila['autor'], str(fila['anio']), fila['genero'], fila['isbn'])
                self.agregar_libro(libro)
        except FileNotFoundError:
            # Si el archivo no existe, no hace nada, solo lo crea al guardar los datos
            pass

    def guardar_libros(self):
        """
        Guarda los libros en el archivo CSV.
        """
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
        """
        Sobrescribe el método para agregar un libro y guarda los cambios en el archivo CSV.
        
        :param libro: Una instancia de la clase Libro.
        :raises ValueError: Si el ISBN del libro ya existe en el inventario.
        """
        super().agregar_libro(libro)
        self.guardar_libros()

    def eliminar_libro(self, isbn):
        """
        Sobrescribe el método para eliminar un libro y guarda los cambios en el archivo CSV.
        
        :param isbn: El ISBN del libro a eliminar.
        :raises ValueError: Si el libro con este ISBN no se encuentra en el inventario.
        """
        super().eliminar_libro(isbn)
        self.guardar_libros()

    def actualizar_libro(self, isbn, **input):
        """
        Sobrescribe el método para actualizar un libro y guarda los cambios en el archivo CSV.
        
        :param isbn: El ISBN del libro a actualizar.
        :param input: Los datos a actualizar (título, autor, año, género).
        :raises ValueError: Si el libro con este ISBN no se encuentra en el inventario.
        """
        super().actualizar_libro(isbn, **input)
        self.guardar_libros()

# Inicializa el inventario con un archivo CSV
archivo_csv = 'inventario_libros.csv'
inventario = InventarioCSV(archivo_csv)

# Configura la aplicación Streamlit
st.title("Gestión de Libros")

# Menú lateral para seleccionar la opción deseada
opcion = st.sidebar.selectbox(
    "Selecciona una opción",
    ["Agregar Libro", "Eliminar Libro", "Buscar Libro", "Listar Libros", "Actualizar Libro", "Descargar CSV"]
)

# Funcionalidad para agregar un libro
if opcion == "Agregar Libro":
    st.header("Agregar Nuevo Libro")
    titulo = st.text_input("Título")
    autor = st.text_input("Autor")
    anio = st.text_input("Año")
    genero = st.text_input("Género")
    isbn = st.text_input("ISBN")

    if st.button("Agregar Libro"):
        try:
            if not anio.isdigit():
                raise ValueError("El año debe ser un número.")
            libro = Libro(titulo, autor, anio, genero, isbn)
            inventario.agregar_libro(libro)
            st.success("Libro agregado exitosamente.")
        except ValueError as e:
            st.error(f"Error al agregar libro: {e}")

# Funcionalidad para eliminar un libro
elif opcion == "Eliminar Libro":
    st.header("Eliminar Libro")
    isbn = st.text_input("ISBN del libro a eliminar")

    if st.button("Eliminar Libro"):
        try:
            inventario.eliminar_libro(isbn)
            st.success("Libro eliminado exitosamente.")
        except ValueError as e:
            st.error(f"Error al eliminar libro: {e}")

# Funcionalidad para buscar un libro
elif opcion == "Buscar Libro":
    st.header("Buscar Libro")
    titulo = st.text_input("Título del libro a buscar")

    if st.button("Buscar Libro"):
        libro = inventario.buscar_libro(titulo)
        if libro:
            st.write("Libro encontrado:", libro)
        else:
            st.write("Libro no encontrado.")

# Funcionalidad para listar todos los libros
elif opcion == "Listar Libros":
    st.header("Listado de Libros")
    libros = [libro for libro in inventario.libros.values()]
    if libros:
        for libro in libros:
            st.write(libro)
    else:
        st.write("No hay libros en el inventario.")

# Funcionalidad para actualizar un libro
elif opcion == "Actualizar Libro":
    st.header("Actualizar Libro")
    isbn = st.text_input("ISBN del libro a actualizar")

    if st.button("Buscar Libro"):
        libro = inventario.buscar_libro_por_isbn(isbn)
        if libro:
            nuevo_titulo = st.text_input("Nuevo título", value=libro.titulo)
            nuevo_autor = st.text_input("Nuevo autor", value=libro.autor)
            nuevo_anio = st.text_input("Nuevo año", value=libro.anio)
            nuevo_genero = st.text_input("Nuevo género", value=libro.genero)

            if st.button("Actualizar Libro"):
                try:
                    kwargs = {}
                    if nuevo_titulo != libro.titulo: kwargs['titulo'] = nuevo_titulo
                    if nuevo_autor != libro.autor: kwargs['autor'] = nuevo_autor
                    if nuevo_anio != libro.anio:
                        if not nuevo_anio.isdigit():
                            raise ValueError("El año debe ser un número.")
                        kwargs['anio'] = nuevo_anio
                    if nuevo_genero != libro.genero: kwargs['genero'] = nuevo_genero

                    inventario.actualizar_libro(isbn, **kwargs)
                    st.success("Libro actualizado exitosamente.")
                except ValueError as e:
                    st.error(f"Error al actualizar libro: {e}")
        else:
            st.write("Libro no encontrado.")

# Funcionalidad para descargar el listado de libros en CSV
elif opcion == "Descargar CSV":
    st.header("Descargar Listado de Libros en CSV")

    # Crea un DataFrame con los libros actuales
    datos = []
    for libro in inventario.libros.values():
        datos.append({
            'titulo': libro.titulo,
            'autor': libro.autor,
            'anio': libro.anio,
            'genero': libro.genero,
            'isbn': libro.isbn
        })
    df = pd.DataFrame(datos)

    # Crea un archivo CSV en memoria
    csv = df.to_csv(index=False)

    # Botón para descargar el archivo CSV
    st.download_button(
        label="Descargar CSV",
        data=csv,
        file_name='inventario_libros.csv',
        mime='text/csv'
    )

# app.py

# Importar las bibliotecas necesarias
import streamlit as st  # Importa Streamlit para crear la interfaz web
import pandas as pd  # Importa Pandas para la manipulación de datos
from gestion_libros.inventario import Inventario, Libro  # Importa las clases Inventario y Libro de otro módulo
from io import BytesIO  # Importa BytesIO para manipular datos binarios en memoria

# Configurar el inventario con el archivo CSV
archivo_csv = 'inventario_libros.csv'  # Define la ruta del archivo CSV donde se almacena el inventario
inventario = Inventario(archivo_csv)  # Crea una instancia de la clase Inventario usando el archivo CSV

# Configurar la aplicación Streamlit
st.title("Gestión de Libros")  # Establece el título de la aplicación en la interfaz web

# Definir las opciones como pestañas
tabs = st.tabs(["Agregar Libro", "Eliminar Libro", "Buscar Libro", "Listar Libros", "Actualizar Libro", "Descargar"])
# Crea un conjunto de pestañas en la interfaz web con diferentes opciones para gestionar el inventario de libros

# Pestaña para agregar un libro
with tabs[0]:  # Selecciona la primera pestaña llamada "Agregar Libro"
    st.header("Agregar Nuevo Libro")  # Muestra el encabezado para esta pestaña
    with st.form(key='agregar_libro_form'):  # Crea un formulario para ingresar los datos del nuevo libro
        # Campos para ingresar la información del libro
        titulo = st.text_input("Título")  # Campo de texto para ingresar el título del libro
        autor = st.text_input("Autor")  # Campo de texto para ingresar el autor del libro
        anio = st.text_input("Año")  # Campo de texto para ingresar el año de publicación del libro
        genero = st.text_input("Género")  # Campo de texto para ingresar el género del libro
        isbn = st.text_input("ISBN")  # Campo de texto para ingresar el ISBN del libro

        if st.form_submit_button("Agregar Libro"):  # Botón para enviar el formulario
            try:
                if not anio.isdigit():  # Verifica que el año ingresado sea un número
                    raise ValueError("El año debe ser un número.")  # Lanza una excepción si el año no es un número
                libro = Libro(titulo, autor, anio, genero, isbn)  # Crea una instancia de la clase Libro con los datos ingresados
                inventario.agregar_libro(libro)  # Llama al método para agregar el libro al inventario
                st.success("Libro agregado exitosamente.")  # Muestra un mensaje de éxito si el libro se agrega correctamente
            except ValueError as e:
                st.error(f"Error al agregar libro: {e}")  # Muestra un mensaje de error si ocurre una excepción

# Pestaña para eliminar un libro
with tabs[1]:  # Selecciona la segunda pestaña llamada "Eliminar Libro"
    st.header("Eliminar Libro")  # Muestra el encabezado para esta pestaña
    with st.form(key='eliminar_libro_form'):  # Crea un formulario para ingresar el título del libro a eliminar
        titulo_eliminar = st.text_input("Título del libro a eliminar")  # Campo de texto para ingresar el título del libro a eliminar

        if st.form_submit_button("Eliminar Libro"):  # Botón para enviar el formulario
            try:
                libro_encontrado = inventario.buscar_libro(titulo_eliminar)  # Busca el libro por el título ingresado
                if libro_encontrado:  # Verifica si el libro existe en el inventario
                    inventario.eliminar_libro(libro_encontrado.titulo)  # Llama al método para eliminar el libro del inventario
                    st.success("Libro eliminado exitosamente.")  # Muestra un mensaje de éxito si el libro se elimina correctamente
                else:
                    st.error("El libro con este título no se encuentra en el inventario.")  # Muestra un mensaje de error si el libro no está en el inventario
            except ValueError as e:
                st.error(f"Error al eliminar libro: {e}")  # Muestra un mensaje de error si ocurre una excepción

# Pestaña para buscar un libro
with tabs[2]:  # Selecciona la tercera pestaña llamada "Buscar Libro"
    st.header("Buscar Libro")  # Muestra el encabezado para esta pestaña
    with st.form(key='buscar_libro_form'):  # Crea un formulario para ingresar el título del libro a buscar
        titulo_buscar = st.text_input("Título del libro a buscar")  # Campo de texto para ingresar el título del libro a buscar

        if st.form_submit_button("Buscar Libro"):  # Botón para enviar el formulario
            libro = inventario.buscar_libro(titulo_buscar)  # Busca el libro por el título ingresado
            if libro:  # Verifica si el libro existe en el inventario
                st.write("Libro encontrado:", libro)  # Muestra la información del libro encontrado
            else:
                st.write("Libro no encontrado.")  # Muestra un mensaje si el libro no está en el inventario

# Pestaña para listar todos los libros
with tabs[3]:  # Selecciona la cuarta pestaña llamada "Listar Libros"
    st.header("Listado de Libros")  # Muestra el encabezado para esta pestaña
    libros = [libro for libro in inventario.libros.values()]  # Obtiene todos los libros del inventario como una lista
    if libros:  # Verifica si hay libros en el inventario
        for libro in libros:  # Itera sobre cada libro en la lista
            st.write(libro)  # Muestra la información del libro
    else:
        st.write("No hay libros en el inventario.")  # Muestra un mensaje si no hay libros en el inventario

# Pestaña para actualizar un libro
with tabs[4]:  # Selecciona la quinta pestaña llamada "Actualizar Libro"
    st.header("Actualizar Libro")  # Muestra el encabezado para esta pestaña
    with st.form(key='actualizar_libro_form'):  # Crea un formulario para ingresar el título del libro a actualizar
        titulo_actualizar = st.text_input("Título del libro a actualizar")  # Campo de texto para ingresar el título del libro a actualizar

        if st.form_submit_button("Buscar Libro"):  # Botón para enviar el formulario y buscar el libro a actualizar
            libro = inventario.buscar_libro(titulo_actualizar)  # Busca el libro por el título ingresado
            if libro:  # Verifica si el libro existe en el inventario
                # Campos para ingresar los nuevos datos del libro, con valores predeterminados de los datos actuales
                nuevo_titulo = st.text_input("Nuevo título", value=libro.titulo)
                nuevo_autor = st.text_input("Nuevo autor", value=libro.autor)
                nuevo_anio = st.text_input("Nuevo año", value=libro.anio)
                nuevo_genero = st.text_input("Nuevo género", value=libro.genero)

                # Mostrar un mensaje de confirmación antes de actualizar
                if st.form_submit_button("Actualizar Libro"):  # Botón para enviar el formulario y actualizar el libro
                    try:
                        kwargs = {}  # Crea un diccionario vacío para almacenar los cambios
                        # Verifica si cada campo ha cambiado y agrega los cambios al diccionario
                        if nuevo_titulo != libro.titulo:
                            kwargs['titulo'] = nuevo_titulo
                        if nuevo_autor != libro.autor:
                            kwargs['autor'] = nuevo_autor
                        if nuevo_anio != libro.anio:
                            if not nuevo_anio.isdigit():  # Verifica que el nuevo año sea un número
                                raise ValueError("El año debe ser un número.")  # Lanza una excepción si el año no es un número
                            kwargs['anio'] = nuevo_anio
                        if nuevo_genero != libro.genero:
                            kwargs['genero'] = nuevo_genero

                        inventario.actualizar_libro(titulo_actualizar, **kwargs)  # Llama al método para actualizar el libro en el inventario
                        inventario.guardar_libros()  # Guarda los cambios en el archivo CSV
                        st.success("Libro actualizado exitosamente.")  # Muestra un mensaje de éxito si el libro se actualiza correctamente
                    except ValueError as e:
                        st.error(f"Error al actualizar libro: {e}")  # Muestra un mensaje de error si ocurre una excepción

            else:
                st.error("El libro con este título no se encuentra en el inventario.")  # Muestra un mensaje de error si el libro no está en el inventario

# Pestaña para descargar el inventario como CSV o Excel
with tabs[5]:  # Selecciona la sexta pestaña llamada "Descargar"
    st.header("Descargar Inventario")  # Muestra el encabezado para esta pestaña

    if st.button("Generar CSV"):  # Botón para generar el archivo CSV
        df = pd.read_csv(archivo_csv)  # Lee el archivo CSV en un DataFrame de Pandas
        csv = df.to_csv(index=False)  # Convierte el DataFrame a un formato CSV en una cadena de texto
        st.download_button(  # Crea un botón para descargar el archivo CSV
            label="Descargar CSV",
            data=csv,
            file_name='inventario_libros.csv',
            mime='text/csv'
        )
        st.success("Inventario generado como CSV correctamente.")  # Muestra un mensaje de éxito después de generar el archivo CSV

    if st.button("Generar EXCEL"):  # Botón para generar el archivo Excel
        df = pd.read_csv(archivo_csv)  # Lee el archivo CSV en un DataFrame de Pandas
        output = BytesIO()  # Crea un objeto BytesIO para almacenar el archivo Excel en memoria
        writer = pd.ExcelWriter(output, engine='xlsxwriter')  # Crea un escritor Excel con el motor 'xlsxwriter'
        df.to_excel(writer, index=False, sheet_name='Inventario')  # Escribe el DataFrame en una hoja llamada 'Inventario'
        writer.close()  # Cierra el escritor Excel
        output.seek(0)  # Vuelve al inicio del objeto BytesIO para leer su contenido
        st.download_button(  # Crea un botón para descargar el archivo Excel
            label="Descargar EXCEL",
            data=output,
            file_name='inventario_libros.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        st.success("Inventario generado como EXCEL correctamente.")  # Muestra un mensaje de éxito después de generar el archivo Excel

# gestion_libros.py

# Definición de la clase Libro para representar un libro en el inventario
class Libro:
    def __init__(self, titulo, autor, anio, genero, isbn):
        """
        Inicializa un nuevo libro con los datos proporcionados.
        
        :param titulo: El título del libro.
        :param autor: El autor del libro.
        :param anio: El año de publicación del libro. Debe ser un número.
        :param genero: El género del libro.
        :param isbn: El ISBN del libro. Este debe ser único.
        :raises ValueError: Si el año no es un número.
        """
        if not anio.isdigit():
            raise ValueError("El año debe ser un número.")
        self.titulo = titulo
        self.autor = autor
        self.anio = anio
        self.genero = genero
        self.isbn = isbn

    def __str__(self):
        """
        Representación en cadena del libro.
        
        :return: Cadena que describe el libro con su título, autor, año, género e ISBN.
        """
        return f"{self.titulo}, {self.autor}, {self.anio}, {self.genero}, ISBN: {self.isbn}"

# Definición de la clase Inventario para gestionar una colección de libros
class Inventario:
    def __init__(self):
        """
        Inicializa un nuevo inventario vacío.
        """
        self.libros = {}

    def agregar_libro(self, libro):
        """
        Agrega un nuevo libro al inventario.
        
        :param libro: Una instancia de la clase Libro.
        :raises ValueError: Si el ISBN del libro ya existe en el inventario.
        """
        if libro.isbn in self.libros:
            raise ValueError("El libro con este ISBN ya existe.")
        self.libros[libro.isbn] = libro

    def eliminar_libro(self, isbn):
        """
        Elimina un libro del inventario por su ISBN.
        
        :param isbn: El ISBN del libro a eliminar.
        :raises ValueError: Si el libro con este ISBN no se encuentra en el inventario.
        """
        if isbn in self.libros:
            del self.libros[isbn]
        else:
            raise ValueError("El libro con este ISBN no se encuentra en el inventario.")

    def buscar_libro(self, titulo):
        """
        Busca un libro en el inventario por su título.
        
        :param titulo: El título del libro a buscar.
        :return: La instancia del libro si se encuentra, None si no se encuentra.
        """
        for libro in self.libros.values():
            if libro.titulo.lower() == titulo.lower():
                return libro
        return None

    def buscar_libro_por_isbn(self, isbn):
        """
        Busca un libro en el inventario por su ISBN.
        
        :param isbn: El ISBN del libro a buscar.
        :return: La instancia del libro si se encuentra, None si no se encuentra.
        """
        return self.libros.get(isbn, None)

    def listar_libros(self):
        """
        Lista todos los libros en el inventario.
        """
        if not self.libros:
            print("No hay libros en el inventario.")
        else:
            for libro in self.libros.values():
                print(libro)

    def actualizar_libro(self, isbn, **input):
        """
        Actualiza los datos de un libro en el inventario.
        
        :param isbn: El ISBN del libro a actualizar.
        :param input: Los datos a actualizar (título, autor, año, género).
        :raises ValueError: Si el libro con este ISBN no se encuentra en el inventario.
        """
        libro = self.buscar_libro_por_isbn(isbn)
        if libro:
            for key, value in input.items():
                if hasattr(libro, key):
                    setattr(libro, key, value)
        else:
            raise ValueError("El libro con este ISBN no se encuentra en el inventario.")

# Funciones para manejar la interacción con el usuario
def main():
    """
    Función principal que proporciona un menú de opciones para el usuario.
    """
    inventario = Inventario()

    while True:
        print("\nMenú de opciones:")
        print("1. Agregar libro")
        print("2. Eliminar libro")
        print("3. Buscar libro")
        print("4. Listar libros")
        print("5. Actualizar libro")
        print("6. Salir")
        
        opcion = input("Elija una opción: ")
        
        try:
            if opcion == '1':
                agregar_libro(inventario)
            elif opcion == '2':
                eliminar_libro(inventario)
            elif opcion == '3':
                buscar_libro(inventario)
            elif opcion == '4':
                listar_libros(inventario)
            elif opcion == '5':
                actualizar_libro(inventario)
            elif opcion == '6':
                print("Saliendo del programa.")
                break
            else:
                print("Opción no válida. Intente de nuevo.")
        except ValueError as e:
            print(f"Error de valor: {e}")
        except Exception as e:
            print(f"Se produjo un error inesperado: {e}")

def agregar_libro(inventario):
    """
    Solicita los datos de un nuevo libro al usuario y lo agrega al inventario.
    
    :param inventario: Una instancia de la clase Inventario.
    """
    try:
        titulo = input("Título: ")
        autor = input("Autor: ")
        anio = input("Año: ")
        genero = input("Género: ")
        isbn = input("ISBN: ")
        if not anio.isdigit():
            raise ValueError("El año debe ser un número.")
        libro = Libro(titulo, autor, anio, genero, isbn)
        inventario.agregar_libro(libro)
        print("Libro agregado.")
    except ValueError as e:
        print(f"Error al agregar libro: {e}")

def eliminar_libro(inventario):
    """
    Solicita el ISBN de un libro al usuario y lo elimina del inventario.
    
    :param inventario: Una instancia de la clase Inventario.
    """
    try:
        isbn = input("ISBN del libro a eliminar: ")
        inventario.eliminar_libro(isbn)
        print("Libro eliminado.")
    except ValueError as e:
        print(f"Error al eliminar libro: {e}")

def buscar_libro(inventario):
    """
    Solicita el título de un libro al usuario y muestra los datos del libro si se encuentra en el inventario.
    
    :param inventario: Una instancia de la clase Inventario.
    """
    try:
        titulo = input("Título del libro a buscar: ")
        libro = inventario.buscar_libro(titulo)
        if libro:
            print("Libro encontrado:", libro)
        else:
            print("Libro no encontrado.")
    except Exception as e:
        print(f"Error al buscar libro: {e}")

def listar_libros(inventario):
    """
    Muestra todos los libros en el inventario.
    
    :param inventario: Una instancia de la clase Inventario.
    """
    try:
        print("Listado de libros en el inventario:")
        inventario.listar_libros()
    except Exception as e:
        print(f"Error al listar libros: {e}")

def actualizar_libro(inventario):
    """
    Solicita los datos de actualización de un libro al usuario y actualiza el libro en el inventario.
    
    :param inventario: Una instancia de la clase Inventario.
    """
    try:
        isbn = input("ISBN del libro a actualizar: ")
        print("Ingrese los nuevos datos (deje en blanco para mantener el valor actual):")
        nuevo_titulo = input("Nuevo título: ")
        nuevo_autor = input("Nuevo autor: ")
        nuevo_anio = input("Nuevo año: ")
        nuevo_genero = input("Nuevo género: ")
        
        kwargs = {}
        if nuevo_titulo: kwargs['titulo'] = nuevo_titulo
        if nuevo_autor: kwargs['autor'] = nuevo_autor
        if nuevo_anio:
            if not nuevo_anio.isdigit():
                raise ValueError("El año debe ser un número.")
            kwargs['anio'] = nuevo_anio
        if nuevo_genero: kwargs['genero'] = nuevo_genero
        
        inventario.actualizar_libro(isbn, **kwargs)
        print("Libro actualizado.")
    except ValueError as e:
        print(f"Error al actualizar libro: {e}")
    except Exception as e:
        print(f"Error inesperado al actualizar libro: {e}")

# Llama a la función principal para iniciar el programa
if __name__ == "__main__":
    main()

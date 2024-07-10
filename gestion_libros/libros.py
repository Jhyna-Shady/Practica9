# gestion_libros/libros.py

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
        return f"{self.titulo}, {self.autor}, {self.anio}, {self.genero}, {self.isbn}"

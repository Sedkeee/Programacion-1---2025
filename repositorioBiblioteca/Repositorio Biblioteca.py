from abc import ABC, abstractmethod
from datetime import datetime, timedelta
#Rafael Angel Hernandez Gomez
#Juan Jose Herrera Largo
# =========================
# 1. Abstracción
# =========================
class MaterialBiblioteca(ABC):
    def __init__(self, titulo, autor, anio):
        self.__titulo = titulo      # Atributos privados (encapsulamiento)
        self.__autor = autor
        self.__anio = anio
        self.__disponible = True

    # encapsulamiento
    def get_titulo(self):
        return self.__titulo

    def get_autor(self):
        return self.__autor

    def get_anio(self):
        return self.__anio

    def esta_disponible(self):
        return self.__disponible

    def prestar(self):
        if self.__disponible:
            self.__disponible = False
            return True
        return False

    def devolver(self):
        self.__disponible = True

    def obtener_informacion(self):
        return (f"Titulo: {self.__titulo} \nAutor: {self.__autor} \nAnio: {self.__anio} \nDisponible: {"Si" if self.__disponible else "No"}")

    @abstractmethod
    def calcular_fecha_devolucion(self):
        pass
    
    @abstractmethod
    def obtener_tipo(self):
        pass

# =========================
# 2. Herencia y Polimorfismo
# =========================
class Libro(MaterialBiblioteca):
    def calcular_fecha_devolucion(self):
        return datetime.now() + timedelta(days=15)  # 15 días de préstamo

    def obtener_tipo(self):
        return "Libro"

class Revista(MaterialBiblioteca):
    def calcular_fecha_devolucion(self):
        return datetime.now() + timedelta(days=7)   # 7 días de préstamo
    
    def obtener_tipo(self):
        return "Revista"

class MaterialAudiovisual(MaterialBiblioteca):
    def calcular_fecha_devolucion(self):
        return datetime.now() + timedelta(days=3)   # 3 días de préstamo
    
    def obtener_tipo(self):
        return "Material Audiovisual"

# =========================
# Clase Usuario
# =========================
class Usuario:
    def __init__(self, nombre, identificacion):
        self.__nombre = nombre
        self.__id = identificacion
        self.__prestamos = []

    def get_nombre(self):
        return self.__nombre

    def get_id(self):
        return self.__id

    def agregar_prestamo(self, prestamo):
        self.__prestamos.append(prestamo)

    def listar_prestamos(self):
        return self.__prestamos

# =========================
# Clase Préstamo
# =========================
class Prestamo:
    def __init__(self, usuario, material):
        self.usuario = usuario
        self.material = material
        self.fecha_prestamo = datetime.now()
        self.fecha_devolucion = material.calcular_fecha_devolucion()

    def __str__(self):
        return f"{self.material.get_titulo()} prestado a {self.usuario.get_nombre()} hasta {self.fecha_devolucion.strftime('%d-%m-%Y')}"

# =========================
# Sistema Biblioteca
# =========================
class Biblioteca:
    def __init__(self):
        self.materiales = []
        self.usuarios = []
        self.prestamos = []

    def agregar_material(self, material):
        self.materiales.append(material)

    def registrar_usuario(self, usuario):
        self.usuarios.append(usuario)

    def realizar_prestamo(self, usuario, material):
        if material.esta_disponible():
            material.prestar()
            prestamo = Prestamo(usuario, material)
            usuario.agregar_prestamo(prestamo)
            self.prestamos.append(prestamo)
            print("Préstamo realizado con éxito:", prestamo)
        else:
            print("El material no está disponible.")

    def devolver_material(self, material):
        material.devolver()
        print(f"Material '{material.get_titulo()}' devuelto correctamente.")

# =========================
# Ejemplo de uso
# =========================
if __name__ == "__main__":
    # Crear biblioteca
    biblio = Biblioteca()

    # Agregar materiales
    libro1 = Libro("Cien Años de Soledad", "Gabriel García Márquez", 1967)
    revista1 = Revista("National Geographic", "Varios", 2023)
    dvd1 = MaterialAudiovisual("Inception", "Christopher Nolan", 2010)

    biblio.agregar_material(libro1)
    biblio.agregar_material(revista1)
    biblio.agregar_material(dvd1)

    # Registrar usuarios
    usuario1 = Usuario("Rafael Angel", "123")
    biblio.registrar_usuario(usuario1)

    # Realizar préstamos
    biblio.realizar_prestamo(usuario1, libro1)
    biblio.realizar_prestamo(usuario1, revista1)

    # Intentar prestar un material ya prestado
    biblio.realizar_prestamo(usuario1, libro1)

    # Devolver material
    biblio.devolver_material(libro1)
    
    #informacion del ejemplo
    print(libro1.obtener_informacion())
    print(revista1.obtener_informacion())
    print(dvd1.obtener_informacion())


#Rafael Angel Hernandez Gomez
#Juan Jose Herrera Largo

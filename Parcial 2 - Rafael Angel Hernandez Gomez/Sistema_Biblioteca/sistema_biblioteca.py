#!/usr/bin/env python3
"""
Nombre: Rafael Angel Hernandez Gomez
Sistema de Biblioteca — Parte 2 del examen

"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Tuple
import os


# =====================================================
# 1. EXCEPCIONES PERSONALIZADAS
# =====================================================
# Se definen para que el sistema lance errores más descriptivos
# en lugar de usar excepciones genéricas como ValueError o KeyError.
class ErrorBiblioteca(Exception):
    """Clase base para todas las excepciones personalizadas de la biblioteca."""
    pass


class LibroNoEncontrado(ErrorBiblioteca):
    """Se lanza cuando se busca un ISBN inexistente."""
    def __init__(self, isbn):
        super().__init__(f"Libro con ISBN {isbn} no encontrado")


class LibroNoDisponible(ErrorBiblioteca):
    """Se lanza cuando no quedan copias disponibles para préstamo."""
    def __init__(self, isbn, titulo):
        super().__init__(f"No hay copias disponibles de '{titulo}'")


class UsuarioNoRegistrado(ErrorBiblioteca):
    """Se lanza cuando se intenta operar con un usuario inexistente."""
    def __init__(self, id_usuario):
        super().__init__(f"Usuario con ID '{id_usuario}' no está registrado")


class LimitePrestamosExcedido(ErrorBiblioteca):
    """Se lanza cuando un usuario intenta superar su límite de préstamos."""
    def __init__(self, id_usuario, limite):
        super().__init__(f"Usuario {id_usuario} excede límite de {limite} préstamos")


class PrestamoVencido(ErrorBiblioteca):
    """Se lanza cuando se intenta renovar un préstamo que ya está vencido."""
    def __init__(self, id_prestamo, dias_retraso):
        super().__init__(f"Préstamo {id_prestamo} está vencido por {dias_retraso} días")


# =====================================================
# 2. CLASE PRINCIPAL: SistemaBiblioteca
# =====================================================
class SistemaBiblioteca:
    """
    Esta clase concentra toda la lógica del sistema de biblioteca.
    Usa estructuras de datos en memoria para mantener:
      - Catálogo de libros
      - Usuarios registrados
      - Préstamos activos y su historial
    """

    def __init__(self, dias_prestamo: int = 14, multa_por_dia: float = 1.0, limite_prestamos: int = 3):
        """
        Inicializa los parámetros generales del sistema y sus estructuras internas.
        """
        # Diccionario principal del catálogo:
        # { ISBN: { titulo, autor, anio, categoria, copias_total, copias_disponibles, veces_prestado } }
        self.catalogo: Dict[str, Dict[str, Any]] = {}

        # Diccionario de usuarios:
        # { id_usuario: { nombre, email, prestamos_activos, historial_prestamos, multas_pendientes } }
        self.usuarios: Dict[str, Dict[str, Any]] = {}

        # Diccionario de préstamos:
        # { id_prestamo: { isbn, id_usuario, fecha_prestamo, fecha_vencimiento, fecha_devolucion, multa } }
        self.prestamos: Dict[str, Dict[str, Any]] = {}

        # Contador para generar IDs automáticos de préstamos
        self._contador_prestamos = 0

        # Parámetros generales configurables
        self.dias_prestamo = dias_prestamo
        self.multa_por_dia = multa_por_dia
        self.limite_prestamos = limite_prestamos

    # =====================================================
    # 3. FUNCIONES AUXILIARES INTERNAS
    # =====================================================
    def _generar_id_prestamo(self) -> str:
        """
        Genera un ID secuencial con formato P000001, P000002, etc.
        """
        self._contador_prestamos += 1
        return f"P{self._contador_prestamos:06d}"

    @staticmethod
    def _validar_isbn(isbn: str):
        """Verifica que el ISBN tenga 13 dígitos numéricos."""
        if not isinstance(isbn, str) or len(isbn) != 13 or not isbn.isdigit():
            raise ValueError("ISBN inválido: debe ser una cadena de 13 dígitos")

    @staticmethod
    def _validar_email(email: str):
        """Valida que el email contenga '@' y un dominio con punto."""
        if not isinstance(email, str) or "@" not in email:
            raise ValueError("Email inválido")
        try:
            local, domain = email.split("@", 1)
        except Exception:
            raise ValueError("Email inválido")
        if "." not in domain:
            raise ValueError("Email inválido")

    # =====================================================
    # 4. GESTIÓN DEL CATÁLOGO
    # =====================================================
    def agregar_libro(self, isbn: str, titulo: str, autor: str, anio: int, categoria: str, copias: int = 1):
        """
        Añade un libro al catálogo después de validar los datos básicos.
        """
        self._validar_isbn(isbn)
        if not titulo or not autor:
            raise ValueError("Título y autor no pueden estar vacíos")

        ahora = datetime.now()
        if not (1000 <= int(anio) <= ahora.year):
            raise ValueError("Año inválido")
        if copias < 1:
            raise ValueError("Debe añadirse al menos 1 copia")
        if isbn in self.catalogo:
            raise KeyError(f"ISBN {isbn} ya existe")

        # Si todo es correcto, se agrega el libro al diccionario
        self.catalogo[isbn] = {
            "titulo": titulo,
            "autor": autor,
            "anio": int(anio),
            "categoria": categoria or "",
            "copias_total": int(copias),
            "copias_disponibles": int(copias),
            "veces_prestado": 0,
        }
        return True

    def actualizar_copias(self, isbn: str, cambio: int):
        """
        Permite aumentar o disminuir la cantidad de copias totales de un libro.
        Si se intenta dejar menos copias que las actualmente prestadas, se lanza un error.
        """
        if isbn not in self.catalogo:
            raise LibroNoEncontrado(isbn)

        entry = self.catalogo[isbn]
        nuevo_total = entry["copias_total"] + cambio
        prestadas = entry["copias_total"] - entry["copias_disponibles"]

        if nuevo_total < prestadas:
            raise ValueError("No se puede reducir copias por debajo de las ya prestadas")

        entry["copias_total"] = nuevo_total
        entry["copias_disponibles"] = nuevo_total - prestadas
        return True

    def buscar_libros(self, criterio: str, valor: Any, categoria: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Permite buscar libros por título, autor o año, con opción de filtrar por categoría.
        La búsqueda es parcial (insensible a mayúsculas/minúsculas).
        """
        criterio = criterio.lower()
        if criterio not in ("titulo", "autor", "anio"):
            raise ValueError("Criterio inválido. Use 'titulo', 'autor' o 'anio'")

        resultados = []
        for isbn, data in self.catalogo.items():
            # Determinar si coincide con el criterio solicitado
            match = False
            if criterio == "anio":
                match = int(valor) == int(data["anio"])
            else:
                if str(valor).lower() in data[criterio].lower():
                    match = True

            # Si además se pidió categoría, se filtra
            if match:
                if categoria and categoria.lower() != data["categoria"].lower():
                    continue
                resultados.append({
                    "isbn": isbn,
                    "titulo": data["titulo"],
                    "autor": data["autor"],
                    "anio": data["anio"],
                    "categoria": data["categoria"],
                    "copias_disponibles": data["copias_disponibles"]
                })
        return resultados

    # =====================================================
    # 5. GESTIÓN DE USUARIOS
    # =====================================================
    def registrar_usuario(self, id_usuario: str, nombre: str, email: str):
        """
        Registra un nuevo usuario, validando el email y que el ID no se repita.
        """
        if not id_usuario or not nombre:
            raise ValueError("ID y nombre no pueden estar vacíos")
        self._validar_email(email)
        if id_usuario in self.usuarios:
            raise ValueError("ID de usuario ya registrado")

        self.usuarios[id_usuario] = {
            "nombre": nombre,
            "email": email,
            "fecha_registro": datetime.now(),
            "prestamos_activos": [],
            "historial_prestamos": 0,
            "multas_pendientes": 0.0,
        }
        return True

    def obtener_estado_usuario(self, id_usuario: str) -> Dict[str, Any]:
        """
        Devuelve un resumen del estado actual del usuario:
        - lista de préstamos activos
        - si puede o no prestar
        - monto total de multas pendientes
        """
        if id_usuario not in self.usuarios:
            raise UsuarioNoRegistrado(id_usuario)

        u = self.usuarios[id_usuario]
        puede_prestar = (len(u["prestamos_activos"]) < self.limite_prestamos) and (u["multas_pendientes"] <= 50)

        return {
            "nombre": u["nombre"],
            "prestamos_activos": list(u["prestamos_activos"]),
            "puede_prestar": puede_prestar,
            "multas_pendientes": u["multas_pendientes"],
        }

    # =====================================================
    # 6. PRÉSTAMOS: prestar, devolver, renovar
    # =====================================================
    def prestar_libro(self, id_usuario: str, isbn: str) -> str:
        """
        Registra un préstamo de un libro, aplicando todas las validaciones:
        - usuario debe existir
        - libro debe existir
        - debe haber copias disponibles
        - usuario no debe exceder límite ni tener multas > 50
        """
        if id_usuario not in self.usuarios:
            raise UsuarioNoRegistrado(id_usuario)
        if isbn not in self.catalogo:
            raise LibroNoEncontrado(isbn)

        usuario = self.usuarios[id_usuario]
        libro = self.catalogo[isbn]

        if libro["copias_disponibles"] <= 0:
            raise LibroNoDisponible(isbn, libro["titulo"])
        if len(usuario["prestamos_activos"]) >= self.limite_prestamos:
            raise LimitePrestamosExcedido(id_usuario, self.limite_prestamos)
        if usuario["multas_pendientes"] > 50:
            raise ValueError("Usuario tiene multas pendientes superiores a 50")

        # Generamos el préstamo
        id_prestamo = self._generar_id_prestamo()
        fecha_prestamo = datetime.now()
        fecha_vencimiento = fecha_prestamo + timedelta(days=self.dias_prestamo)

        # Registrar en diccionarios
        self.prestamos[id_prestamo] = {
            "isbn": isbn,
            "id_usuario": id_usuario,
            "fecha_prestamo": fecha_prestamo,
            "fecha_vencimiento": fecha_vencimiento,
            "fecha_devolucion": None,
            "multa": 0.0,
        }

        # Actualizar catálogos y usuario
        libro["copias_disponibles"] -= 1
        libro["veces_prestado"] += 1
        usuario["prestamos_activos"].append(id_prestamo)
        usuario["historial_prestamos"] += 1

        return id_prestamo

    def devolver_libro(self, id_prestamo: str) -> Dict[str, Any]:
        """
        Marca un préstamo como devuelto, calcula la multa si está vencido
        y actualiza el estado del libro y del usuario.
        """
        if id_prestamo not in self.prestamos:
            raise KeyError(f"Préstamo {id_prestamo} no encontrado")

        prestamo = self.prestamos[id_prestamo]
        if prestamo["fecha_devolucion"] is not None:
            raise ValueError("Préstamo ya devuelto")

        ahora = datetime.now()
        vencimiento = prestamo["fecha_vencimiento"]

        # Cálculo de retraso
        dias_retraso = max(0, (ahora.date() - vencimiento.date()).days)
        multa = dias_retraso * self.multa_por_dia

        # Actualizar préstamo y usuario
        prestamo["fecha_devolucion"] = ahora
        prestamo["multa"] = multa

        usuario = self.usuarios[prestamo["id_usuario"]]
        usuario["multas_pendientes"] += multa
        if id_prestamo in usuario["prestamos_activos"]:
            usuario["prestamos_activos"].remove(id_prestamo)

        libro = self.catalogo[prestamo["isbn"]]
        libro["copias_disponibles"] += 1

        return {"dias_retraso": dias_retraso, "multa": multa, "mensaje": f"Devolución registrada para {id_prestamo}"}

    def renovar_prestamo(self, id_prestamo: str) -> Dict[str, Any]:
        """
        Extiende la fecha de vencimiento de un préstamo activo.
        Si el préstamo ya está vencido, lanza PrestamoVencido.
        """
        if id_prestamo not in self.prestamos:
            raise KeyError(f"Préstamo {id_prestamo} no encontrado")

        prestamo = self.prestamos[id_prestamo]
        if prestamo["fecha_devolucion"] is not None:
            raise ValueError("Préstamo ya devuelto")

        ahora = datetime.now()
        if ahora.date() > prestamo["fecha_vencimiento"].date():
            dias = (ahora.date() - prestamo["fecha_vencimiento"].date()).days
            raise PrestamoVencido(id_prestamo, dias)

        # Extender desde la fecha actual de vencimiento
        prestamo["fecha_vencimiento"] += timedelta(days=self.dias_prestamo)
        return {"id_prestamo": id_prestamo, "fecha_vencimiento": prestamo["fecha_vencimiento"], "mensaje": f"Préstamo {id_prestamo} renovado"}

    # =====================================================
    # 7. ESTADÍSTICAS Y REPORTES
    # =====================================================
    def libros_mas_prestados(self, n: int = 10):
        """Devuelve los N libros más prestados."""
        ordenados = sorted(self.catalogo.items(), key=lambda kv: kv[1]["veces_prestado"], reverse=True)
        return [(isbn, d["titulo"], d["veces_prestado"]) for isbn, d in ordenados[:n]]

    def usuarios_mas_activos(self, n: int = 10):
        """Devuelve los N usuarios que más préstamos realizaron."""
        ordenados = sorted(self.usuarios.items(), key=lambda kv: kv[1]["historial_prestamos"], reverse=True)
        return [(idu, u["nombre"], u["historial_prestamos"]) for idu, u in ordenados[:n]]

    def estadisticas_categoria(self, categoria: str) -> Dict[str, Any]:
        """
        Calcula estadísticas generales de una categoría de libros:
        - Total de libros
        - Copias totales y prestadas
        - Tasa de préstamo (%)
        - Libro más popular
        """
        total_libros = 0
        total_copias = 0
        copias_disponibles = 0
        libro_mas_popular = None
        max_prestamos = -1

        for isbn, data in self.catalogo.items():
            if data["categoria"].lower() == categoria.lower():
                total_libros += 1
                total_copias += data["copias_total"]
                copias_disponibles += data["copias_disponibles"]
                if data["veces_prestado"] > max_prestamos:
                    libro_mas_popular = {"isbn": isbn, "titulo": data["titulo"], "veces": data["veces_prestado"]}
                    max_prestamos = data["veces_prestado"]

        copias_prestadas = total_copias - copias_disponibles
        tasa = (copias_prestadas / total_copias * 100) if total_copias > 0 else 0
        return {"categoria": categoria, "total_libros": total_libros, "copias_prestadas": copias_prestadas, "tasa_prestamo_porcentaje": tasa, "libro_mas_popular": libro_mas_popular}

    # =====================================================
    # 8. IMPORTAR / EXPORTAR CATÁLOGO
    # =====================================================
    def exportar_catalogo(self, archivo: str) -> bool:
        """Guarda el catálogo en un archivo de texto con formato delimitado por |"""
        with open(archivo, "w", encoding="utf-8") as f:
            for isbn, d in self.catalogo.items():
                f.write(f"{isbn}|{d['titulo']}|{d['autor']}|{d['anio']}|{d['categoria']}|{d['copias_total']}\n")
        return True

    def importar_catalogo(self, archivo: str) -> Dict[str, Any]:
        """Carga libros desde un archivo de texto. Devuelve un resumen de éxito y errores."""
        if not os.path.exists(archivo):
            raise FileNotFoundError(f"Archivo {archivo} no encontrado")

        exitosos = 0
        errores = []
        with open(archivo, "r", encoding="utf-8") as f:
            for idx, linea in enumerate(f, start=1):
                partes = linea.strip().split("|")
                if len(partes) != 6:
                    errores.append((idx, "Línea mal formada"))
                    continue
                isbn, titulo, autor, anio, categoria, copias = partes
                try:
                    if isbn in self.catalogo:
                        errores.append((idx, f"ISBN {isbn} ya existe (saltado)"))
                        continue
                    self.agregar_libro(isbn, titulo, autor, int(anio), categoria, int(copias))
                    exitosos += 1
                except Exception as e:
                    errores.append((idx, str(e)))
        return {"exitosos": exitosos, "errores": errores}
    # =====================================================
# BLOQUE DE PRUEBA DIRECTA
# =====================================================
if __name__ == "__main__":
    print("=== PRUEBAS RÁPIDAS DEL SISTEMA ===")
    s = SistemaBiblioteca(dias_prestamo=7, multa_por_dia=2.0, limite_prestamos=2)

    # 1️.Registrar libros y usuarios
    s.agregar_libro("9780134685991", "Effective Java", "Joshua Bloch", 2018, "programacion", 2)
    s.agregar_libro("9781491957660", "Fluent Python", "Luciano Ramalho", 2015, "programacion", 1)
    s.registrar_usuario("U001", "Ana", "ana@mail.com")
    s.registrar_usuario("U002", "Luis", "luis@mail.com")

    # 2️.Prestar libros
    p1 = s.prestar_libro("U001", "9780134685991")
    print("Préstamo creado:", p1)
    print("Estado usuario U001:", s.obtener_estado_usuario("U001"))

    # 3️.Devolver sin retraso
    print("Devolviendo libro...")
    print(s.devolver_libro(p1))

    # 4️.Forzar retraso artificial
    p2 = s.prestar_libro("U002", "9781491957660")
    s.prestamos[p2]["fecha_vencimiento"] = datetime.now() - timedelta(days=3)
    print("Devolviendo con retraso...")
    print(s.devolver_libro(p2))

    # 5️.Mostrar multas pendientes
    print("Estado final de U002:", s.obtener_estado_usuario("U002"))

#!/usr/bin/env python3
# test_biblioteca.py
"""
Rafael Angel Hernandez Gomez
"""

from datetime import datetime, timedelta
import os
import sys
import traceback

# Importar el sistema real
try:
    from sistema_biblioteca import (
        SistemaBiblioteca,
        LibroNoEncontrado,
        LibroNoDisponible,
        UsuarioNoRegistrado,
        LimitePrestamosExcedido,
        PrestamoVencido
    )
except Exception as e:
    print("ERROR: No se pudo importar sistema_biblioteca.py")
    traceback.print_exc()
    sys.exit(1)
#Profe tuve problemas con llamar el catalogo, asi que implemente esta funcion que lo que hace es obligar a python a buscar en la misma carpeta donde esta el test_biblioteca
CATALOGO = os.path.join(os.path.dirname(__file__), "catalogo_inicial.txt")

# ------------------------------
# UTILIDADES
# ------------------------------
_total = 0
_ok = 0
_fail = 0

def ok():  # marca prueba exitosa
    global _total, _ok
    _total += 1
    _ok += 1

def fail():  # marca prueba fallida
    global _total, _fail
    _total += 1
    _fail += 1

def titulo(t):
    print("\n" + "="*75)
    print(t)
    print("="*75)

# ------------------------------
# PRUEBAS
# ------------------------------
def test_agregar_libros():
    titulo("AGREGAR LIBROS Y VALIDACIONES")
    try:
        s = SistemaBiblioteca()
        s.agregar_libro("9780134685991", "Effective Java", "Joshua Bloch", 2018, "Programacion", 2)
        assert "9780134685991" in s.catalogo
        # Duplicado
        try:
            s.agregar_libro("9780134685991", "Otra", "Autor", 2010, "Cat", 1)
        except KeyError:
            pass
        # ISBN inválido
        try:
            s.agregar_libro("123", "T", "A", 2000, "C", 1)
            raise AssertionError
        except ValueError:
            pass
        print("✓ Libros OK")
        ok()
    except Exception as e:
        print("✗ Error en agregar libros:", e)
        fail()

def test_usuarios():
    titulo("REGISTRO DE USUARIOS")
    try:
        s = SistemaBiblioteca()
        s.registrar_usuario("U01", "Ana", "ana@mail.com")
        assert "U01" in s.usuarios
        try:
            s.registrar_usuario("U01", "Repetido", "dup@mail.com")
        except ValueError:
            pass
        try:
            s.registrar_usuario("U02", "Beto", "correoSinArroba")
        except ValueError:
            pass
        print("✓ Usuarios OK")
        ok()
    except Exception as e:
        print("✗ Error en usuarios:", e)
        fail()

def test_prestamos_y_limites():
    titulo("PRÉSTAMOS Y LÍMITES")
    try:
        s = SistemaBiblioteca(limite_prestamos=2)
        s.agregar_libro("9780000000001", "Libro A", "Autor", 2020, "Ciencia", 2)
        s.agregar_libro("9780000000002", "Libro B", "Autor", 2020, "Ciencia", 1)
        s.registrar_usuario("U1", "Juan", "juan@mail.com")
        # prestar_libro espera (id_usuario, isbn)
        pid1 = s.prestar_libro("U1", "9780000000001")
        pid2 = s.prestar_libro("U1", "9780000000001")
        try:
            s.prestar_libro("U1", "9780000000001")
        except LimitePrestamosExcedido:
            pass
        try:
            s.prestar_libro("NOUSER", "9780000000001")
        except UsuarioNoRegistrado:
            pass
        try:
            s.prestar_libro("U1", "9999999999999")
        except LibroNoEncontrado:
            pass
        print("✓ Préstamos OK")
        ok()
    except Exception as e:
        print("✗ Error en préstamos:", e)
        fail()

def test_devolucion_y_multas():
    titulo("DEVOLUCIONES Y MULTAS")
    try:
        s = SistemaBiblioteca(dias_prestamo=7, multa_por_dia=2.0)
        s.agregar_libro("9780000000003", "Libro C", "Autor", 2015, "General", 1)
        s.registrar_usuario("U2", "Pedro", "pedro@mail.com")
        pid = s.prestar_libro("U2", "9780000000003")
        # devolución puntual
        r = s.devolver_libro(pid)
        assert r["multa"] == 0
        # préstamo atrasado
        pid2 = s.prestar_libro("U2", "9780000000003")
        s.prestamos[pid2]["fecha_vencimiento"] = datetime.now() - timedelta(days=3)
        r2 = s.devolver_libro(pid2)
        assert r2["multa"] == 6
        print("✓ Devoluciones OK")
        ok()
    except Exception as e:
        print("✗ Error en devoluciones:", e)
        fail()

def test_busquedas():
    titulo("BÚSQUEDAS EN CATÁLOGO")
    try:
        s = SistemaBiblioteca()
        s.agregar_libro("9780000001000", "Python Avanzado", "Autor1", 2019, "Programacion", 2)
        s.agregar_libro("9780000001001", "C Básico", "Autor2", 2018, "Programacion", 1)
        s.agregar_libro("9780000001002", "Historia", "Autor3", 2000, "Historia", 1)
        r = s.buscar_libros("titulo", "python")
        assert len(r) == 1
        r2 = s.buscar_libros("autor", "Autor2")
        assert len(r2) == 1
        r3 = s.buscar_libros("anio", 2000)
        assert len(r3) == 1
        print("✓ Búsquedas OK")
        ok()
    except Exception as e:
        print("✗ Error en búsquedas:", e)
        fail()

def test_estadisticas():
    titulo("ESTADÍSTICAS GENERALES")
    try:
        s = SistemaBiblioteca()
        s.agregar_libro("9780000002000", "Libro X", "Autor", 2010, "Drama", 2)
        s.agregar_libro("9780000002001", "Libro Y", "Autor", 2011, "Drama", 1)
        s.registrar_usuario("U3", "Luz", "luz@mail.com")
        pid = s.prestar_libro("U3", "9780000002000")
        s.devolver_libro(pid)
        top = s.libros_mas_prestados()
        assert isinstance(top, list)
        cat = s.estadisticas_categoria("Drama")
        assert "total_libros" in cat
        print("✓ Estadísticas OK")
        ok()
    except Exception as e:
        print("✗ Error en estadísticas:", e)
        fail()

def test_import_export():
    titulo("IMPORTACIÓN / EXPORTACIÓN")
    try:
        s = SistemaBiblioteca()
        tmp = "tmp_export.txt"
        # asegurar que el export no falle aunque catalogo esté vacío
        s.exportar_catalogo(tmp)
        assert os.path.exists(tmp)
        os.remove(tmp)
        if os.path.exists(CATALOGO):
            r = s.importar_catalogo(CATALOGO)
            assert "exitosos" in r and "errores" in r
            print(f"✓ Importación: {r['exitosos']} exitosos, {len(r['errores'])} errores")
        else:
            print("No se encontró catalogo_inicial.txt")
        ok()
    except Exception as e:
        print("✗ Error en import/export:", e)
        fail()

def test_renovar():
    titulo("RENOVACIÓN DE PRÉSTAMO")
    try:
        s = SistemaBiblioteca(dias_prestamo=5)
        s.agregar_libro("9780000003000", "Renovable", "Autor", 2020, "Novela", 1)
        s.registrar_usuario("U4", "Renato", "r@mail.com")
        pid = s.prestar_libro("U4", "9780000003000")
        old = s.prestamos[pid]["fecha_vencimiento"]
        res = s.renovar_prestamo(pid)
        assert res["fecha_vencimiento"] > old
        print("✓ Renovación OK")
        ok()
    except Exception as e:
        print("✗ Error en renovación:", e)
        fail()

# ------------------------------
# EJECUCIÓN PRINCIPAL
# ------------------------------
def main():
    print("\nSISTEMA DE BIBLIOTECA — SUITE DE PRUEBAS AUTOMÁTICAS\n")
    tests = [
        test_agregar_libros,
        test_usuarios,
        test_prestamos_y_limites,
        test_devolucion_y_multas,
        test_busquedas,
        test_estadisticas,
        test_import_export,
        test_renovar
    ]
    for t in tests:
        try:
            t()
        except Exception as e:
            print("Error inesperado:", e)
            fail()

    print("\n" + "="*75)
    print(f"Pruebas ejecutadas: {_total}")
    print(f"   Exitosas: {_ok}")
    print(f"   Fallidas: {_fail}")
    if _fail == 0:
        print("→ Todas las pruebas pasaron correctamente ")
    else:
        print("→ Algunas pruebas fallaron ")
    print("="*75)

if __name__ == "__main__":
    main()

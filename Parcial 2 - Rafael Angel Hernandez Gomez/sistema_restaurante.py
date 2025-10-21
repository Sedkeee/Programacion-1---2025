#!/usr/bin/env python3
"""
sistema_restaurante.py

Rafael Angel Hernandez Gomez

"""

from datetime import datetime
from typing import Dict, Any, List
import os

# ===========================================================================
# EXCEPCIONES PERSONALIZADAS
# ===========================================================================

class ErrorRestaurante(Exception):
    """Excepción base para el sistema de restaurante."""
    pass

class PlatoNoEncontrado(ErrorRestaurante):
    """Se lanza cuando un plato no existe en el menú."""
    def __init__(self, codigo_plato: str):
        self.codigo_plato = codigo_plato
        super().__init__(f"Plato con código '{codigo_plato}' no encontrado en el menú")

class MesaNoDisponible(ErrorRestaurante):
    """Se lanza cuando la mesa está ocupada."""
    def __init__(self, numero_mesa: int, hora_disponible: str):
        self.numero_mesa = numero_mesa
        self.hora_disponible = hora_disponible
        super().__init__(f"Mesa {numero_mesa} no disponible. Disponible a las {hora_disponible}")

class CapacidadExcedida(ErrorRestaurante):
    """Se lanza cuando hay más comensales que capacidad."""
    def __init__(self, numero_mesa: int, capacidad: int, comensales: int):
        self.numero_mesa = numero_mesa
        self.capacidad = capacidad
        self.comensales = comensales
        super().__init__(f"Mesa {numero_mesa} tiene capacidad para {capacidad}, se solicitaron {comensales} lugares")

class PedidoInvalido(ErrorRestaurante):
    """Se lanza para pedidos con problemas."""
    def __init__(self, razon: str):
        self.razon = razon
        super().__init__(f"Pedido inválido: {razon}")


# ===========================================================================
# CLASE PRINCIPAL: SISTEMA RESTAURANTE
# ===========================================================================

class SistemaRestaurante:
    """
    Sistema completo de gestión de restaurante.
    """

    def __init__(self, num_mesas: int = 10, tasa_impuesto: float = 0.16, propina_sugerida: float = 0.15):
        """
        Inicializa las estructuras principales.

        Comentario: usamos diccionarios para representar el estado del restaurante
        en memoria (sin persistencia en base de datos). Esto es suficiente para
        los ejercicios y para pruebas locales.
        """
        # Parámetros
        self.num_mesas = int(num_mesas)
        self.tasa_impuesto = float(tasa_impuesto)
        self.propina_sugerida = float(propina_sugerida)

        # Menú: {codigo: {'nombre', 'categoria', 'precio', 'disponible'}}
        self.menu: Dict[str, Dict[str, Any]] = {}

        # Mesas: {numero: {'capacidad', 'ocupada', 'reservacion', 'pedido_actual'}}
        # reservacion: {'comensales', 'hora' (str)}
        self.mesas: Dict[int, Dict[str, Any]] = {}

        # Pedidos: {id_pedido: {'mesa', 'items': {codigo: cantidad}, 'subtotal', 'impuesto', 'propina', 'total', 'hora', 'pagado'}}
        self.pedidos: Dict[str, Dict[str, Any]] = {}

        # Ventas del día: lista de ids de pedidos pagados en el día
        self.ventas_dia: List[str] = []

        # Conteo acumulado por plato de la jornada (codigo -> cantidad vendida)
        self.ventas_platos: Dict[str, int] = {}

    # ============ GESTIÓN DE MENÚ ============

    def agregar_plato(self, codigo: str, nombre: str, categoria: str, precio: float):
        """
        Agrega un plato al menú con validaciones:
        - código no vacío y único
        - nombre no vacío
        - categoría dentro de las permitidas
        - precio > 0
        """
        if not codigo or not isinstance(codigo, str):
            raise ValueError("Código inválido")
        if codigo in self.menu:
            raise KeyError(f"Código {codigo} ya existe en el menú")
        if not nombre:
            raise ValueError("Nombre de plato no puede estar vacío")
        categorias_validas = {"entrada", "plato_fuerte", "postre", "bebida"}
        if categoria not in categorias_validas:
            raise ValueError(f"Categoría inválida. Debe ser una de {categorias_validas}")
        try:
            precio = float(precio)
        except Exception:
            raise ValueError("Precio inválido")
        if precio <= 0:
            raise ValueError("Precio debe ser mayor que 0")

        # Guardamos el plato en el menú. Por defecto está disponible.
        self.menu[codigo] = {
            "nombre": nombre,
            "categoria": categoria,
            "precio": precio,
            "disponible": True
        }

    def cambiar_disponibilidad(self, codigo: str, disponible: bool):
        """
        Cambia la disponibilidad de un plato.
        Lanza PlatoNoEncontrado si el código no existe.
        """
        if codigo not in self.menu:
            raise PlatoNoEncontrado(codigo)
        self.menu[codigo]["disponible"] = bool(disponible)

    def buscar_platos(self, categoria: str = None, precio_max: float = None):
        """
        Busca platos disponibles, filtrando por categoría y/o precio máximo.
        Retorna lista de diccionarios con información pública de los platos.
        """
        resultados = []
        for codigo, p in self.menu.items():
            if not p.get("disponible", False):
                continue
            if categoria and p["categoria"] != categoria:
                continue
            if precio_max is not None:
                try:
                    if p["precio"] > float(precio_max):
                        continue
                except Exception:
                    continue
            resultados.append({
                "codigo": codigo,
                "nombre": p["nombre"],
                "categoria": p["categoria"],
                "precio": p["precio"]
            })
        return resultados

    # ============ GESTIÓN DE MESAS ============

    def configurar_mesa(self, numero: int, capacidad: int):
        """
        Configura (o crea) una mesa con número y capacidad.
        Validaciones: número entre 1 y num_mesas, capacidad entre 1 y 12.
        """
        if not (1 <= numero <= self.num_mesas):
            raise ValueError(f"Número de mesa inválido. Debe estar entre 1 y {self.num_mesas}")
        if not (1 <= capacidad <= 12):
            raise ValueError("Capacidad inválida. Debe estar entre 1 y 12")

        # Crear o actualizar la mesa con estado inicial no ocupada.
        self.mesas[numero] = {
            "capacidad": int(capacidad),
            "ocupada": False,
            "reservacion": None,
            "pedido_actual": None
        }

    def reservar_mesa(self, numero: int, comensales: int, hora: str):
        """
        Reserva una mesa: valida existencia, estado y capacidad.
        Si la mesa está ocupada lanza MesaNoDisponible con la hora de disponibilidad (si existe).
        """
        if numero not in self.mesas:
            raise ValueError("Mesa no existe")
        mesa = self.mesas[numero]
        if mesa["ocupada"]:
            # Si ya hay una reservación/ocupación recuperamos la hora (si existe)
            hora_disp = mesa["reservacion"]["hora"] if mesa["reservacion"] else "desconocida"
            raise MesaNoDisponible(numero, hora_disp)
        if comensales > mesa["capacidad"]:
            raise CapacidadExcedida(numero, mesa["capacidad"], comensales)
        # Validar formato simple de hora "HH:MM"
        try:
            parts = hora.split(":")
            if len(parts) != 2 or not (0 <= int(parts[0]) < 24) or not (0 <= int(parts[1]) < 60):
                raise ValueError
        except Exception:
            raise ValueError("Formato de hora inválido. Debe ser 'HH:MM'")

        # Marcar la mesa como ocupada por la reservación solicitada
        mesa["ocupada"] = True
        mesa["reservacion"] = {"comensales": int(comensales), "hora": hora}
        # No creamos pedido aún; el pedido se crea cuando los comensales solicitan
        mesa["pedido_actual"] = None

    def liberar_mesa(self, numero: int):
        """
        Libera una mesa al terminar servicio: limpia reservación y pedido.
        """
        if numero not in self.mesas:
            raise ValueError("Mesa no existe")
        mesa = self.mesas[numero]
        if not mesa["ocupada"]:
            raise ValueError("Mesa no está ocupada")
        # Si había un pedido activo y no fue pagado, lo dejamos como historial (no lo eliminamos),
        # pero desvinculamos la relación con la mesa.
        if mesa["pedido_actual"]:
            # No forzamos pago; simplemente removemos la referencia de la mesa.
            mesa["pedido_actual"] = None
        mesa["ocupada"] = False
        mesa["reservacion"] = None

    def mesas_disponibles(self, comensales: int):
        """
        Retorna lista de números de mesa que no están ocupadas y tienen capacidad suficiente.
        """
        disponibles = []
        for numero in range(1, self.num_mesas + 1):
            mesa = self.mesas.get(numero)
            if not mesa:
                continue
            if not mesa["ocupada"] and mesa["capacidad"] >= comensales:
                disponibles.append(numero)
        return disponibles

    # ============ GESTIÓN DE PEDIDOS ============

    def _generar_id_pedido(self) -> str:
        """
        Genera un ID único para pedido usando timestamp en milisegundos.
        """
        ts = int(datetime.now().timestamp() * 1000)
        return f"PED{ts}"

    def crear_pedido(self, numero_mesa: int) -> str:
        """
        Crea un pedido vinculado a una mesa ocupada y sin pedido activo.
        Devuelve id_pedido (string).
        """
        if numero_mesa not in self.mesas:
            raise ValueError("Mesa no existe")
        mesa = self.mesas[numero_mesa]
        if not mesa["ocupada"]:
            raise ValueError("Mesa no está ocupada")
        if mesa["pedido_actual"] is not None:
            raise ValueError("La mesa ya tiene un pedido activo")

        id_pedido = self._generar_id_pedido()
        self.pedidos[id_pedido] = {
            "mesa": numero_mesa,
            "items": {},  # codigo -> cantidad
            "subtotal": 0.0,
            "impuesto": 0.0,
            "propina": 0.0,
            "total": 0.0,
            "hora": datetime.now(),
            "pagado": False
        }
        mesa["pedido_actual"] = id_pedido
        return id_pedido

    def agregar_item(self, id_pedido: str, codigo_plato: str, cantidad: int = 1):
        """
        Agrega un item (plato) a un pedido: valida existencia de pedido, estado de pago,
        existencia del plato y disponibilidad, y cantidad positiva.
        """
        if id_pedido not in self.pedidos:
            raise PedidoInvalido("Pedido no existe")
        pedido = self.pedidos[id_pedido]
        if pedido["pagado"]:
            raise PedidoInvalido("Pedido ya fue pagado")

        if codigo_plato not in self.menu:
            raise PlatoNoEncontrado(codigo_plato)
        plato = self.menu[codigo_plato]
        if not plato.get("disponible", False):
            raise ValueError("Plato no disponible")

        if cantidad <= 0:
            raise ValueError("Cantidad debe ser mayor que 0")

        # Agregar cantidad al pedido (sumando si ya existe)
        pedido["items"][codigo_plato] = pedido["items"].get(codigo_plato, 0) + int(cantidad)

    def calcular_total(self, id_pedido: str, propina_porcentaje: float = None):
        """
        Calcula subtotal, impuesto, propina y total para el pedido.
        No marca el pedido como pagado; simplemente calcula y devuelve los valores.
        """
        if id_pedido not in self.pedidos:
            raise PedidoInvalido("Pedido no existe")
        pedido = self.pedidos[id_pedido]
        items = pedido["items"]
        subtotal = 0.0
        # Sumamos precio * cantidad para cada item (validando que el plato siga en el menú)
        for codigo, qty in items.items():
            plato = self.menu.get(codigo)
            if not plato:
                # Si el plato fue borrado del menú después de pedirlo, lo tratamos como error
                raise PlatoNoEncontrado(codigo)
            subtotal += plato["precio"] * qty

        impuesto = subtotal * self.tasa_impuesto
        if propina_porcentaje is None:
            propina_porcentaje = self.propina_sugerida
        propina = subtotal * float(propina_porcentaje)
        total = subtotal + impuesto + propina

        # No actualizamos el pedido aquí para que la función sea "pure calc" — pero es conveniente
        # guardar los valores calculados en la estructura del pedido para reportes.
        pedido["subtotal"] = round(subtotal, 2)
        pedido["impuesto"] = round(impuesto, 2)
        pedido["propina"] = round(propina, 2)
        pedido["total"] = round(total, 2)

        return {
            "subtotal": pedido["subtotal"],
            "impuesto": pedido["impuesto"],
            "propina": pedido["propina"],
            "total": pedido["total"]
        }

    def pagar_pedido(self, id_pedido: str, propina_porcentaje: float = None):
        """
        Procesa el pago del pedido: calcula totales, marca como pagado, actualiza
        las estadísticas (ventas_dia y ventas_platos) y desvincula el pedido de la mesa.
        """
        if id_pedido not in self.pedidos:
            raise PedidoInvalido("Pedido no existe")
        pedido = self.pedidos[id_pedido]
        if pedido["pagado"]:
            raise PedidoInvalido("Pedido ya fue pagado")

        # Calcular totales (esto también actualiza los campos subtotal/impuesto/propina/total)
        totales = self.calcular_total(id_pedido, propina_porcentaje)

        # Marcar como pagado y registrar hora final de pago
        pedido["pagado"] = True
        pedido["hora_pago"] = datetime.now()

        # Registrar en ventas del día
        self.ventas_dia.append(id_pedido)

        # Actualizar conteo de platos vendidos (para reportes)
        for codigo, qty in pedido["items"].items():
            self.ventas_platos[codigo] = self.ventas_platos.get(codigo, 0) + qty

        # Desvincular pedido de la mesa (la mesa queda ocupada hasta liberación manual)
        numero_mesa = pedido["mesa"]
        if numero_mesa in self.mesas:
            mesa = self.mesas[numero_mesa]
            if mesa.get("pedido_actual") == id_pedido:
                mesa["pedido_actual"] = None

        return totales

    # ============ REPORTES Y ESTADÍSTICAS ============

    def platos_mas_vendidos(self, n: int = 5):
        """
        Retorna los N platos más vendidos como lista de tuplas:
        (codigo, nombre, cantidad_vendida)
        """
        ranking = sorted(self.ventas_platos.items(), key=lambda kv: kv[1], reverse=True)
        result = []
        for codigo, qty in ranking[:n]:
            nombre = self.menu.get(codigo, {}).get("nombre", "Desconocido")
            result.append((codigo, nombre, qty))
        return result

    def ventas_por_categoria(self):
        """
        Calcula ventas monetarias por categoría (sumando precio*cantidad vendidos).
        """
        totales = {"entrada": 0.0, "plato_fuerte": 0.0, "postre": 0.0, "bebida": 0.0}
        for codigo, qty in self.ventas_platos.items():
            plato = self.menu.get(codigo)
            if not plato:
                continue
            categoria = plato["categoria"]
            totales[categoria] = totales.get(categoria, 0.0) + plato["precio"] * qty
        # Redondear para presentación
        for k in totales:
            totales[k] = round(totales[k], 2)
        return totales

    def reporte_ventas_dia(self):
        """
        Genera resumen del día usando los pedidos pagados (ventas_dia).
        """
        total_pedidos = len(self.ventas_dia)
        subtotal_ventas = 0.0
        total_impuestos = 0.0
        total_propinas = 0.0
        total_ingresos = 0.0

        for pid in self.ventas_dia:
            p = self.pedidos.get(pid)
            if not p:
                continue
            subtotal_ventas += p.get("subtotal", 0.0)
            total_impuestos += p.get("impuesto", 0.0)
            total_propinas += p.get("propina", 0.0)
            total_ingresos += p.get("total", 0.0)

        ticket_promedio = round((total_ingresos / total_pedidos), 2) if total_pedidos > 0 else 0.0

        # Plato más vendido (nombre)
        plato_mas_vendido = None
        if self.ventas_platos:
            codigo_top = max(self.ventas_platos.items(), key=lambda kv: kv[1])[0]
            plato_mas_vendido = self.menu.get(codigo_top, {}).get("nombre", None)

        return {
            "total_pedidos": total_pedidos,
            "subtotal_ventas": round(subtotal_ventas, 2),
            "total_impuestos": round(total_impuestos, 2),
            "total_propinas": round(total_propinas, 2),
            "total_ingresos": round(total_ingresos, 2),
            "ticket_promedio": ticket_promedio,
            "plato_mas_vendido": plato_mas_vendido
        }

    def estado_restaurante(self):
        """
        Retorna un resumen rápido del estado actual del restaurante.
        """
        mesas_ocupadas = sum(1 for m in self.mesas.values() if m["ocupada"])
        mesas_disponibles = sum(1 for m in self.mesas.values() if not m["ocupada"])
        pedidos_activos = sum(1 for p in self.pedidos.values() if not p["pagado"])
        pedidos_completados_hoy = len(self.ventas_dia)

        return {
            "mesas_ocupadas": mesas_ocupadas,
            "mesas_disponibles": mesas_disponibles,
            "pedidos_activos": pedidos_activos,
            "pedidos_completados_hoy": pedidos_completados_hoy
        }

    # ============ UTILIDADES: IMPORT / EXPORT ============

    def exportar_menu(self, archivo: str = "menu.txt"):
        """
        Exporta el menú actual a un archivo de texto.
        Formato por línea: Codigo|Nombre|Categoria|Precio|Disponible
        """
        try:
            with open(archivo, "w", encoding="utf-8") as f:
                for codigo, p in self.menu.items():
                    linea = f"{codigo}|{p['nombre']}|{p['categoria']}|{p['precio']:.2f}|{p['disponible']}\n"
                    f.write(linea)
            return True
        except Exception as e:
            # Re-lanzamos la excepción para que el llamador la gestione
            raise e

    def importar_menu(self, archivo: str = "menu.txt"):
        """
        Importa menú desde archivo de texto. Maneja:
        - Archivo inexistente -> FileNotFoundError
        - Líneas mal formadas -> errores listados
        - Duplicados -> reportados como errores (no sobrescribir)
        Devuelve dict {'exitosos': int, 'errores': [(linea, error), ...]}
        """
        if not os.path.exists(archivo):
            raise FileNotFoundError(f"Archivo {archivo} no encontrado")

        exitosos = 0
        errores = []
        with open(archivo, "r", encoding="utf-8") as f:
            for idx, linea in enumerate(f, start=1):
                partes = linea.strip().split("|")
                if len(partes) != 5:
                    errores.append((idx, "Línea mal formada"))
                    continue
                codigo, nombre, categoria, precio_str, disponible_str = partes
                try:
                    if codigo in self.menu:
                        errores.append((idx, f"Código {codigo} ya existe (saltado)"))
                        continue
                    precio = float(precio_str)
                    disponible = disponible_str.strip().lower() in ("true", "1", "si", "yes", "verdadero")
                    # Reutilizar la validación de agregar_plato (pero sin lanzar KeyError)
                    categorias_validas = {"entrada", "plato_fuerte", "postre", "bebida"}
                    if categoria not in categorias_validas:
                        raise ValueError("Categoría inválida")
                    if precio <= 0:
                        raise ValueError("Precio inválido")
                    # Insertar en el menú
                    self.menu[codigo] = {
                        "nombre": nombre,
                        "categoria": categoria,
                        "precio": precio,
                        "disponible": disponible
                    }
                    exitosos += 1
                except Exception as e:
                    errores.append((idx, str(e)))
        return {"exitosos": exitosos, "errores": errores}


# ===========================================================================
# BLOQUE DE PRUEBA RÁPIDA (opcional)
# ===========================================================================

if __name__ == "__main__":
    print("== SISTEMA RESTAURANTE - PRUEBAS RÁPIDAS ==")

    # Crear sistema y configurar algunas mesas (ejemplo)
    sr = SistemaRestaurante(num_mesas=5)
    sr.configurar_mesa(1, 4)
    sr.configurar_mesa(2, 2)
    sr.configurar_mesa(3, 6)

    # Cargar menú desde archivo 'Menu.txt' si existe
    if os.path.exists("Menu.txt"):
        print("Importando Menu.txt ...")
        try:
            res = sr.importar_menu("Menu.txt")
            print(f"Importados: {res['exitosos']}, errores: {len(res['errores'])}")
        except Exception as e:
            print("Error importando menu:", e)
    else:
        # Agregar algunos platos manualmente para probar
        sr.agregar_plato("E001", "Ensalada César", "entrada", 85.00)
        sr.agregar_plato("P001", "Filete de Res", "plato_fuerte", 350.00)
        sr.agregar_plato("B001", "Limonada", "bebida", 45.00)

    # Reservar mesa y crear pedido de ejemplo
    try:
        sr.reservar_mesa(1, 3, "14:30")
        pid = sr.crear_pedido(1)
        sr.agregar_item(pid, "E001", 2)
        sr.agregar_item(pid, "P001", 1)
        tot = sr.calcular_total(pid, propina_porcentaje=0.18)
        print("Totales calculados:", tot)
        pago = sr.pagar_pedido(pid, propina_porcentaje=0.18)
        print("Pago procesado:", pago)
        sr.liberar_mesa(1)
        print("Reporte vent as dia:", sr.reporte_ventas_dia())
    except Exception as e:
        print("Error en flujo de prueba:", e)

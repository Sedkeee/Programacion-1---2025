#!/usr/bin/env python3
"""
PARCIAL 2 - EJERCICIOS (Parte 1)
Autor: Rafael Angel Hernandez Gomez
Fecha: 10/19/25
"""

# ===========================================================================
# EJERCICIO 1: EXPRESIONES ARITMÉTICAS
# ===========================================================================

def calculadora_cientifica(operacion, a, b):
    """
    Realiza operaciones matemáticas con validación y manejo de errores.

    Args:
        operacion (str): tipo de operación ("suma", "resta", "multiplicacion", "division", "potencia", "modulo")
        a (float|int): primer número
        b (float|int): segundo número

    Returns:
        float: resultado redondeado a 2 decimales

    Raises:
        ValueError: si la operación o tipos son inválidos
        ZeroDivisionError: si se intenta dividir o hacer módulo entre cero
    """
    # Primero validamos que ambos valores sean numéricos
    if not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
        raise ValueError("Los parámetros deben ser numéricos (int o float)")

    # Lista de operaciones permitidas según el enunciado
    operaciones_validas = {
        "suma", "resta", "multiplicacion", "division", "potencia", "modulo"
    }

    # Si la operación no está en el conjunto permitido, lanzamos error
    if operacion not in operaciones_validas:
        raise ValueError(f"Operación inválida: '{operacion}'")

    # Realizamos la operación correspondiente
    if operacion == "suma":
        res = a + b
    elif operacion == "resta":
        res = a - b
    elif operacion == "multiplicacion":
        res = a * b
    elif operacion == "division":
        if b == 0:
            raise ZeroDivisionError("No se puede dividir por cero")
        res = a / b
    elif operacion == "potencia":
        res = a ** b
    elif operacion == "modulo":
        if b == 0:
            raise ZeroDivisionError("No se puede hacer módulo con divisor 0")
        res = a % b

    # Finalmente devolvemos el resultado redondeado a 2 decimales
    return round(res, 2)


# ===========================================================================
# EJERCICIO 2: EXPRESIONES LÓGICAS Y RELACIONALES
# ===========================================================================

class ValidadorPassword:
    """
    Clase que valida contraseñas bajo reglas configurables.
    Permite verificar la fortaleza de un password y los errores específicos.
    """

    CARACTERES_ESPECIALES = set("!@#$%^&*()_+-=[]{}|;:,.<>?/")

    def __init__(self, min_longitud=8, requiere_mayuscula=True,
                 requiere_minuscula=True, requiere_numero=True,
                 requiere_especial=True):
        self.min_longitud = min_longitud
        self.requiere_mayuscula = requiere_mayuscula
        self.requiere_minuscula = requiere_minuscula
        self.requiere_numero = requiere_numero
        self.requiere_especial = requiere_especial

    def validar(self, password):
        """
        Valida la contraseña según las reglas definidas en la clase.

        Returns:
            tuple: (es_valido: bool, errores: list[str])
        """
        if not isinstance(password, str):
            raise ValueError("La contraseña debe ser una cadena de texto")

        errores = []

        # Revisamos una a una las condiciones de seguridad
        if len(password) < self.min_longitud:
            errores.append(f"Debe tener al menos {self.min_longitud} caracteres")

        if self.requiere_mayuscula and not any(c.isupper() for c in password):
            errores.append("Debe contener al menos una mayúscula")

        if self.requiere_minuscula and not any(c.islower() for c in password):
            errores.append("Debe contener al menos una minúscula")

        if self.requiere_numero and not any(c.isdigit() for c in password):
            errores.append("Debe contener al menos un número")

        if self.requiere_especial and not any(c in self.CARACTERES_ESPECIALES for c in password):
            errores.append("Debe contener al menos un carácter especial (!, @, #, etc.)")

        # Si hay errores, devolvemos la lista, si no, indicamos que es válida
        return (len(errores) == 0, errores)

    def es_fuerte(self, password):
        """
        Determina si una contraseña es fuerte.
        Criterios: al menos 12 caracteres, con mayúsculas, minúsculas, número y símbolo.
        """
        if len(password) < 12:
            return False
        checks = [
            any(c.isupper() for c in password),
            any(c.islower() for c in password),
            any(c.isdigit() for c in password),
            any(c in self.CARACTERES_ESPECIALES for c in password)
        ]
        return all(checks)


# ===========================================================================
# EJERCICIO 3: ESTRUCTURAS DE DATOS
# ===========================================================================

class GestorInventario:
    """
    Clase que permite gestionar productos con sus precios, stock y categoría.
    """

    def __init__(self):
        # Estructura: {codigo: {'nombre', 'precio', 'cantidad', 'categoria'}}
        self.inventario = {}

    def agregar_producto(self, codigo, nombre, precio, cantidad, categoria):
        """
        Agrega un producto nuevo al inventario.
        """
        if codigo in self.inventario:
            raise ValueError("El código del producto ya existe")
        if cantidad < 0 or precio < 0:
            raise ValueError("Precio o cantidad no pueden ser negativos")

        # Guardamos los datos del producto en el diccionario
        self.inventario[codigo] = {
            'nombre': nombre,
            'precio': float(precio),
            'cantidad': int(cantidad),
            'categoria': categoria
        }

    def actualizar_stock(self, codigo, cantidad_cambio):
        """
        Suma o resta unidades del stock de un producto.
        """
        if codigo not in self.inventario:
            raise ValueError("El producto no existe")
        nuevo_stock = self.inventario[codigo]['cantidad'] + cantidad_cambio
        if nuevo_stock < 0:
            raise ValueError("El stock no puede quedar negativo")
        self.inventario[codigo]['cantidad'] = nuevo_stock

    def buscar_por_categoria(self, categoria):
        """
        Retorna una lista de productos que pertenecen a una categoría dada.
        """
        return [
            (codigo, datos['nombre'], datos['precio'])
            for codigo, datos in self.inventario.items()
            if datos['categoria'] == categoria
        ]

    def productos_bajo_stock(self, limite=10):
        """
        Retorna los productos cuyo stock está por debajo del límite especificado.
        """
        return {
            codigo: datos['cantidad']
            for codigo, datos in self.inventario.items()
            if datos['cantidad'] < limite
        }

    def valor_total_inventario(self):
        """
        Calcula el valor total de todos los productos en el inventario.
        """
        total = sum(d['precio'] * d['cantidad'] for d in self.inventario.values())
        return round(total, 2)

    def top_productos(self, n=5):
        """
        Devuelve los N productos con mayor valor total (precio * cantidad).
        """
        productos_ordenados = sorted(
            self.inventario.items(),
            key=lambda item: item[1]['precio'] * item[1]['cantidad'],
            reverse=True
        )
        return [
            (codigo, round(datos['precio'] * datos['cantidad'], 2))
            for codigo, datos in productos_ordenados[:n]
        ]


# ===========================================================================
# EJERCICIO 4: ESTRUCTURAS DE CONTROL
# ===========================================================================

def es_bisiesto(anio):
    """
    Retorna True si el año es bisiesto, False en caso contrario.
    """
    # Regla: divisible entre 400 o divisible entre 4 pero no entre 100
    if (anio % 400) == 0:
        return True
    if (anio % 100) == 0:
        return False
    return (anio % 4) == 0


def dias_en_mes(mes, anio):
    """
    Devuelve el número de días que tiene un mes determinado de un año.
    """
    if mes == 2:
        return 29 if es_bisiesto(anio) else 28
    if mes in {1, 3, 5, 7, 8, 10, 12}:
        return 31
    if mes in {4, 6, 9, 11}:
        return 30
    raise ValueError("Mes inválido")


def generar_calendario(mes, anio, dia_inicio=0):
    """
    Genera una representación textual simple del calendario de un mes.

    dia_inicio: 0=Lunes, ..., 6=Domingo
    """
    dia_inicio = dia_inicio % 7  # Aseguramos que el número sea válido
    dias = dias_en_mes(mes, anio)
    encabezado = "Lu Ma Mi Ju Vi Sa Do"
    lineas = [encabezado]

    # Comenzamos llenando los espacios vacíos antes del primer día
    semana = ["  "] * dia_inicio

    # Recorremos los días y los añadimos a la semana actual
    for dia in range(1, dias + 1):
        semana.append(f"{dia:>2}")
        # Cada 7 días, imprimimos una línea completa
        if len(semana) == 7:
            lineas.append(" ".join(semana))
            semana = []

    # Si quedan días sueltos al final, los agregamos también
    if semana:
        lineas.append(" ".join(semana))

    return "\n".join(lineas)


# ===========================================================================
# EJERCICIO 5: ESTRUCTURAS DE REPETICIÓN
# ===========================================================================

def analizar_ventas(ventas):
    """
    Analiza una lista de ventas y genera estadísticas agregadas.
    """
    total_ventas = 0
    total_descuentos = 0
    ventas_por_producto = {}
    venta_mayor = None
    valor_mayor = -float('inf')

    for v in ventas:
        cantidad = v.get('cantidad', 0)
        precio = v.get('precio', 0.0)
        descuento = v.get('descuento', 0.0)

        # Calculamos el valor real de la venta (ya con descuento)
        valor = cantidad * precio * (1 - descuento)
        ahorro = cantidad * precio * descuento

        total_ventas += valor
        total_descuentos += ahorro

        # Acumulamos la cantidad por producto para hallar el más vendido
        prod = v.get('producto')
        ventas_por_producto[prod] = ventas_por_producto.get(prod, 0) + cantidad

        # Verificamos si esta venta fue la más grande
        if valor > valor_mayor:
            valor_mayor = valor
            venta_mayor = v

    promedio = round(total_ventas / len(ventas), 2) if ventas else 0
    mas_vendido = max(ventas_por_producto, key=ventas_por_producto.get, default=None)

    return {
        'total_ventas': round(total_ventas, 2),
        'promedio_por_venta': promedio,
        'producto_mas_vendido': mas_vendido,
        'venta_mayor': venta_mayor,
        'total_descuentos': round(total_descuentos, 2)
    }


def encontrar_patrones(numeros):
    """
    Encuentra patrones de secuencias ascendentes y descendentes en una lista.
    También identifica números repetidos.
    """
    if not numeros:
        return {
            'secuencias_ascendentes': 0,
            'secuencias_descendentes': 0,
            'longitud_max_ascendente': 0,
            'longitud_max_descendente': 0,
            'numeros_repetidos': {}
        }

    sec_asc = sec_des = max_asc = max_des = 0
    i = 0

    # Recorremos la lista para detectar secuencias consecutivas
    while i < len(numeros) - 1:
        if numeros[i+1] > numeros[i]:
            j = i
            # Avanzamos mientras siga aumentando
            while j + 1 < len(numeros) and numeros[j+1] > numeros[j]:
                j += 1
            longitud = j - i + 1
            sec_asc += 1
            max_asc = max(max_asc, longitud)
            i = j
        elif numeros[i+1] < numeros[i]:
            j = i
            # Avanzamos mientras siga disminuyendo
            while j + 1 < len(numeros) and numeros[j+1] < numeros[j]:
                j += 1
            longitud = j - i + 1
            sec_des += 1
            max_des = max(max_des, longitud)
            i = j
        else:
            # Si son iguales, solo avanzamos un paso
            i += 1

    # Contamos los elementos repetidos
    from collections import Counter
    conteo = Counter(numeros)
    repetidos = {n: c for n, c in conteo.items() if c > 1}

    return {
        'secuencias_ascendentes': sec_asc,
        'secuencias_descendentes': sec_des,
        'longitud_max_ascendente': max_asc,
        'longitud_max_descendente': max_des,
        'numeros_repetidos': repetidos
    }


def simular_crecimiento(principal, tasa_anual, años, aporte_anual=0):
    """
    Simula el crecimiento de una inversión con interés compuesto.

    Cada año se aplica:
      1. Se añade el aporte anual al balance.
      2. Se calcula el interés del nuevo total.
      3. Se almacena el balance final del año.
    """
    resultados = []
    balance = principal

    for año in range(1, años + 1):
        # Aportamos primero (al inicio del año)
        balance += aporte_anual

        # Luego calculamos el interés sobre el total actualizado
        interes = balance * tasa_anual
        balance += interes

        # Guardamos el resultado del año
        resultados.append({
            'años': año,
            'balance': round(balance, 2),
            'interes_ganado': round(interes, 2)
        })

    return resultados


# ===========================================================================
# PRUEBAS (MAIN)
# ===========================================================================

if __name__ == "__main__":
    print("=== PRUEBAS PARTE 1 ===")

    print("\nEjercicio 1: Calculadora")
    print(calculadora_cientifica("suma", 3, 4))
    print(calculadora_cientifica("division", 10, 2))

    print("\nEjercicio 2: Passwords")
    val = ValidadorPassword()
    print(val.validar("Abc123!@"))
    print(val.es_fuerte("Abcdef123!@#X"))

    print("\nEjercicio 3: Inventario")
    inv = GestorInventario()
    inv.agregar_producto("A1", "Teclado", 50, 10, "Accesorios")
    inv.agregar_producto("A2", "Monitor", 800, 3, "Electrónica")
    print(inv.productos_bajo_stock(5))
    print(inv.valor_total_inventario())

    print("\nEjercicio 4: Calendario")
    print(generar_calendario(1, 2025, 2))

    print("\nEjercicio 5: Análisis de ventas")
    ventas = [
        {'producto': 'Mouse', 'cantidad': 10, 'precio': 20, 'descuento': 0.1},
        {'producto': 'Teclado', 'cantidad': 5, 'precio': 40, 'descuento': 0.05}
    ]
    print(analizar_ventas(ventas))
    print(encontrar_patrones([1,2,3,2,1,2,3,4]))
    print(simular_crecimiento(1000, 0.05, 5, 100))

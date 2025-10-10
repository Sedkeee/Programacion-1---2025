#3.1 Validación de Formulario:
def validar_datos(nombre, email, edad, password):
    # Verificar que el nombre tenga entre 2 y 30 caracteres
    if len(nombre) < 2 or len(nombre) > 30:
        return False
    
    # Verificar que el email contenga '@'
    if "@" not in email:
        return False
    
    # Verificar que la edad sea mayor o igual a 18
    if edad < 18:
        return False
    
    # Verificar que la contraseña tenga al menos 8 caracteres
    if len(password) < 8:
        return False
    
    # Si todo está correcto
    return True
# Datos de prueba
print("3.1 Validación de Formulario:")
print(validar_datos("Ana", "ana@email.com", 25, "secreto123"))  # Debe ser True
print(validar_datos("", "no-email", 15, "123"))                 # Debe ser False

print()

#3.2 Sistema de Autorización:
def puede_acceder(usuario, permiso_requerido, lista_negra):
    #Verificar si el usuario está autenticado
    if not usuario["autenticado"]:
        return False

    #Verificar si el usuario está en la lista negra
    if usuario["id"] in lista_negra:
        return False

    #Verificar si es administrador o tiene el permiso requerido
    if usuario["admin"] or permiso_requerido in usuario["permisos"]:
        return True

    #Si no cumple las condiciones anteriores, no puede acceder
    return False
# Usuarios de ejemplo
admin = {
    "id": 1,
    "autenticado": True,
    "admin": True,
    "permisos": ["leer", "escribir"]
}
usuario_normal = {
    "id": 2,
    "autenticado": True,
    "admin": False,
    "permisos": ["leer"]
}
usuario_bloqueado = {
    "id": 3,
    "autenticado": True,
    "admin": False,
    "permisos": ["leer", "escribir"]
}
lista_negra = [3, 4]
# Pruebas
print("3.2 Sistema de Autorización:")
print(puede_acceder(admin, "borrar", lista_negra))            # True  (es admin)
print(puede_acceder(usuario_normal, "leer", lista_negra))     # True  (tiene permiso "leer")
print(puede_acceder(usuario_normal, "escribir", lista_negra)) # False (no tiene permiso)
print(puede_acceder(usuario_bloqueado, "leer", lista_negra))  # False (está en lista negra)

print()

#3.3 Acceso Seguro a Diccionario:
def obtener_valor_seguro(diccionario, clave, predeterminado=None):
    # Recorremos las claves manualmente, sin usar .get()
    if clave in diccionario:
        return diccionario[clave]
    else:
        return predeterminado
# Pruebas
print("3.3 Acceso Seguro a Diccionario:")
config = {"timeout": 30, "retries": 3}
print(obtener_valor_seguro(config, "timeout"))      # 30
print(obtener_valor_seguro(config, "cache"))        # None
print(obtener_valor_seguro(config, "cache", 60))    # 60

print()

#3.4 Filtrar Lista:
def filtrar_productos(productos, precio_min, precio_max, categoria=None):
    filtrados = []

    for producto in productos:
        #Verificar disponibilidad
        if not producto["disponible"]:
            continue

        #Verificar rango de precio
        if not (precio_min <= producto["precio"] <= precio_max):
            continue

        #Verificar categoría (si se especifica)
        if categoria is not None and producto["categoria"] != categoria:
            continue

        #Si pasa todos los filtros, lo agregamos
        filtrados.append(producto)

    return filtrados
# Lista de productos de ejemplo
productos = [
    {"nombre": "Laptop", "precio": 1200, "categoria": "Electrónica", "disponible": True},
    {"nombre": "Teléfono", "precio": 800, "categoria": "Electrónica", "disponible": False},
    {"nombre": "Libro", "precio": 15, "categoria": "Libros", "disponible": True},
    {"nombre": "Audífonos", "precio": 200, "categoria": "Electrónica", "disponible": True},
]
# Pruebas
print("3.4 Filtrar Lista:")
print(filtrar_productos(productos, 0, 500))
print(filtrar_productos(productos, 100, 1000, "Electrónica"))

print()

#3.5 Evaluación de Riesgo:
def evaluar_riesgo(cliente):
    """
    Evalúa si un cliente tiene bajo riesgo crediticio.
    
    Criterios:
    - Score crediticio alto (>700) O
    - Ingreso anual >50000 Y historial > 2 años O
    - Cliente VIP Y sin deudas pendientes
    """
    # Desempaquetar los datos del cliente
    score = cliente["score_crediticio"]
    ingreso = cliente["ingreso_anual"]
    historial = cliente["años_historial"]
    vip = cliente["vip"]
    deudas = cliente["deudas_pendientes"]

    # Aplicar las condiciones del enunciado
    if (
        score > 700
        or (ingreso > 50000 and historial > 2)
        or (vip and not deudas)
    ):
        return True
    else:
        return False
# Datos de prueba
cliente1 = {
    "nombre": "Ana García",
    "score_crediticio": 720,
    "ingreso_anual": 45000,
    "años_historial": 3,
    "vip": False,
    "deudas_pendientes": False
}
cliente2 = {
    "nombre": "Luis Pérez",
    "score_crediticio": 680,
    "ingreso_anual": 60000,
    "años_historial": 4,
    "vip": False,
    "deudas_pendientes": False
}
cliente3 = {
    "nombre": "Carmen Ruiz",
    "score_crediticio": 690,
    "ingreso_anual": 30000,
    "años_historial": 1,
    "vip": True,
    "deudas_pendientes": False
}
# Pruebas
print("3.5 Evaluación de Riesgo:")
print(evaluar_riesgo(cliente1))  # True (score > 700)
print(evaluar_riesgo(cliente2))  # True (ingreso > 50000 y historial > 2)
print(evaluar_riesgo(cliente3))  # True (VIP y sin deudas)

print()
print()
print()

#PROYECTO FINAL: Sistema de Control de Acceso

usuarios = [
    {
        "id": 1,
        "nombre": "Admin",
        "roles": ["admin"],
        "permisos": ["leer", "escribir", "eliminar"],
        "plan": "premium",
        "activo": True,
        "edad": 35
    },
    {
        "id": 2,
        "nombre": "Usuario Regular",
        "roles": ["usuario"],
        "permisos": ["leer"],
        "plan": "basico",
        "activo": True,
        "edad": 17
    },
    {
        "id": 3,
        "nombre": "Usuario Premium Adulto",
        "roles": ["usuario"],
        "permisos": ["leer"],
        "plan": "premium",
        "activo": True,
        "edad": 25
    },
    {
        "id": 4,
        "nombre": "Usuario Inactivo",
        "roles": ["usuario"],
        "permisos": ["leer"],
        "plan": "premium",
        "activo": False,
        "edad": 30
    }
]

recursos = [
    {
        "id": 1,
        "nombre": "Panel Admin",
        "requiere_rol": ["admin"],
        "requiere_permiso": "eliminar",
        "solo_premium": False,
        "solo_adultos": False
    },
    {
        "id": 2,
        "nombre": "Contenido Premium",
        "requiere_rol": ["usuario", "admin"],
        "requiere_permiso": "leer",
        "solo_premium": True,
        "solo_adultos": False
    },
    {
        "id": 3,
        "nombre": "Contenido para Adultos",
        "requiere_rol": ["usuario", "admin"],
        "requiere_permiso": "leer",
        "solo_premium": False,
        "solo_adultos": True
    },
    {
        "id": 4,
        "nombre": "Foro Público",
        "requiere_rol": ["usuario", "admin"],
        "requiere_permiso": "leer",
        "solo_premium": False,
        "solo_adultos": False
    }
]

def puede_acceder_recurso(usuario, recurso):
    #Verificar si el usuario está activo
    if not usuario["activo"]:
        return "Acceso denegado: usuario inactivo."
    
    #Verificar roles
    if not any(rol in usuario["roles"] for rol in recurso["requiere_rol"]):
        return "Acceso denegado: rol insuficiente."
    
    #Verificar permisos
    if recurso["requiere_permiso"] not in usuario["permisos"]:
        return "Acceso denegado: permiso insuficiente."
    
    #Verificar plan premium
    if recurso.get("solo_premium", False) and usuario["plan"] != "premium":
        return "Acceso denegado: requiere plan premium."
    
    #Verificar edad, si es contenido solo para adultos
    if recurso.get("solo_adultos", False) and usuario["edad"] < 18:
        return "Acceso denegado: menor de edad."
    
    # ✅ Si pasa todas las verificaciones
    return "✅ Acceso concedido."

def probar_accesos():
    for usuario in usuarios:
        for recurso in recursos:
            resultado = puede_acceder_recurso(usuario, recurso)
            print(f"Usuario: {usuario['nombre']:25} | Recurso: {recurso['nombre']:25} | Resultado: {resultado}")

probar_accesos()

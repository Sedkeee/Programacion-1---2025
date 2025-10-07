
# Taller: Expresiones Aritméticas en Python
#Rafael Angel Hernandez Gomez


# -------------------------------
# NIVEL 1: Básico (Precedencia Simple)
# -------------------------------

print("Nivel 1 - Básico")

# Ejercicio 1.1
# Predicción: 11
# Explicación: primero se multiplica 3*2 = 6 y luego se suma 5 + 6 = 11
print("Ejercicio 1.1")
print(5 + 3 * 2)  # Resultado: 11

# Ejercicio 1.2
# Predicción: 16
# Explicación: el paréntesis se resuelve primero: (5+3)=8, luego 8*2 = 16
print("Ejercicio 1.2")
print((5 + 3) * 2)  # Resultado: 16

# Ejercicio 1.3
# Predicciones: 5.0, 5, 0
print("Ejercicio 1.3")
print(10 / 2)    # División normal → Resultado: 5.0
print(10 // 2)   # División entera → Resultado: 5
print(10 % 2)    # Resto → Resultado: 0

# Ejercicio 1.4
# Predicciones: 8, 1
print("Ejercicio 1.4")
print(2 ** 3)    # Potencia → Resultado: 8
print(2 ^ 3)     # XOR bit a bit → Resultado: 1

# Ejercicio 1.5
# Predicciones: 8, 15
print("Ejercicio 1.5")
print(5 - -3)    # Resta de negativo → Resultado: 8
print(-5 * -3)   # Negativo * negativo → Resultado: 15

# -------------------------------
# NIVEL 2: Intermedio
# -------------------------------

print("\nNivel 2 - Intermedio")

# Ejercicio 2.1
# Predicción: 9
# Paso a paso: 3*4=12 → 2+12=14 → 14-5=9
print("Ejercicio 2.1")
print(2 + 3 * 4 - 5)  # Resultado: 9

# Ejercicio 2.2
# Predicciones: 10.0, 2.5
print("Ejercicio 2.2")
print(20 / 4 * 2)      # Se resuelve de izq a der: 5.0 * 2 = 10.0
print(20 / (4 * 2))    # Paréntesis primero: 20 / 8 = 2.5

# Ejercicio 2.3
# Predicción: 8
# Paso a paso: 17 % 5 = 2 → 2*3=6 → 2+6=8
print("Ejercicio 2.3")
print(17 % 5 + 2 * 3)  # Resultado: 8

# Ejercicio 2.4
# Predicciones: 512, 64
print("Ejercicio 2.4")
print(2 ** 3 ** 2)      # Derecha a izquierda: 2**(3**2) = 2**9 = 512
print((2 ** 3) ** 2)    # Paréntesis primero: 8**2 = 64

# Ejercicio 2.5
# Predicción: 21.0
# Paso a paso: 5*2=10 → 8/4=2.0 → 10+10=20 → 20-2=18 → 18+3=21.0
print("Ejercicio 2.5")
print(10 + 5 * 2 - 8 / 4 + 3)  # Resultado: 21.0

# -------------------------------
# NIVEL 3: Avanzado
# -------------------------------

print("\nNivel 3 - Avanzado")

# Ejercicio 3.1: Cálculo de impuestos
print("Ejercicio 3.1")
precio = 100
tasa_impuesto = 0.15
total = precio * (1 + tasa_impuesto)
print(f"${total}")  # Resultado: 115.0

# Ejercicio 3.2: Conversión de temperatura
print("Ejercicio 3.2")
celsius = 25
fahrenheit = (celsius * 9 / 5) + 32
print(f"{celsius}°C = {fahrenheit}°F")  # Resultado: 77.0°F

# Ejercicio 3.3: Promedio de calificaciones
print("Ejercicio 3.3")
nota1 = 85
nota2 = 90
nota3 = 78
promedio = (nota1 + nota2 + nota3) / 3
print(f"Promedio: {promedio}")  # Resultado: 84.33

# Ejercicio 3.4: Dividir cuenta
print("Ejercicio 3.4")
cuenta_total = 127.50
num_personas = 4
por_persona = cuenta_total / num_personas
print(f"Cada persona paga: ${por_persona}")  # Resultado: 31.88

# Ejercicio 3.5: Tiempo restante
print("Ejercicio 3.5")
minutos_totales = 125
horas = minutos_totales // 60
minutos = minutos_totales % 60
print(f"{minutos_totales} minutos = {horas}h y {minutos}min")  # Resultado: 2h y 5min

# -------------------------------
# PROYECTO FINAL: Calculadora de Expresiones
# -------------------------------

def evaluar_expresion(expresion):
    try:
        resultado = eval(expresion)
        print(f"Resultado: {resultado}")
        print(f"Tipo: {type(resultado).__name__}")
        if isinstance(resultado, float) and resultado.is_integer():
            print(f"Nota: Es un número entero: {int(resultado)}")
        return resultado
    except ZeroDivisionError:
        print("Error: División por cero.")
    except SyntaxError:
        print("Error: Sintaxis inválida.")
    except NameError:
        print("Error: Variable no definida.")
    except Exception as e:
        print(f"Error desconocido: {e}")

def calculadora():
    print("\n=== CALCULADORA DE EXPRESIONES ===")
    print("Escribe una expresión como: 5 + 3 * 2, (10 + 5) * 2, etc.")
    print("Comandos especiales: 'salir', 'historial'\n")

    historial = []

    while True:
        expresion = input("Expresión: ").strip()
        
        if expresion.lower() == "salir":
            print("Gracias por usar la calculadora.")
            break

        if expresion.lower() == "historial":
            print("\nHistorial de operaciones:")
            for i, (exp, res) in enumerate(historial, 1):
                print(f"{i}. {exp} = {res}")
            print()
            continue

        if not expresion:
            continue

        resultado = evaluar_expresion(expresion)
        if resultado is not None:
            historial.append((expresion, resultado))

# Ejecutar la calculadora solo si este archivo es el principal
if __name__ == "__main__":
    calculadora()

# -------------------------------
#DEBUGGING
# -------------------------------

print("\nDEBUGGING")

# Debug 1: Error en promedio
print("Debug 1")
a = 10
b = 20
c = 30
# Promedio incorrecto:
# promedio = a + b + c / 3
# Promedio correcto:
promedio = (a + b + c) / 3
print(f"Promedio corregido: {promedio}")  # Resultado: 20.0

# Debug 2: Descuento mal calculado
print("Debug 2")
precio = 50
descuento = 20
# Incorrecto: final = precio - descuento * precio
precio_final = precio * (1 - descuento / 100)
print(f"Precio con 20% de descuento: ${precio_final}")  # Resultado: 40.0


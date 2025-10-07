# Ejercicios Prácticos: Expresiones Aritméticas

## 📝 Instrucciones

- Resuelve los ejercicios en orden
- Intenta predecir el resultado antes de ejecutar el código
- Verifica tus respuestas con Python
- Si te equivocas, analiza por qué

---

## 🟢 NIVEL 1: Básico (Precedencia Simple)

### Ejercicio 1.1: Predice el Resultado
```python
print(5 + 3 * 2)
```
**Tu predicción**: _______  
**Resultado real**: _______  
**Explicación**: _______

<details>
<summary>Ver Solución</summary>

**Resultado**: 11  
**Explicación**: Multiplicación primero (3 * 2 = 6), luego suma (5 + 6 = 11)
</details>

### Ejercicio 1.2: Paréntesis
```python
print((5 + 3) * 2)
```
**Tu predicción**: _______

<details>
<summary>Ver Solución</summary>

**Resultado**: 16  
**Explicación**: Paréntesis primero (5 + 3 = 8), luego multiplicación (8 * 2 = 16)
</details>

### Ejercicio 1.3: División
```python
print(10 / 2)
print(10 // 2)
print(10 % 2)
```
**Tus predicciones**: _______, _______, _______

<details>
<summary>Ver Solución</summary>

**Resultados**: 5.0, 5, 0  
**Explicación**:
- `10 / 2 = 5.0` (división normal, siempre float)
- `10 // 2 = 5` (división entera)
- `10 % 2 = 0` (resto, 10 es divisible por 2)
</details>

### Ejercicio 1.4: Potencia
```python
print(2 ** 3)
print(2 ^ 3)
```
**Tus predicciones**: _______, _______

<details>
<summary>Ver Solución</summary>

**Resultados**: 8, 1  
**Explicación**:
- `2 ** 3 = 8` (potencia correcta: 2×2×2)
- `2 ^ 3 = 1` (XOR bit a bit, NO potencia)
</details>

### Ejercicio 1.5: Negación
```python
print(5 - -3)
print(-5 * -3)
```
**Tus predicciones**: _______, _______

<details>
<summary>Ver Solución</summary>

**Resultados**: 8, 15  
**Explicación**:
- `5 - (-3) = 5 + 3 = 8` (restar negativo = sumar)
- `-5 * -3 = 15` (negativo × negativo = positivo)
</details>

---

## 🟡 NIVEL 2: Intermedio (Expresiones Complejas)

### Ejercicio 2.1: Múltiples Operadores
```python
print(2 + 3 * 4 - 5)
```
**Tu predicción**: _______  
**Paso a paso**: _______

<details>
<summary>Ver Solución</summary>

**Resultado**: 9  
**Paso a paso**:
1. `3 * 4 = 12` (multiplicación primero)
2. `2 + 12 = 14` (suma)
3. `14 - 5 = 9` (resta)
</details>

### Ejercicio 2.2: División y Multiplicación
```python
print(20 / 4 * 2)
print(20 / (4 * 2))
```
**Tus predicciones**: _______, _______

<details>
<summary>Ver Solución</summary>

**Resultados**: 10.0, 2.5  
**Explicación**:
- `20 / 4 * 2`: Izquierda a derecha → (20/4)*2 = 5.0*2 = 10.0
- `20 / (4 * 2)`: Paréntesis primero → 20/8 = 2.5
</details>

### Ejercicio 2.3: Módulo en Expresión
```python
print(17 % 5 + 2 * 3)
```
**Tu predicción**: _______

<details>
<summary>Ver Solución</summary>

**Resultado**: 8  
**Paso a paso**:
1. `17 % 5 = 2` (resto de 17÷5)
2. `2 * 3 = 6` (multiplicación)
3. `2 + 6 = 8` (suma)
</details>

### Ejercicio 2.4: Potencias Anidadas
```python
print(2 ** 3 ** 2)
print((2 ** 3) ** 2)
```
**Tus predicciones**: _______, _______

<details>
<summary>Ver Solución</summary>

**Resultados**: 512, 64  
**Explicación**:
- `2 ** 3 ** 2`: Derecha a izquierda → 2**(3**2) = 2**9 = 512
- `(2 ** 3) ** 2`: Paréntesis primero → 8**2 = 64
</details>

### Ejercicio 2.5: Expresión Compleja
```python
print(10 + 5 * 2 - 8 / 4 + 3)
```
**Tu predicción**: _______  
**Paso a paso**: _______

<details>
<summary>Ver Solución</summary>

**Resultado**: 21.0  
**Paso a paso**:
1. `5 * 2 = 10` (multiplicación)
2. `8 / 4 = 2.0` (división)
3. `10 + 10 = 20` (suma, izq a der)
4. `20 - 2.0 = 18.0` (resta)
5. `18.0 + 3 = 21.0` (suma)
</details>

---

## 🔴 NIVEL 3: Avanzado (Problemas del Mundo Real)

### Ejercicio 3.1: Cálculo de Impuestos
Calcula el total con impuesto del 15% sobre una compra de $100.

```python
price = 100
tax_rate = 0.15

# Escribe la expresión correcta:
total = ?
```

<details>
<summary>Ver Solución</summary>

```python
# Opción 1: Calcular impuesto por separado
tax = price * tax_rate
total = price + tax

# Opción 2: En una expresión
total = price * (1 + tax_rate)

# Resultado: $115.00
```
</details>

### Ejercicio 3.2: Conversión de Temperatura
Convierte 25°C a Fahrenheit usando la fórmula: F = (C × 9/5) + 32

```python
celsius = 25

# Escribe la expresión:
fahrenheit = ?
```

<details>
<summary>Ver Solución</summary>

```python
fahrenheit = (celsius * 9 / 5) + 32
# O también:
fahrenheit = celsius * 9 / 5 + 32  # Funciona por precedencia

# Resultado: 77.0°F
```
</details>

### Ejercicio 3.3: Promedio de Calificaciones
Calcula el promedio de 3 calificaciones: 85, 90, 78

```python
grade1 = 85
grade2 = 90
grade3 = 78

# Escribe la expresión correcta:
average = ?
```

<details>
<summary>Ver Solución</summary>

```python
average = (grade1 + grade2 + grade3) / 3

# Resultado: 84.33...
```
</details>

### Ejercicio 3.4: Dividir Cuenta
4 amigos van a cenar. La cuenta es $127.50. Calcula cuánto paga cada uno.

```python
total_bill = 127.50
num_people = 4

per_person = ?
```

<details>
<summary>Ver Solución</summary>

```python
per_person = total_bill / num_people

# Resultado: $31.875 (o $31.88 redondeado)
```
</details>

### Ejercicio 3.5: Tiempo Restante
Tienes 125 minutos. ¿Cuántas horas y minutos son?

```python
total_minutes = 125

hours = ?
minutes = ?
```

<details>
<summary>Ver Solución</summary>

```python
hours = total_minutes // 60  # División entera
minutes = total_minutes % 60  # Resto

# Resultado: 2 horas y 5 minutos
```
</details>

---

## 🎯 PROYECTO FINAL: Calculadora de Expresiones

### Descripción
Crea un programa que:
1. Solicite una expresión al usuario
2. Evalúe la expresión
3. Muestre el resultado
4. Maneje errores básicos

### Requisitos Mínimos
```python
# Tu código aquí
expression = input("Ingresa una expresión: ")

# Evaluar y mostrar resultado
# Manejar división por cero
# Manejar expresiones inválidas
```

### Solución Básica

<details>
<summary>Ver Solución Básica</summary>

```python
"""
Simple Expression Calculator
"""

print("=== CALCULADORA DE EXPRESIONES ===")
print("Operadores: +, -, *, /, //, %, **")
print()

while True:
    expression = input("Ingresa una expresión (o 'salir' para terminar): ")
    
    if expression.lower() == 'salir':
        print("¡Hasta luego!")
        break
    
    try:
        result = eval(expression)
        print(f"Resultado: {result}")
        print(f"Tipo: {type(result).__name__}")
        print()
    except ZeroDivisionError:
        print("❌ Error: División por cero")
        print()
    except:
        print("❌ Error: Expresión inválida")
        print()
```
</details>

### Solución Avanzada (Con Pasos)

<details>
<summary>Ver Solución Avanzada</summary>

```python
"""
Advanced Expression Calculator with Step-by-Step Evaluation
"""

def evaluate_with_steps(expression):
    """Evaluate expression and show steps."""
    print(f"\nExpresión: {expression}")
    print("-" * 50)
    
    try:
        # Evaluate
        result = eval(expression)
        
        # Show result
        print(f"Resultado: {result}")
        print(f"Tipo: {type(result).__name__}")
        
        # Show some analysis
        if isinstance(result, float) and result.is_integer():
            print(f"Nota: El resultado es un número entero: {int(result)}")
        
        return result
        
    except ZeroDivisionError:
        print("❌ Error: División por cero")
        return None
    except SyntaxError:
        print("❌ Error: Sintaxis inválida")
        return None
    except NameError:
        print("❌ Error: Variable no definida")
        return None
    except:
        print("❌ Error desconocido")
        return None

def main():
    """Main calculator loop."""
    print("=" * 50)
    print("CALCULADORA DE EXPRESIONES ARITMÉTICAS")
    print("=" * 50)
    print("\nOperadores disponibles:")
    print("  +   Suma")
    print("  -   Resta")
    print("  *   Multiplicación")
    print("  /   División")
    print("  //  División entera")
    print("  %   Módulo (resto)")
    print("  **  Potencia")
    print("\nEjemplos:")
    print("  5 + 3 * 2")
    print("  (10 + 5) * 2")
    print("  2 ** 3")
    print()
    
    history = []
    
    while True:
        expression = input("Expresión (o 'salir'/'historial'): ").strip()
        
        if expression.lower() == 'salir':
            print("\n¡Gracias por usar la calculadora!")
            break
        
        if expression.lower() == 'historial':
            if history:
                print("\n=== HISTORIAL ===")
                for i, (expr, res) in enumerate(history, 1):
                    print(f"{i}. {expr} = {res}")
                print()
            else:
                print("\nNo hay historial aún.\n")
            continue
        
        if not expression:
            continue
        
        result = evaluate_with_steps(expression)
        
        if result is not None:
            history.append((expression, result))

if __name__ == "__main__":
    main()
```
</details>

---

## 📊 Ejercicios de Debugging

### Debug 1: Encuentra el Error
```python
# Este código debería calcular el promedio
a = 10
b = 20
c = 30
average = a + b + c / 3
print(f"Promedio: {average}")
```

**¿Qué está mal?** _______

<details>
<summary>Ver Solución</summary>

**Error**: Solo divide `c` por 3  
**Correcto**: `average = (a + b + c) / 3`  
**Resultado incorrecto**: 40.0  
**Resultado correcto**: 20.0
</details>

### Debug 2: Encuentra el Error
```python
# Calcular 20% de descuento sobre $50
price = 50
discount = 20
final = price - discount * price
print(f"Precio final: ${final}")
```

**¿Qué está mal?** _______

<details>
<summary>Ver Solución</summary>

**Error**: Multiplica descuento por precio (20 * 50 = 1000)  
**Correcto**: `final = price - (discount / 100) * price`  
O mejor: `final = price * (1 - discount / 100)`  
**Resultado incorrecto**: -950  
**Resultado correcto**: 40.0
</details>

---

## ✅ Autoevaluación

Marca los ejercicios que completaste correctamente:

### Nivel 1 (Básico)
- [ ] Ejercicio 1.1
- [ ] Ejercicio 1.2
- [ ] Ejercicio 1.3
- [ ] Ejercicio 1.4
- [ ] Ejercicio 1.5

### Nivel 2 (Intermedio)
- [ ] Ejercicio 2.1
- [ ] Ejercicio 2.2
- [ ] Ejercicio 2.3
- [ ] Ejercicio 2.4
- [ ] Ejercicio 2.5

### Nivel 3 (Avanzado)
- [ ] Ejercicio 3.1
- [ ] Ejercicio 3.2
- [ ] Ejercicio 3.3
- [ ] Ejercicio 3.4
- [ ] Ejercicio 3.5

### Proyecto Final
- [ ] Calculadora básica
- [ ] Calculadora avanzada

---

## 🎯 Próximos Pasos

Si completaste todos los ejercicios:
1. ✅ Practica con problemas del mundo real
2. ✅ Crea tus propias expresiones complejas
3. ✅ Ayuda a tus compañeros
4. ✅ Explora el módulo `math` de Python

**¡Excelente trabajo! 🚀**

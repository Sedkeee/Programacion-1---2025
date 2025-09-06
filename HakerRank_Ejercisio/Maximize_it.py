from itertools import product

entrada = input().split()
K = int(entrada[0])
M = int(entrada[1])

listas = []
for _ in range(K):
    datos = input().split()
    numeros = []
    for i in range(1, len(datos)):
        numeros.append(int(datos[i]))
    listas.append(numeros)

def maximoValor(lists, M):
    maximo = 0

    todas = product(*lists)

    for combo in todas:
        sumaCuadrados = 0
        for numero in combo:
            cuadrado = numero ** 2
            sumaCuadrados += cuadrado

        resto = sumaCuadrados % M

        if resto > maximo:
            maximo = resto

    return maximo

resultado = maximoValor(listas, M)
print(resultado)

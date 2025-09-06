#Rafael Angel Hernandez Gomez

palabra = input("Ingrese la palabra: ")

#Condicion para validar que haya una palabra.
if palabra == "":
    print("Error: la palabra no puede estar vacía.")
    exit()

vocales = "aeiouAEIOU"

#Competencia 
jugador_vocales = []       # Jugador A
jugador_consonantes = []   # Jugador B


for inicio in range(len(palabra)):
    for fin in range(inicio + 1, len(palabra) + 1):
        subcadena = palabra[inicio:fin]
        
        if palabra[inicio] in vocales:
            jugador_vocales.append(subcadena)
        else:
            jugador_consonantes.append(subcadena)

#Resultados
print("\n--- RESULTADOS ---")
print("Substrings que empiezan con vocales (Jugador A):", jugador_vocales)
print("Cantidad:", len(jugador_vocales))
print()
print("Substrings que empiezan con consonantes (Jugador B):", jugador_consonantes)
print("Cantidad:", len(jugador_consonantes))
print()

#Determinar quien gano.
if len(jugador_vocales) > len(jugador_consonantes):
    print("gana el Jugador A con", len(jugador_vocales), "substrings")
elif len(jugador_consonantes) > len(jugador_vocales):
    print("gana el Jugador B con", len(jugador_consonantes), "substrings")
else:
    print("empate con", len(jugador_vocales), "substrings cada uno.")
from pyswip import Prolog

# Cargar el código Prolog desde el archivo
prolog = Prolog()
prolog.consult("prueba2.pl")
def tablero_prolog(tablero):
    # Convertir el tablero de Python a una lista de listas en Prolog
    filas = []
    for fila in tablero:
        filas.append(f"[{','.join(map(str, fila))}]")
    tablero_prolog = f"[{','.join(filas)}]"
    return tablero_prolog

def jugada_calculada(jugador, tablero):
    jugadas_lista = []

    # Convertir el tablero de Python a una lista de listas en Prolog
    tablero_prolog_str = tablero_prolog(tablero)

    # Consultar jugadas válidas para el jugador en el tablero dado
    result = list(prolog.query(f"jugadas_validas({jugador}, {tablero_prolog_str}, Jugadas)"))

    if result:
        jugadas = result[0]["Jugadas"]
        print("Jugadas válidas para el jugador", jugador, ":")
        for jugada in jugadas:
            fila = jugada.args[0] - 1
            columna = jugada.args[1] - 1
            jugadas_lista.append((fila, columna))
        
        # Eliminar duplicados de la lista de jugadas
        jugadas_lista = list(set(jugadas_lista))
    
    return jugadas_lista


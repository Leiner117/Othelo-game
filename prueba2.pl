% Predicado para obtener todas las jugadas válidas para un jugador en el tablero
jugadas_validas(Jugador, Tablero, ListaJugadas) :-
    dimensiones_tablero(Tablero, NumFilas, NumColumnas),
    findall((Fila, Columna), (
        between(1, NumFilas, Fila),             % Iterar sobre filas
        between(1, NumColumnas, Columna),       % Iterar sobre columnas
        casilla_vacia(Fila, Columna, Tablero),  % Verificar si la casilla está vacía (0)
        jugada_valida(Jugador, Fila, Columna, Tablero)  % Verificar si es una jugada válida
    ), ListaJugadas).

% Predicado para verificar si una casilla está vacía
casilla_vacia(Fila, Columna, Tablero) :-
    nth1(Fila, Tablero, FilaTablero),   % Obtener la fila del tablero
    nth1(Columna, FilaTablero, 0).      % Verificar si la casilla está vacía (0)

% Predicado para verificar si una jugada es válida para un jugador en una posición dada
jugada_valida(Jugador, Fila, Columna, Tablero) :-
    oponente(Jugador, Oponente),  % Obtener al oponente del jugador
    direcciones(Direcciones),     % Obtener las direcciones posibles
    member((DirF, DirC), Direcciones),  % Iterar sobre cada dirección posible
    validar_jugada(Jugador, Oponente, Fila, Columna, DirF, DirC, Tablero).

% Direcciones posibles para verificar
direcciones([(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1)]).

% Predicado para validar una jugada en una dirección específica
validar_jugada(Jugador, Oponente, Fila, Columna, DirF, DirC, Tablero) :-
    Fila2 is Fila + DirF,               % Calcular la fila siguiente
    Columna2 is Columna + DirC,         % Calcular la columna siguiente
    dentro_tablero(Fila2, Columna2, Tablero),  % Verificar si está dentro del tablero
    casilla_contiene(Fila2, Columna2, Oponente, Tablero),  % Verificar si la casilla contiene al oponente
    seguir_linea(Jugador, Fila2, Columna2, DirF, DirC, Tablero).

% Predicado para seguir una línea en una dirección específica y validar si se pueden voltear fichas
seguir_linea(Jugador, Fila, Columna, DirF, DirC, Tablero) :-
    Fila2 is Fila + DirF,
    Columna2 is Columna + DirC,
    dentro_tablero(Fila2, Columna2, Tablero),
    casilla_contiene(Fila2, Columna2, Oponente, Tablero),
    seguir_linea(Jugador, Fila2, Columna2, DirF, DirC, Tablero).
seguir_linea(Jugador, Fila, Columna, DirF, DirC, Tablero) :-
    Fila2 is Fila + DirF,
    Columna2 is Columna + DirC,
    dentro_tablero(Fila2, Columna2, Tablero),
    casilla_contiene(Fila2, Columna2, Jugador, Tablero).

% Predicado para verificar si una casilla contiene un cierto valor en el tablero
casilla_contiene(Fila, Columna, Contenido, Tablero) :-
    nth1(Fila, Tablero, FilaTablero),   % Obtener la fila del tablero
    nth1(Columna, FilaTablero, Contenido).  % Verificar el contenido de la casilla

% Predicado para obtener las dimensiones del tablero (filas y columnas)
dimensiones_tablero(Tablero, NumFilas, NumColumnas) :-
    length(Tablero, NumFilas),  % Obtener el número de filas del tablero
    (   NumFilas > 0 ->
        nth1(1, Tablero, Fila),
        length(Fila, NumColumnas)  % Obtener el número de columnas de la primera fila
    ;   NumColumnas = 0  % Si el tablero está vacío, el número de columnas es 0
    ).

% Predicado para verificar si una posición está dentro del tablero
dentro_tablero(Fila, Columna, Tablero) :-
    dimensiones_tablero(Tablero, NumFilas, NumColumnas),
    Fila >= 1, Fila =< NumFilas,         % Verificar límites de fila
    Columna >= 1, Columna =< NumColumnas.  % Verificar límites de columna

% Predicado para determinar quién es el oponente de un jugador
oponente(1, 2).  % oponente de black es white
oponente(2, 1).  % oponente de white es black

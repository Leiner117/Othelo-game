% Predicado para obtener todas las jugadas válidas para un jugador en el tablero
jugadas_validas(Jugador, Tablero, ListaJugadas) :-
    dimensiones_tablero(Tablero, NumFilas, NumColumnas),
    findall((Fila, Columna), (
        between(1, NumFilas, Fila),             % Iterar sobre filas
        between(1, NumColumnas, Columna),       % Iterar sobre columnas
        nth1(Fila, Tablero, FilaTablero),       % Obtener la fila del tablero
        nth1(Columna, FilaTablero, 0),          % Verificar si la casilla está vacía (0)
        jugada_valida(Jugador, Fila, Columna, Tablero, _Comio)  % Verificar si es una jugada válida y si come al menos una ficha del oponente
    ), ListaJugadas).

% Predicado para verificar si una jugada es válida para un jugador en una posición dada
jugada_valida(Jugador, Fila, Columna, Tablero, Comio) :-
    oponente(Jugador, Oponente),
    member((DirF, DirC), [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1)]),  % Direcciones posibles
    validar_jugada(Jugador, Fila, Columna, DirF, DirC, Oponente, Tablero, Comio).

% Predicado para validar una jugada en una dirección específica
validar_jugada(Jugador, Fila, Columna, DirF, DirC, Oponente, Tablero, Comio) :-
    Fila2 is Fila + DirF,               % Calcular la fila siguiente
    Columna2 is Columna + DirC,         % Calcular la columna siguiente
    dentro_tablero(Fila2, Columna2, Tablero),  % Verificar si está dentro del tablero
    casilla_contiene(Fila2, Columna2, Oponente, Tablero),    % Verificar si la casilla contiene al oponente
    % Probar si se pueden voltear fichas en esta dirección
    seguir_linea(Jugador, Fila2, Columna2, DirF, DirC, Oponente, Tablero, _),
    Comio = true.  % Marcar que se comió al menos una ficha del oponente

% Predicado para seguir una línea en una dirección específica y validar si se pueden voltear fichas
seguir_linea(_, Fila, Columna, DirF, DirC, Jugador, Tablero, _) :-
    casilla_contiene(Fila, Columna, Jugador, Tablero).  % Encontramos una ficha del jugador
seguir_linea(Jugador, Fila, Columna, DirF, DirC, Oponente, Tablero, _) :-
    casilla_contiene(Fila, Columna, Oponente, Tablero),  % Encontramos una ficha del oponente
    Fila2 is Fila + DirF,
    Columna2 is Columna + DirC,
    dentro_tablero(Fila2, Columna2, Tablero),
    seguir_linea(Jugador, Fila2, Columna2, DirF, DirC, Oponente, Tablero, _).

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


% Predicado para determinar quién es el oponente de un jugador
oponente(1, 2).  % oponente de black es white
oponente(2, 1).  % oponente de white es black

dentro_tablero(Fila, Columna, Tablero) :-
    dimensiones_tablero(Tablero, NumFilas, NumColumnas),
    Fila >= 1 , Fila =< NumFilas,         % Verificar límites de fila
    Columna >= 1, Columna =< NumColumnas.  % Verificar límites de columna
% Ejemplo de tablero para Othello (8x8)
tablero_ejemplo([
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,2,1,0,0,0],
    [0,0,0,1,2,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0]
]).
% Ejemplo de consulta para mostrar la mejor jugada para el jugador negro en el tablero de ejemplo
ejemplo_mejor_jugada :-
    tablero_ejemplo(Tablero),
    mejor_jugada_captura(1, Tablero, MejorJugada), % Jugador negro es 1 en este ejemplo
    write('La mejor jugada para el jugador negro es: '),
    write(MejorJugada),
    nl.

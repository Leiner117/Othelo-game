% Predicate to get all valid moves for a player on the board
valid_moves(Player, Board, MoveList) :-
    board_dimensions(Board, NumRows, NumColumns),
    findall((Row, Column), (
        between(1, NumRows, Row),             % Iterate over rows
        between(1, NumColumns, Column),       % Iterate over columns
        empty_cell(Row, Column, Board),       % Check if the cell is empty (0)
        valid_move(Player, Row, Column, Board)  % Check if its a valid move
    ), MoveList).

% Predicate to check if a cell is empty
empty_cell(Row, Column, Board) :-
    nth1(Row, Board, RowBoard),   % Get the row from the board
    nth1(Column, RowBoard, 0).    % Check if the cell is empty (0)

% Predicate to check if a move is valid for a player at a given position
valid_move(Player, Row, Column, Board) :-
    opponent(Player, Opponent),    % Get the opponent of the player
    directions(Directions),        % Get possible directions
    member((DirRow, DirColumn), Directions),  % Iterate over each possible direction
    validate_move(Player, Opponent, Row, Column, DirRow, DirColumn, Board).

% Possible directions to check
directions([(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1)]).

% Predicate to validate a move in a specific direction
validate_move(Player, Opponent, Row, Column, DirRow, DirColumn, Board) :-
    Row2 is Row + DirRow,               % Calculate the next row
    Column2 is Column + DirColumn,      % Calculate the next column
    inside_board(Row2, Column2, Board),  % Check if its inside the board
    cell_contains(Row2, Column2, Opponent, Board),  % Check if the cell contains the opponent
    follow_line(Player, Row2, Column2, DirRow, DirColumn, Board).

% Predicate to follow a line in a specific direction and validate if pieces can be flipped
follow_line(Player, Row, Column, DirRow, DirColumn, Board) :-
    Row2 is Row + DirRow,
    Column2 is Column + DirColumn,
    inside_board(Row2, Column2, Board),
    cell_contains(Row2, Column2, Opponent, Board),
    follow_line(Player, Row2, Column2, DirRow, DirColumn, Board).
follow_line(Player, Row, Column, DirRow, DirColumn, Board) :-
    Row2 is Row + DirRow,
    Column2 is Column + DirColumn,
    inside_board(Row2, Column2, Board),
    cell_contains(Row2, Column2, Player, Board).

% Predicate to check if a cell contains a certain value on the board
cell_contains(Row, Column, Content, Board) :-
    nth1(Row, Board, RowBoard),    % Get the row from the board
    nth1(Column, RowBoard, Content).  % Check the content of the cell

% Predicate to get the dimensions of the board (rows and columns)
board_dimensions(Board, NumRows, NumColumns) :-
    length(Board, NumRows),  % Get the number of rows of the board
    (   NumRows > 0 ->
        nth1(1, Board, Row),
        length(Row, NumColumns)  % Get the number of columns of the first row
    ;   NumColumns = 0  % If the board is empty, the number of columns is 0
    ).

% Predicate to check if a position is inside the board
inside_board(Row, Column, Board) :-
    board_dimensions(Board, NumRows, NumColumns),
    Row >= 1, Row =< NumRows,         % Check row limits
    Column >= 1, Column =< NumColumns.  % Check column limits

% Predicate to determine who is the opponent of a player
opponent(1, 2).  % Opponent of black is white
opponent(2, 1).  % Opponent of white is black

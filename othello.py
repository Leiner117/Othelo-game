from pyswip import Prolog

# Load Prolog code from the file
prolog = Prolog()
prolog.consult("busqueda1.pl")

def prolog_board(board):
    """
    Convert the Python board to a list of lists in Prolog format.

    Args:
        board (list): The game board represented as a 2D list.

    Returns:
        str: The Prolog representation of the board.
    """
    rows = []
    for row in board:
        rows.append(f"[{','.join(map(str, row))}]")
    prolog_board = f"[{','.join(rows)}]"
    return prolog_board

def calculated_move(player, board):
    """
    Calculate the next move for the player using Prolog.

    Args:
        player (int): The player making the move (1 for black, 2 for white).
        board (list): The game board represented as a 2D list.

    Returns:
        tuple: The coordinates of the calculated move (row, column).
    """
    possible_moves = []

    # Convert the Python board to Prolog format
    prolog_board_str = prolog_board(board)

    # Query valid moves for the player on the given board
    result = list(prolog.query(f"valid_moves({player}, {prolog_board_str}, Moves)"))
    moves = result[0]["Moves"]
    if len(moves) > 0:
        
        for move in moves:
            row = move.args[0] - 1
            column = move.args[1] - 1
            possible_moves.append((row, column))
        
        # Remove duplicates from the list of moves
        possible_moves = list(set(possible_moves))
    else:
        return 0
    return possible_moves[0]

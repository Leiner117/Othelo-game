import tkinter as tk
from tkinter import messagebox
from othello import calculated_move

# Constants
EMPTY = 0
BLACK = 1
WHITE = 2

def draw_board(canvas, board):
    """
    Draw the game board on the canvas.

    Args:
        canvas (tk.Canvas): The canvas widget to draw on.
        board (list): The game board represented as a 2D list.
    """
    canvas.delete("pieces")  # Remove all existing pieces
    canvas.delete("invalid")  # Remove any previous highlighting of invalid cells

    cell_size = 400 // len(board)

    # Draw the board cells
    for row in range(len(board)):
        for col in range(len(board)):
            x1 = col * cell_size
            y1 = row * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            canvas.create_rectangle(x1, y1, x2, y2, fill="green", tags="board")

            # Draw pieces based on the board state
            if board[row][col] == BLACK:
                canvas.create_oval(x1+2, y1+2, x2-2, y2-2, fill="black", tags="pieces")
            elif board[row][col] == WHITE:
                canvas.create_oval(x1+2, y1+2, x2-2, y2-2, fill="white", tags="pieces")

    # Highlight invalid moves
    highlight_invalid_moves(canvas, board)

def on_click(event, canvas, board, current_player, score_labels, root):
    """
    Handle mouse click events on the canvas.

    Args:
        event: The mouse click event.
        canvas (tk.Canvas): The canvas widget.
        board (list): The game board represented as a 2D list.
        current_player (int): The current player (BLACK or WHITE).
        score_labels (list): Labels displaying the scores of players.
        root: The root Tkinter window.
    """
    row = event.y // (400 // len(board))
    col = event.x // (400 // len(board))
    
    if current_player == BLACK:
        if is_valid_move(board, row, col, current_player):
            make_move(board, row, col, BLACK)
            current_player = WHITE
            draw_board(canvas, board)
            update_scores(board, score_labels)
            
            # Make white move after 0.5 seconds
            canvas.after(500, lambda: make_white_move(canvas, board, score_labels, root))
            if board_is_full(board):
                check_winner(board, root)

def make_white_move(canvas, board, score_labels, root):
    """
    Make a move for the white player.

    Args:
        canvas (tk.Canvas): The canvas widget.
        board (list): The game board represented as a 2D list.
        score_labels (list): Labels displaying the scores of players.
        root: The root Tkinter window.
    """
    play = calculated_move(WHITE, board)
    if play != 0:
        valid_move = play
        make_move(board, valid_move[0], valid_move[1], WHITE)
        draw_board(canvas, board)
        update_scores(board, score_labels)
        if board_is_full(board):
            check_winner(board, root)
    else:
        messagebox.showinfo("Result", "You win!")
        root.destroy()
        
def is_valid_move(board, row, col, player):
    """
    Check if a move is valid for the given player.

    Args:
        board (list): The game board represented as a 2D list.
        row (int): The row index of the move.
        col (int): The column index of the move.
        player (int): The player making the move.

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    if board[row][col] != EMPTY:
        return False
    
    opponent = WHITE if player == BLACK else BLACK
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        cells_to_flip = []

        while 0 <= r < len(board) and 0 <= c < len(board) and board[r][c] == opponent:
            cells_to_flip.append((r, c))
            r += dr
            c += dc

        if 0 <= r < len(board) and 0 <= c < len(board) and board[r][c] == player and cells_to_flip:
            return True
    
    return False

def make_move(board, row, col, player):
    """
    Make a move on the board for the specified player.

    Args:
        board (list): The game board represented as a 2D list.
        row (int): The row index of the move.
        col (int): The column index of the move.
        player (int): The player making the move.
    """
    board[row][col] = player

    opponent = WHITE if player == BLACK else BLACK
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        cells_to_flip = []

        while 0 <= r < len(board) and 0 <= c < len(board) and board[r][c] == opponent:
            cells_to_flip.append((r, c))
            r += dr
            c += dc

        if 0 <= r < len(board) and 0 <= c < len(board) and board[r][c] == player and cells_to_flip:
            for flip_row, flip_col in cells_to_flip:
                board[flip_row][flip_col] = player

def highlight_invalid_moves(canvas, board):
    """
    Highlight invalid moves on the board canvas.

    Args:
        canvas (tk.Canvas): The canvas widget.
        board (list): The game board represented as a 2D list.
    """
    for row in range(len(board)):
        for col in range(len(board)):
            if not is_valid_move(board, row, col, BLACK):
                cell_size = 400 // len(board)
                x1 = col * cell_size
                y1 = row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                canvas.create_rectangle(x1, y1, x2, y2, fill="red", stipple="gray12", tags="invalid")

def change_turn(canvas, board, current_player, score_labels, root):
    """
    Change the turn from black to white or vice versa.

    Args:
        canvas (tk.Canvas): The canvas widget.
        board (list): The game board represented as a 2D list.
        current_player (int): The current player (BLACK or WHITE).
        score_labels (list): Labels displaying the scores of players.
        root: The root Tkinter window.
    """
    if current_player == BLACK:
        current_player = WHITE
        make_white_move(canvas, board, score_labels,root)
        if board_is_full(board):
            check_winner(board, root)
    else:
        current_player = BLACK
        draw_board(canvas, board)
        update_scores(board, score_labels)
        if board_is_full(board):
            check_winner(board, root)
       
def board_is_full(board):
    """
    Check if the game board is full.

    Args:
        board (list): The game board represented as a 2D list.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for row in board:
        if EMPTY in row:
            return False
    return True

def update_scores(board, score_labels):
    """
    Update the scores displayed on the GUI.

    Args:
        board (list): The game board represented as a 2D list.
        score_labels (list): Labels displaying the scores of players.
    """
    black_score = sum(row.count(BLACK) for row in board)
    white_score = sum(row.count(WHITE) for row in board)
    score_labels[0].config(text=f"Black: {black_score}")
    score_labels[1].config(text=f"White: {white_score}")

def check_winner(board, root):
    """
    Check the winner of the game and display a message box.

    Args:
        board (list): The game board represented as a 2D list.
        root: The root Tkinter window.
    """
    black_score = sum(row.count(BLACK) for row in board)
    white_score = sum(row.count(WHITE) for row in board)

    if black_score > white_score:
        messagebox.showinfo("Result", "You win!")
    elif black_score < white_score:
        messagebox.showinfo("Result", "You lose!")
    else:
        messagebox.showinfo("Result", "It's a draw!")
    root.destroy()

def place_initial_pieces(board):
    """
    Place initial pieces on the board.

    Args:
        board (list): The game board represented as a 2D list.
    """
    size = len(board)
    mid = size // 2
    board[mid-1][mid-1] = WHITE
    board[mid][mid] = WHITE
    board[mid-1][mid] = BLACK
    board[mid][mid-1] = BLACK

def center_window(window):
    """
    Function to center a tkinter window on the screen.

    Args:
        window: The tkinter window to be centered.
    """
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x_offset = (window.winfo_screenwidth() - width) // 2
    y_offset = (window.winfo_screenheight() - height) // 2
    window.geometry(f"+{x_offset}+{y_offset}")

# Initialize the game board and start the game
def start_game(size):
    """
    Initialize the game board and start the game.

    Args:
        size (int): The size of the game board.
    """
    root = tk.Tk()
    root.title("Othello")
    board = [[EMPTY] * size for _ in range(size)]
    place_initial_pieces(board)
    current_player = BLACK 
    canvas = tk.Canvas(root, width=400, height=400, bg="green")
    canvas.pack(side="left")
    draw_board(canvas, board)
    score_frame = tk.Frame(root)
    score_frame.pack(side="right", padx=10, pady=10)
    score_labels = [
        tk.Label(score_frame, text="Black: 2"),
        tk.Label(score_frame, text="White: 2")
    ]
    for label in score_labels:
        label.pack()
    canvas.bind("<Button-1>", lambda event: on_click(event, canvas, board, current_player, score_labels, root))
    button = tk.Button(score_frame, text="Change turn", command=lambda: change_turn(canvas, board, current_player,score_labels, root))
    button.pack(side="bottom", padx=10, pady=10)

    center_window(root)  # Center the game window on the screen
    root.mainloop()

if __name__ == "__main__":
    start_game(8)  # Start the game with an 8x8 board

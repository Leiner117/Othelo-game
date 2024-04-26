from time import sleep
import tkinter as tk

from othello import jugada_calculada

# Constantes
BOARD_SIZE = 8
EMPTY = 0
BLACK = 1
WHITE = 2

class OthelloGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Othello")

        # Inicializar el tablero
        self.board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.board[3][3] = WHITE
        self.board[3][4] = BLACK
        self.board[4][3] = BLACK
        self.board[4][4] = WHITE
        
        self.current_player = BLACK  # Comienza el jugador negro

        # Crear lienzo (canvas)
        self.canvas = tk.Canvas(self.master, width=400, height=400, bg="green")
        self.canvas.pack()

        # Dibujar el tablero inicial
        self.draw_board()

        # Manejar clics en el tablero
        self.canvas.bind("<Button-1>", self.on_click)

    def draw_board(self):
        self.canvas.delete("pieces")  # Eliminar todas las fichas existentes
        self.canvas.delete("invalid")  # Eliminar cualquier resaltado anterior de casillas no válidas

        cell_size = 400 // BOARD_SIZE

        # Dibujar las celdas del tablero
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x1 = col * cell_size
                y1 = row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="green", tags="board")

                # Dibujar las fichas según el estado del tablero
                if self.board[row][col] == BLACK:
                    self.canvas.create_oval(x1+2, y1+2, x2-2, y2-2, fill="black", tags="pieces")
                elif self.board[row][col] == WHITE:
                    self.canvas.create_oval(x1+2, y1+2, x2-2, y2-2, fill="white", tags="pieces")
        

        # Resaltar las casillas inválidas
        self.highlight_invalid_moves()
    def print_board(self):
        for row in self.board:
            print(row)
        print()
    def on_click(self, event):
       
        row = event.y // (400 // BOARD_SIZE)
        col = event.x // (400 // BOARD_SIZE)
        
        if self.current_player == BLACK:
            if self.is_valid_move(row, col):
                self.make_move(row, col, BLACK)
                self.current_player = WHITE
                self.draw_board()

                # Realizar la jugada para el jugador blanco si hay movimientos válidos disponibles
                
                plays = jugada_calculada(WHITE, self.board)
                valid_move = plays[0]#self.select_move(plays)
                self.make_move(valid_move[0], valid_move[1], WHITE)
                self.current_player = BLACK
                self.draw_board()
        self.print_board()

    def is_valid_move(self, row, col):
        if self.board[row][col] != EMPTY:
            return False
        
        player = self.current_player
        opponent = WHITE if player == BLACK else BLACK
        
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            cells_to_flip = []

            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == opponent:
                cells_to_flip.append((r, c))
                r += dr
                c += dc

            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == player and cells_to_flip:
                return True
        
        return False
    def select_move(self,calculated_plays):
        jugadas = []
        for i in calculated_plays:
            if self.is_valid_move(i[0], i[1]):
                return (i[0], i[1])

    def make_move(self, row, col, player):
        # Realizar la jugada para el jugador especificado
        self.board[row][col] = player

        # Voltear fichas del oponente según las direcciones
        player = self.current_player
        opponent = WHITE if player == BLACK else BLACK
        
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            cells_to_flip = []

            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == opponent:
                cells_to_flip.append((r, c))
                r += dr
                c += dc

            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == player and cells_to_flip:
                for flip_row, flip_col in cells_to_flip:
                    self.board[flip_row][flip_col] = player

    def highlight_invalid_moves(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if not self.is_valid_move(row, col):
                    cell_size = 400 // BOARD_SIZE
                    x1 = col * cell_size
                    y1 = row * cell_size
                    x2 = x1 + cell_size
                    y2 = y1 + cell_size
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="red", stipple="gray12", tags="invalid")

    def mainloop(self):
        self.master.mainloop()
    
def main():
    root = tk.Tk()
    gui = OthelloGUI(root)
    gui.mainloop()

if __name__ == "__main__":
    main()

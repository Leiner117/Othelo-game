import tkinter as tk
from tkinter import ttk
from othelloUI import start_game

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

def menu_screen():
    """
    Function to display the menu screen for selecting game options.
    """
    menu_window = tk.Tk()
    menu_window.title("Menu")

    board_size_var = tk.StringVar(value="4x4")  # Default value

    size_label = ttk.Label(menu_window, text="Board Size:")
    size_label.grid(row=0, column=0, padx=10, pady=5)

    board_size_combo = ttk.Combobox(menu_window, textvariable=board_size_var, 
                                    values=["4x4", "6x6", "8x8", "10x10"], state="readonly")
    board_size_combo.grid(row=0, column=1, padx=10, pady=5)

    def board_size():
        """
        Function to retrieve the selected board size.
        
        Returns:
            int: The selected board size.
        """
        size = board_size_var.get()
        if size == "4x4":
            return 4
        elif size == "6x6":
            return 6
        elif size == "8x8":
            return 8
        else: 
            return 10

    def on_play_click():
        """
        Callback function for the play button.
        Destroys the menu window and starts the game.
        """
        size = board_size()
        menu_window.destroy()  # Close the menu window
        start_game(size)

    play_button = ttk.Button(menu_window, text="Play", command=on_play_click)
    play_button.grid(row=1, columnspan=2, padx=10, pady=5)

    center_window(menu_window)  # Center the menu window on the screen
    menu_window.mainloop()

if __name__ == "__main__":
    menu_screen()

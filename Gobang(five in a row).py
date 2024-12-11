
from tkinter import *
import numpy as np

# Constants for the game setup
size_of_board = 600  # Size of the game board in pixels
grid_size = 15  # Number of grid cells per row/column
cell_size = size_of_board / grid_size  # Size of each cell in pixels
symbol_size = cell_size / 3  # Size of the symbols (X and O)
symbol_thickness = 2  # Thickness of the symbols
symbol_X_color = '#EE4035'  # Color for X symbol
symbol_O_color = '#0492CF'  # Color for O symbol
Green_color = '#7BC043'  # Color for highlighting

class Gobang:
    def __init__(self):
        self.reset_board = False  # Flag to indicate board reset
        self.window = Tk()  # Initialize main window
        self.window.title('Gobang (Five in a Row)')  # Title of the game window

        # Initialize board status with zeros
        self.board_status = np.zeros((grid_size, grid_size), dtype=int)
        self.cell_size = size_of_board / grid_size  # Cell size calculation

        # Initialize the starting page
        self.starting_page()
        self.move_history = []  # Stack to store the history of moves

    def mainloop(self):
        # Main loop to run the GUI
        self.window.mainloop()

    def starting_page(self):
        # Create and configure the starting page
        self.start_frame = Frame(self.window)
        self.start_frame.pack()
        self.start_frame.configure(bg="#F5F5F5")

        # Add title label
        title = Label(
            self.start_frame,
            text="Gobang (Five in a Row)",
            font=("Helvetica", 28, "bold italic"),
            fg="#333333",
            bg="#F5F5F5"
        )
        title.pack(pady=20)

        # Button to start the game
        btn_vs_human = Button(
            self.start_frame,
            text="Play now!",
            font=("Helvetica", 16),
            bg="#F0F0F0",
            relief="raised",
            command=self.start_human_game
        )
        btn_vs_human.pack(pady=10, anchor="center")

        # Button to exit the game
        btn_exit = Button(
            self.start_frame,
            text="Return to Desktop",
            font=("Helvetica", 16),
            bg="#F0F0F0",
            relief="raised",
            command=self.exit_game
        )
        btn_exit.pack(pady=10, anchor="center")

    def start_human_game(self):
        # Start the game for human players
        self.start_game()

    def start_game(self):
        # Initialize the game board and UI elements
        self.start_frame.destroy()  # Remove starting page frame
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()

        # Label to show the current player's turn
        self.turn_label = Label(
            self.window,
            text="Player X's Turn",
            font=("Helvetica", 16, "bold"),
            fg=symbol_X_color,
            bg="#F5F5F5"
        )
        self.turn_label.pack(pady=10)

        # Bind mouse click event
        self.window.bind('<Button-1>', self.click)

        # Initialize the board grid
        self.initialize_board()
        self.player_X_turns = True  # Flag to indicate X's turn
        self.board_status = np.zeros((grid_size, grid_size), dtype=int)  # Reset board status

        self.reset_board = False
        self.gameover = False

    def initialize_board(self):
        # Draw the grid lines on the canvas
        for i in range(grid_size):
            self.canvas.create_line(i * cell_size, 0, i * cell_size, size_of_board)
            self.canvas.create_line(0, i * cell_size, size_of_board, i * cell_size)

    def return_to_main_page(self):
        # Return to the main starting page
        self.canvas.destroy()
        self.turn_label.destroy()
        self.starting_page()

    def draw_O(self, logical_position):
        # Draw the O symbol at the given logical position
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(
            grid_position[0] - symbol_size, grid_position[1] - symbol_size,
            grid_position[0] + symbol_size, grid_position[1] + symbol_size,
            width=symbol_thickness, outline=symbol_O_color
        )

    def draw_X(self, logical_position):
        # Draw the X symbol at the given logical position
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(
            grid_position[0] - symbol_size, grid_position[1] - symbol_size,
            grid_position[0] + symbol_size, grid_position[1] + symbol_size,
            width=symbol_thickness, fill=symbol_X_color
        )
        self.canvas.create_line(
            grid_position[0] - symbol_size, grid_position[1] + symbol_size,
            grid_position[0] + symbol_size, grid_position[1] - symbol_size,
            width=symbol_thickness, fill=symbol_X_color
        )

    def convert_logical_to_grid_position(self, logical_position):
        # Convert logical position to pixel coordinates
        return (
            (logical_position[0] + 0.5) * cell_size,
            (logical_position[1] + 0.5) * cell_size
        )

    def convert_grid_to_logical_position(self, grid_position):
        # Convert pixel coordinates to logical position
        grid_position = np.array(grid_position)
        return np.array(grid_position // cell_size, dtype=int)

    def is_winner(self, player):
        # Check if the given player is the winner
        player_val = -1 if player == 'X' else 1

        for row in range(grid_size):
            for col in range(grid_size):
                if self.board_status[row][col] == player_val:
                    # Check horizontal, vertical, and diagonal lines
                    if col + 4 < grid_size and all(self.board_status[row][col:col + 5] == player_val):
                        return True
                    if row + 4 < grid_size and all(self.board_status[row:row + 5, col] == player_val):
                        return True
                    if row + 4 < grid_size and col + 4 < grid_size and all(
                            [self.board_status[row + i][col + i] == player_val for i in range(5)]):
                        return True
                    if row + 4 < grid_size and col - 4 >= 0 and all(
                            [self.board_status[row + i][col - i] == player_val for i in range(5)]):
                        return True
        return False

    def display_message(self, message):
        # Display error or informational messages
        self.turn_label.config(text=message, fg="red")
        self.window.after(2000, self.update_turn_label)

    def display_gameover(self, winner):
        # Display game over message and the winner
        self.gameover = True
        if self.turn_label.winfo_exists():  # Check if label exists
            self.turn_label.destroy()

        text = f'Winner: Player {1 if winner == "X" else 2} ({winner})'
        color = symbol_X_color if winner == 'X' else symbol_O_color

        self.canvas.delete("all")  # Clear the canvas
        font_size = int(size_of_board / 20)
        small_font_size = int(size_of_board / 30)

        winner_font = ("Helvetica", 24, "bold italic")
        return_font = ("Helvetica", 16)

        # Display winner text
        self.canvas.create_text(
            size_of_board / 2, size_of_board / 3,
            font=winner_font, fill=color, text=text
        )
        # Display return to main page message
        self.canvas.create_text(
            size_of_board / 2,
            size_of_board / 2,
            font=return_font,
            fill="gray",
            text="Click anywhere to return to main page"
        )

        self.canvas.bind("<Button-1>", lambda event: self.return_to_main_page())

    def update_turn_label(self):
        # Update the turn label to show the current player's turn
        if self.player_X_turns:
            self.turn_label.config(text="Player X's Turn", fg=symbol_X_color)
        else:
            self.turn_label.config(text="Player O's Turn", fg=symbol_O_color)

    def click(self, event):
        # Handle mouse click events for placing a move
        if self.reset_board:
            return

        if self.gameover:
            return

        grid_position = [event.x, event.y]
        try:
            logical_position = self.convert_grid_to_logical_position(grid_position)

            # Check if click is outside the grid or cell is occupied
            if (
                logical_position[0] < 0 or logical_position[0] >= grid_size or
                logical_position[1] < 0 or logical_position[1] >= grid_size
            ):
                raise ValueError("Click outside the grid!")

            if self.board_status[logical_position[0]][logical_position[1]] != 0:
                raise ValueError("Cell already occupied!")

            # Draw the move and check for winner
            if self.player_X_turns:
                self.draw_X(logical_position)
                self.board_status[logical_position[0]][logical_position[1]] = -1
                self.move_history.append((logical_position[0], logical_position[1], -1))
                if self.is_winner('X'):
                    self.gameover = True
                    self.display_gameover('X')
                    return
            else:
                self.draw_O(logical_position)
                self.board_status[logical_position[0]][logical_position[1]] = 1
                self.move_history.append((logical_position[0], logical_position[1], 1))
                if self.is_winner('O'):
                    self.gameover = True
                    self.display_gameover('O')
                    return

            # Switch turns
            self.player_X_turns = not self.player_X_turns
            self.update_turn_label()

        except ValueError as e:
            # Display error messages
            self.display_message(str(e))

    def exit_game(self):
        # Exit the game
        self.window.destroy()

# Create a game instance and run the main loop
game_instance = Gobang()
game_instance.mainloop()

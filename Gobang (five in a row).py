from tkinter import *
import numpy as np

# Constants
size_of_board = 600
grid_size = 15
cell_size = size_of_board / grid_size
symbol_size = cell_size / 3
symbol_thickness = 2
symbol_X_color = '#EE4035'
symbol_O_color = '#0492CF'
Green_color = '#7BC043'


class Gobang:
    def __init__(self):
        self.window = Tk()
        self.window.title('Gobang (Five in a Row)')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()

        # Input from user in the form of clicks
        self.window.bind('<Button-1>', self.click)

        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros((grid_size, grid_size), dtype=int)

        self.reset_board = False
        self.gameover = False

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        # Draw grid lines
        for i in range(grid_size):
            self.canvas.create_line(i * cell_size, 0, i * cell_size, size_of_board)
            self.canvas.create_line(0, i * cell_size, size_of_board, i * cell_size)

    def play_again(self):
        self.canvas.delete("all")
        self.initialize_board()
        self.board_status = np.zeros((grid_size, grid_size), dtype=int)
        self.player_X_turns = True
        self.reset_board = False
        self.gameover = False

    def draw_O(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(
            grid_position[0] - symbol_size, grid_position[1] - symbol_size,
            grid_position[0] + symbol_size, grid_position[1] + symbol_size,
            width=symbol_thickness, outline=symbol_O_color
        )

    def draw_X(self, logical_position):
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
        return (logical_position + 0.5) * cell_size

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)  # Convert list to NumPy array
        return np.array(grid_position // cell_size, dtype=int)


    def is_winner(self, player):
        player_val = -1 if player == 'X' else 1

        for row in range(grid_size):
            for col in range(grid_size):
                if self.board_status[row][col] == player_val:
                    # Check horizontally
                    if col + 4 < grid_size and all(self.board_status[row][col:col + 5] == player_val):
                        return True
                    # Check vertically
                    if row + 4 < grid_size and all(self.board_status[row:row + 5, col] == player_val):
                        return True
                    # Check diagonally (\ direction)
                    if row + 4 < grid_size and col + 4 < grid_size and all(
                            [self.board_status[row + i][col + i] == player_val for i in range(5)]):
                        return True
                    # Check anti-diagonally (/ direction)
                    if row + 4 < grid_size and col - 4 >= 0 and all(
                            [self.board_status[row + i][col - i] == player_val for i in range(5)]):
                        return True
        return False

    def display_gameover(self, winner):
        text = f'Winner: Player {1 if winner == "X" else 2} ({winner})'
        color = symbol_X_color if winner == 'X' else symbol_O_color

        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, size_of_board / 2, font="cmr 60 bold", fill=color, text=text)
        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4, font="cmr 20 bold", fill="gray",
                                text="Click to play again")
        self.reset_board = True

    def click(self, event):
        if self.reset_board:
            self.play_again()
            return

        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)

        if self.board_status[logical_position[0]][logical_position[1]] == 0:
            if self.player_X_turns:
                self.draw_X(logical_position)
                self.board_status[logical_position[0]][logical_position[1]] = -1
                if self.is_winner('X'):
                    self.gameover = True
                    self.display_gameover('X')
            else:
                self.draw_O(logical_position)
                self.board_status[logical_position[0]][logical_position[1]] = 1
                if self.is_winner('O'):
                    self.gameover = True
                    self.display_gameover('O')

            self.player_X_turns = not self.player_X_turns


game_instance = Gobang()
game_instance.mainloop()

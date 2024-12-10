import unittest
import numpy as np
from tkinter import TclError  # For handling GUI issues during testing
from gobang import Gobang



class TestGobang(unittest.TestCase):
    def setUp(self):
        self.game = Gobang()  # Initialize a new game instance

    def tearDown(self):
        try:
            self.game.window.destroy()  # Destroy the GUI after tests
        except TclError:
            pass

    def test_is_winner_horizontal(self):
        # Simulate a horizontal win for Player X
        for i in range(5):
            self.game.board_status[0][i] = -1
        self.assertTrue(self.game.is_winner('X'))

    def test_is_winner_vertical(self):
        # Simulate a vertical win for Player O
        for i in range(5):
            self.game.board_status[i][0] = 1
        self.assertTrue(self.game.is_winner('O'))

    def test_is_winner_diagonal(self):
        # Simulate a diagonal win for Player X
        for i in range(5):
            self.game.board_status[i][i] = -1
        self.assertTrue(self.game.is_winner('X'))

    def test_is_winner_reverse_diagonal(self):
        # Simulate a reverse diagonal win for Player O
        for i in range(5):
            self.game.board_status[i][4 - i] = 1
        self.assertTrue(self.game.is_winner('O'))

    def test_convert_logical_to_grid_position(self):
        logical_position = (0, 0)
        grid_position = self.game.convert_logical_to_grid_position(logical_position)
        self.assertEqual(grid_position, (self.game.cell_size / 2, self.game.cell_size / 2))

    def test_convert_grid_to_logical_position(self):
        grid_position = [self.game.cell_size / 2, self.game.cell_size / 2]
        logical_position = self.game.convert_grid_to_logical_position(grid_position)
        self.assertTrue(np.array_equal(logical_position, [0, 0]))

    def test_board_status_update(self):
        logical_position = (0, 0)
        self.game.board_status[logical_position[0]][logical_position[1]] = -1
        self.assertEqual(self.game.board_status[0][0], -1)

    def test_no_winner(self):
        # No winning condition
        self.game.board_status[0][0] = -1
        self.game.board_status[0][1] = 1
        self.assertFalse(self.game.is_winner('X'))
        self.assertFalse(self.game.is_winner('O'))

if __name__ == '__main__':
    unittest.main()

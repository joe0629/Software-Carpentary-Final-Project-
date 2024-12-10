# Software-Carpentry-Final-Project: Gobang Game (Five in a Row)

## Introduction
The **Gobang Game (Five in a Row)** is a two-player strategy game where players alternately place stones (X and O) on a 15x15 grid. The objective is to align five of their stones in a row—horizontally, vertically, or diagonally before their opponent. The first one to reach the objective wins. 

This project demonstrates fundamental software development practices, including the use of Tkinter for GUI design, logical game implementation, and unit testing with Python's `unittest`.

---

## Features
- **Interactive GUI**: Built using Python's Tkinter library, allowing two players to compete in real time.
- **Turn Indicators**: Clear visual cues for whose turn it is (Player X or Player O).
- **Winner Detection**: Automatically detects and announces the winner when a player aligns five stones.
- **Error Handling**: Displays error messages (e.g., "Cell already occupied!") for 3 seconds before resetting the turn indicator.
- **Unit Testing**: Comprehensive tests to ensure game logic functions correctly.

---

## How to Run the Game
### Prerequisites
- Python 3.7 or higher
- `numpy` library (install using `pip install numpy`, also included in the code. Only try installing when the code won't work)

### Running the Game
1. Clone or download this repository to your local machine.
2. Navigate to the project directory:
   ```bash
   cd [put you directory here]
3. Run the game
   ```bash
   python gobang.py

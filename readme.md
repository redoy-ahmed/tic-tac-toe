# Tic Tac Toe with PyQt5

![Tic Tac Toe](https://github.com/redoy-ahmed/tic-tac-toe/blob/main/1.png)

## Description

This is a simple Tic Tac Toe game implemented using PyQt5 for the GUI. The game allows you to play against a computer that uses a heuristic approach to determine its moves. The game includes a graphical interface with buttons for user interaction and features to restart or exit the game.

## Features

- **Single Player Mode**: Play against the computer.
- **Graphical Interface**: User-friendly interface built with PyQt5.
- **Heuristic AI**: The computer uses a heuristic approach to play intelligently.
- **Restart and Exit Options**: Easily restart the game or exit the application.

## Installation

### Prerequisites

- Python 3.x
- PyQt5

### Steps

1. Clone the repository:
    git clone https://github.com/redoy-ahmed/tic-tac-toe.git

2. Navigate to the project directory 
    cd tic-tac-toe-pyqt5

3. Install the required packages:
    pip install PyQt5

### Usages
1. Run the Tic-Tac-Toe-Manual.py file:
    python Tic-Tac-Toe-Manual.py

2. The game window will open. Click on the buttons to make your move.

### Code Structure
- 'Tic-Tac-Toe-Manual.py': The main script that contains the game logic and GUI implementation.

### Game Logic
- The game starts with an empty 3x3 grid.
- The player makes the first move by clicking on an empty cell, marking it with 'X'.
- The computer then makes its move by marking an empty cell with 'O'.
- The game checks for a winner or a draw after each move.
- The game can be restarted or exited using the provided buttons.

### Acknowledgements
- PyQt5 Documentation: PyQt5
- Inspiration from various online resources and tutorials.
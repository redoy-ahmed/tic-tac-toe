import sys
import random
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLabel, QStyle, QMessageBox
from PyQt5.QtCore import Qt, QPoint
from functools import partial


class TicTacToe(QtWidgets.QMainWindow):

    # region init
    def __init__(self):
        super().__init__()

        # Set the initial size and title of the main window
        self.setGeometry(450, 70, 700, 450)

        # Set the initial dragging state
        self.dragging = False
        self.dragStartPosition = QPoint()

        # Hide minimize, maximize, close buttons and make background transparent
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # Initialize UI elements
        self.initUI()
        self.show()

    def initUI(self):
        # Set up the main page widget and layout
        self.page = QtWidgets.QWidget()
        self.page.setStyleSheet("QWidget {background-color: #1f1f2f; border: 2px solid black; border-radius: 20px;}")
        self.vLayout = QtWidgets.QVBoxLayout()

        # Add game name label to the layout
        self.addGameNameLabel()
        self.vLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.page.setLayout(self.vLayout)
        self.setCentralWidget(self.page)

        # Create a grid layout for the tic-tac-toe buttons
        self.gLayout = QtWidgets.QGridLayout()
        self.vLayout.addLayout(self.gLayout)

        # Add bottom control buttons
        self.addBottomButtons()

        # Add tic-tac-toe buttons
        self.addButtons()

        # Initialize the game state
        self.initGameState()

    def initGameState(self):
        # Initialize the game state variables
        self.clickList = [''] * 9
        self.clickCounter = 0
        self.win = False

    # endregion

    # region draw game window components
    def addGameNameLabel(self):
        # Create and style the game name label
        appNameLabel = QLabel("Tic Tac Toe")
        appNameLabel.setStyleSheet("background-color: #ef927f; color: white; padding: 5px; font-size: 40px;")
        appNameLabel.setFixedSize(500, 70)
        appNameLabel.setAlignment(Qt.AlignCenter)
        self.vLayout.addSpacing(30)
        self.vLayout.addWidget(appNameLabel)
        self.vLayout.addSpacing(30)

    def addButtons(self):
        # Create and style the tic-tac-toe buttons
        self.buttons = []
        for index in range(9):
            btn = QtWidgets.QPushButton()
            btn.setMinimumSize(150, 150)
            btn.setStyleSheet(
                "QPushButton {background-color: #4b495f; border: 2px solid black; border-radius: 20px;}")
            self.gLayout.addWidget(btn, index // 3, index % 3)
            btn.clicked.connect(partial(self.userMove, btn, index))
            self.buttons.append(btn)

    def addBottomButtons(self):
        # Create and style the bottom control buttons
        self.vLayout.addSpacing(30)
        self.buttonLayout = QtWidgets.QHBoxLayout()

        # Add a restart button
        self.playAgainButton = self.createButton(QStyle.SP_DialogApplyButton, self.newGame)
        self.buttonLayout.addWidget(self.playAgainButton)

        # Add an exit button
        self.exitButton = self.createButton(QStyle.SP_DialogCancelButton, exitFunction)
        self.buttonLayout.addWidget(self.exitButton)

        self.vLayout.addLayout(self.buttonLayout)

    def createButton(self, style, func):
        # Helper method to create a styled button with an icon
        button = QtWidgets.QPushButton()
        icon = self.style().standardIcon(style)
        button.setIcon(icon)
        button.setIconSize(button.size() * 0.10)
        button.setFixedSize(90, 90)
        button.clicked.connect(func)
        button.setStyleSheet(
            "background-color: #ef927f; color: white; border: 2px solid black; border-radius: 20px; font-size: 20px;")
        return button

    # endregion

    # region game moves
    def userMove(self, btn, index):
        # Handle user move
        if self.clickList[index] == '':
            self.clickList[index] = 'X'
            btn.setText("X")
            btn.setStyleSheet("QWidget {background-color: #ef927f; color: #f5f5ff; font-size: 55px;}")
            btn.setEnabled(False)
            self.clickCounter += 1

            # Check game state after user's move
            if self.checkGameState('X'):
                return

            # If no win or draw, let the computer make a move
            if self.clickCounter < 9:
                self.computerMove()

    def computerMove(self):
        # Handle computer move
        index = self.bestMove()
        if index is not None:
            self.clickList[index] = 'O'
            btn = self.buttons[index]
            btn.setText("O")
            btn.setStyleSheet("QWidget {background-color: #dd7f9f; color: #f5f5ff; font-size: 55px;}")
            btn.setEnabled(False)
            self.clickCounter += 1

            # Check game state after computer's move
            self.checkGameState('O')

    def bestMove(self):
        # Determine the best move for the computer using a heuristic approach
        # Check if the computer can win in the next move
        for index in range(9):
            if self.clickList[index] == '':
                self.clickList[index] = 'O'
                if self.checkWinner('O'):
                    return index
                self.clickList[index] = ''

        # Check if the player can win in the next move and block them
        for index in range(9):
            if self.clickList[index] == '':
                self.clickList[index] = 'X'
                if self.checkWinner('X'):
                    self.clickList[index] = ''
                    return index
                self.clickList[index] = ''

        # Otherwise, choose a random empty spot
        empty_spots = [idx for idx in range(9) if self.clickList[idx] == '']
        return random.choice(empty_spots) if empty_spots else None

    # endregion

    # region game state check
    def checkGameState(self, player):
        # Check if the current player has won or if the game is a draw
        if self.clickCounter > 4 and self.checkWinner(player):
            self.gameOver(player)
            return True

        if self.clickCounter == 9 and not self.win:
            QMessageBox.information(self, "Draw!", "It is a draw")
            self.disableButtons()
            return True

        return False

    def checkWinner(self, player):
        # Check if the specified player has won
        winConditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]  # diagonals
        ]
        for condition in winConditions:
            if all(self.clickList[i] == player for i in condition):
                return True
        return False

    def gameOver(self, player):
        # Handle the end of the game and show the winner
        QMessageBox.information(self, "Winner!", f"Player {player} Won!!")
        self.disableButtons()
        self.win = True

    def enableButtons(self):
        # Enable all buttons
        for btn in self.buttons:
            btn.setEnabled(True)

    def disableButtons(self):
        # Disable all buttons
        for btn in self.buttons:
            btn.setEnabled(False)

    def newGame(self):
        # Restart the game
        self.initGameState()
        self.clearButtons()
        self.enableButtons()

    def clearButtons(self):
        # Clear the text and style of all buttons
        for btn in self.buttons:
            btn.setText("")
            btn.setStyleSheet(
                "QPushButton {background-color: #4b495f; border: 2px solid black; border-radius: 20px;}")

    # endregion

    # region draggable feature
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.dragStartPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.dragStartPosition)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()
    # endregion


def exitFunction():
    # Terminate the application
    QtWidgets.qApp.quit()


def mainFunction():
    # Create the application and set the style
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Windows')

    # Create and show the main window
    TicTacToe()
    sys.exit(app.exec_())


# Script entry point
if __name__ == '__main__':
    mainFunction()

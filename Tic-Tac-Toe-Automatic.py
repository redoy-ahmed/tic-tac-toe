import sys
import random
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLabel, QStyle
from functools import partial
from PyQt5.QtCore import Qt


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()

        # Set the initial size and title of the main window
        self.setGeometry(450, 200, 850, 750)

        # Hide minimize, maximize, close buttons and make background transparent
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.initUI()
        self.show()

    # Create a central widget for the main window
    def initUI(self):
        self.page = QtWidgets.QWidget()
        self.page.setStyleSheet("QWidget {background-color: #1f1f2f; border : 2px solid black; border-radius : 20px;}")
        self.vLayout = QtWidgets.QVBoxLayout()

        # Create a QLabel for App Name with background color and add it to the layout
        self.addGameNameLabel()

        self.vLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.page.setLayout(self.vLayout)
        self.setCentralWidget(self.page)

        # Create a grid layout for the tic-tac-toe buttons
        self.gLayout = QtWidgets.QGridLayout()
        self.vLayout.addLayout(self.gLayout)

        # Add a horizontal layout for "Restart" and "Exit" buttons
        self.addBottomButtons()

        # Add buttons for the tic-tac-toe grid
        self.addButtons()

        # Initialize the game state
        self.initList()

    # Create a QLabel for App Name with background color and add it to the layout
    def addGameNameLabel(self):
        appNameLabel = QLabel("Tic Tac Toe")
        appNameLabel.setStyleSheet("background-color: #ef927f; color: white; padding: 5px; font-size: 40px;")
        appNameLabel.setFixedWidth(500)
        appNameLabel.setFixedHeight(70)
        appNameLabel.setAlignment(Qt.AlignCenter)
        self.vLayout.addSpacing(30)
        self.vLayout.addWidget(appNameLabel)
        self.vLayout.addSpacing(30)

    # Counter for button indices
    def addButtons(self):
        self.buttonIndex = 0
        for row in range(3):
            for col in range(3):
                btn = QtWidgets.QPushButton()
                btn.setMinimumSize(150, 150)
                btn.setStyleSheet(
                    "QPushButton {background-color: #4b495f; border : 2px solid black; border-radius : 20px;}")
                self.gLayout.addWidget(btn, row, col)

                # Connect each button to the buttonClicked method with its index
                btn.clicked.connect(partial(self.userMove, btn, self.buttonIndex))
                self.buttonIndex += 1

    # Add two bottom buttons
    def addBottomButtons(self):
        pixAPI = getattr(QStyle, 'SP_DialogApplyButton')

        self.vLayout.addSpacing(30)
        self.buttonLayout = QtWidgets.QHBoxLayout()

        # Add a "Restart" button to restart the game
        self.playAgainButton = QtWidgets.QPushButton()
        icon = self.style().standardIcon(pixAPI)
        self.playAgainButton.setIcon(icon)
        self.playAgainButton.setIconSize(self.playAgainButton.size() * 0.10)
        self.playAgainButton.setFixedSize(90, 90)
        self.playAgainButton.clicked.connect(self.newGame)
        # setting border and radius = half of height
        self.playAgainButton.setStyleSheet(
            "background-color: #ef927f; color: white; border : 2px solid black; border-radius : 20px; font-size: 20px;")
        self.buttonLayout.addWidget(self.playAgainButton)

        pixAPI = getattr(QStyle, 'SP_DialogCancelButton')

        # Add an "Exit" button to close the game
        self.exitButton = QtWidgets.QPushButton()
        icon = self.style().standardIcon(pixAPI)
        self.exitButton.setIcon(icon)
        self.exitButton.setIconSize(self.exitButton.size() * 0.10)
        self.exitButton.setFixedSize(90, 90)
        self.exitButton.clicked.connect(exitFunction)
        # setting border and radius = half of height
        self.exitButton.setStyleSheet(
            "background-color: #ef927f; color: white; border : 2px solid black; border-radius : 20px; font-size: 20px;")
        self.buttonLayout.addWidget(self.exitButton)

        self.vLayout.addLayout(self.buttonLayout)

    # Initialize the list to track the button states and the click counter
    def initList(self):
        self.clickList = [''] * 9
        self.clickCounter = 0
        self.win = False

    # Update button text and click_list based on the current player
    def userMove(self, btn, index):
        self.clickList[index] = "X"
        btn.setText("X")
        btn.setStyleSheet("QWidget {background-color: #ef927f; color: #f5f5ff; font-size: 55px;}")

        # Disable the clicked button
        btn.setEnabled(False)
        self.clickCounter += 1

        # Check for a winner if at least 5 moves have been made
        if self.clickCounter > 4:
            if self.checkWinner('X'):
                self.gameOver('X')

        # Check for a draw if all buttons are clicked and no winner
        if self.clickCounter == 9 and not self.win:
            QtWidgets.QMessageBox.information(self, "Draw!", "It is a draw")
            self.disableButtons()

        # AI's turn
        if not self.win and self.clickCounter < 9:
            self.computerMove()

    # AI makes a move
    def computerMove(self):
        index = self.bestMove()
        if index is not None:
            self.clickList[index] = 'O'
            btn = self.gLayout.itemAt(index).widget()
            btn.setText("O")
            btn.setStyleSheet("QWidget {background-color: #dd7f9f; color: #f5f5ff; font-size: 55px;}")

            # Disable the clicked button
            btn.setEnabled(False)
            self.clickCounter += 1

            # Check for a winner if at least 5 moves have been made
            if self.clickCounter > 4:
                if self.checkWinner('O'):
                    self.gameOver('O')

            # Check for a draw if all buttons are clicked and no winner
            if self.clickCounter == 9 and not self.win:
                QtWidgets.QMessageBox.information(self, "Draw!", "It is a draw")
                self.disableButtons()

    # Check all possible winning triplets
    def checkWinner(self, player):
        win_conditions = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ]
        for condition in win_conditions:
            if all(self.clickList[i] == player for i in condition):
                return True
        return False

    # Disable all buttons
    def disableButtons(self):
        for i in range(self.gLayout.count()):
            self.gLayout.itemAt(i).widget().setEnabled(False)

    # Restart the game
    def newGame(self):
        self.initList()
        self.clearButtons()
        self.enableButtons()

    # Clear the text and style of all buttons
    def clearButtons(self):
        for i in range(self.gLayout.count()):
            widget = self.gLayout.itemAt(i).widget()
            widget.setText("")
            widget.setStyleSheet(
                "QPushButton {background-color: #4b495f; border : 2px solid black; border-radius : 20px;}")

    # Enable all buttons
    def enableButtons(self):
        for i in range(self.gLayout.count()):
            self.gLayout.itemAt(i).widget().setEnabled(True)

    # Heuristic approach: If computer can win, win. If player can win, block.
    def bestMove(self):
        for index in range(9):
            if self.clickList[index] == '':
                self.clickList[index] = 'O'
                if self.checkWinner('O'):
                    return index
                self.clickList[index] = ''
        for index in range(9):
            if self.clickList[index] == '':
                self.clickList[index] = 'X'
                if self.checkWinner('X'):
                    self.clickList[index] = ''
                    return index
                self.clickList[index] = ''

        # Otherwise, choose a random empty spot
        empty_spots = [idx for idx in range(9) if self.clickList[idx] == '']
        if empty_spots:
            return random.choice(empty_spots)

        return None

    def gameOver(self, player):
        QtWidgets.QMessageBox.information(self, "Winner!", f"Player {player} Won!!")
        self.disableButtons()
        self.win = True


# Terminate the program
def exitFunction():
    exit(1)


# Create the application and set the style
def mainFunction():
    app = QtWidgets.QApplication(sys.argv)

    # Set the style of the application
    app.setStyle('Windows')

    # Create the main window
    Window()

    # Execute the application
    sys.exit(app.exec_())


if __name__ == '__main__':
    mainFunction()

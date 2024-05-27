import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLabel
from functools import partial
from PyQt5.QtCore import Qt

class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()

        # Set the initial size and title of the main window
        self.setGeometry(450, 200, 900, 800)
        
        # Hide minimize, maximize, and close buttons
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        
        self.initUI()
        self.show()

    def initUI(self):
        # Create a central widget for the main window
        self.page = QtWidgets.QWidget()
        self.page.setStyleSheet("QWidget {background-color: #1f1f2f; border : 2px solid black; border-radius : 20px;}")
        self.vLayout = QtWidgets.QVBoxLayout()

        # Create a QLabel with background color and add it to the layout
        appNameLabel = QLabel("Tic Tac Toe")
        appNameLabel.setStyleSheet("background-color: #ef927f; color: white; padding: 5px; font-size: 40px;")
        appNameLabel.setFixedWidth(500)
        appNameLabel.setFixedHeight(70)
        appNameLabel.setAlignment(Qt.AlignCenter)
        self.vLayout.addWidget(appNameLabel)
        self.vLayout.addSpacing(30)
        
        self.vLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.page.setLayout(self.vLayout)
        self.setCentralWidget(self.page)

        # Create a grid layout for the tic tac toe buttons
        self.gLayout = QtWidgets.QGridLayout()
        self.vLayout.addLayout(self.gLayout)

        # Add a horizontal layout for "Restart" and "Exit" buttons
        self.vLayout.addSpacing(30)
        self.buttonLayout = QtWidgets.QHBoxLayout()

        # Add a "Restart" button to restart the game
        self.playagainButton = QtWidgets.QPushButton("Restart")
        self.playagainButton.setFixedSize(200, 55)
        self.playagainButton.clicked.connect(self.newGame)
        # setting border and radius = half of height 
        self.playagainButton.setStyleSheet("background-color: #ef927f; color: white; border : 2px solid black; border-radius : 20px; font-size: 20px;")
        self.buttonLayout.addWidget(self.playagainButton)

        # Add a "Exit" button to close the game
        self.exitButton = QtWidgets.QPushButton("Exit")
        self.exitButton.setFixedSize(200, 55)
        self.exitButton.clicked.connect(self.exitFunction)
        # setting border and radius = half of height 
        self.exitButton.setStyleSheet("background-color: #ef927f; color: white; border : 2px solid black; border-radius : 20px; font-size: 20px;")
        self.buttonLayout.addWidget(self.exitButton)

        self.vLayout.addLayout(self.buttonLayout)

        # Add buttons for the tic tac toe grid
        self.addButtons()

        # Initialize the game state
        self.initList()

    def addButtons(self):
        self.buttonIndex = 0  # Counter for button indices
        for row in range(3):
            for col in range(3):
                btn = QtWidgets.QPushButton()
                btn.setMinimumSize(150, 150)
                btn.setStyleSheet("QPushButton {background-color: #4b495f; border : 2px solid black; border-radius : 20px;}")
                self.gLayout.addWidget(btn, row, col)

                # Connect each button to the buttonClicked method with its index
                btn.clicked.connect(partial(self.buttonClicked, btn, self.buttonIndex))
                self.buttonIndex += 1

    def initList(self):
        # Initialize the list to track the button states and the click counter
        self.click_list = list(range(9))
        self.click_counter = 0
        self.win = False

    def buttonClicked(self, btn, indx):
        # Update button text and click_list based on the current player
        if self.click_counter % 2 == 0:
            self.click_list[indx] = "X"
            btn.setText("X")
            btn.setStyleSheet("QWidget {background-color: #ef927f; color: #f5f5ff; font-size: 55px;}")
        else:
            self.click_list[indx] = "O"
            btn.setText("O")
            btn.setStyleSheet("QWidget {background-color: #dd7f9f; color: #f5f5ff; font-size: 55px;}")

        # Disable the clicked button
        btn.setEnabled(False)
        self.click_counter += 1

        # Check for a winner if at least 5 moves have been made
        if self.click_counter > 4:
            self.check()

        # Check for a draw if all buttons are clicked and no winner
        if self.click_counter == 9 and not self.win:
            QtWidgets.QMessageBox.information(self, "Draw!", "It is a draw")
            self.disable_btns()

    def check(self):
        # Check all possible winning triplets
        for triplet in [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                        (0, 3, 6), (1, 4, 7), (2, 5, 8),
                        (0, 4, 8), (2, 4, 6)]:
            self.tripletCheck(*triplet)

    def tripletCheck(self, i, j, k):
        # Check if the values in the triplet are the same
        if self.click_list[i] == self.click_list[j] == self.click_list[k]:
            self.tripletColor(i, j, k)
            QtWidgets.QMessageBox.information(self, "Winner!", f"Player {self.click_list[i]} Won!!")
            self.disable_btns()
            self.win = True

    def tripletColor(self, i, j, k):
        # Change the color of the winning triplet buttons
        for index in (i, j, k):
            self.gLayout.itemAt(index).widget().setStyleSheet("QPushButton {background-color: green; font-size: 25px; color: Blue}")

    def disable_btns(self):
        # Disable all buttons
        for i in range(self.gLayout.count()):
            self.gLayout.itemAt(i).widget().setEnabled(False)

    def newGame(self):
        # Restart the game
        self.initList()
        self.clearButtons()
        self.enableButtons()

    def clearButtons(self):
        # Clear the text and style of all buttons
        for i in range(self.gLayout.count()):
            widget = self.gLayout.itemAt(i).widget()
            widget.setText("")
            widget.setStyleSheet("QPushButton {background-color: #4b495f; border : 2px solid black; border-radius : 20px;}")

    # Enable all buttons
    def enableButtons(self):        
        for i in range(self.gLayout.count()):
            self.gLayout.itemAt(i).widget().setEnabled(True)

    # Terminate the program
    def exitFunction(self):
        exit(1)
    
def mainFunction():
    # Create the application and set the style
    app = QtWidgets.QApplication(sys.argv)
    
    # Set the style of the application
    app.setStyle('Windows')
    
     # Create the main window
    window = Window()

    # Execute the application
    sys.exit(app.exec_())

if __name__ == '__main__':
    mainFunction()

import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QHBoxLayout, QApplication
from PyQt5.QtGui import QFont, QPainter, QColor
from PyQt5.QtCore import Qt
from pynput.mouse import Listener, Button
import pyautogui as pag

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.selecting = False
        self.setMouseTracking(False)

        # Set the window properties
        self.setWindowTitle("Colour Picker")
        self.setGeometry(100, 100, 350, 75)  # x, y, width, height
        self.setStyleSheet("background-color: #121212;")
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        # Execute button
        self.button = QPushButton("Start")
        self.button.setStyleSheet("color: white; background-color: #366fc9; border: 2px solid white; border-radius: 5px")
        self.button.setFixedWidth(100)
        self.button.setFixedHeight(30)
        self.button.clicked.connect(self.execute)

        # Colour label
        self.label = QLabel("Hex colour:", self)
        self.label.setStyleSheet("color: white;")
        self.label.setFixedWidth(100)

        # Textbox to show hex colour
        self.textbox = QLineEdit()
        self.textbox.setReadOnly(True)
        self.textbox.setStyleSheet("color: white;")
        self.textbox.setFixedWidth(90)
        self.textbox.setFixedHeight(self.button.height())

        # Square icon to show actual colour
        self.colour_icon = QLineEdit()
        self.colour_icon.setReadOnly(True)
        self.colour_icon.setFixedWidth(self.button.height())
        self.colour_icon.setFixedHeight(self.button.height())

        # Set up layout
        layout = QHBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        layout.addWidget(self.textbox)
        layout.addWidget(self.colour_icon)
        self.setLayout(layout)


    def execute(self):
        if self.button.text() == "Start":
            colour = "#F2433D"
            text = "Stop"

            # Begin listening for mouse clicks elsewhere
            self.selecting = True
            self.listener = Listener(on_click=self.on_click)
            self.listener.start()

        elif self.button.text() == "Stop":
            colour = "#366FC9"
            text = "Start"

            # Stop listening for mouse clicks
            self.selecting = False
            self.listener.stop()

            # Reset elements
            self.textbox.setText("")
            self.colour_icon.setStyleSheet(f"background-color: #121212")

        # Change button style / behaviour
        self.button.setText(text)
        self.button.setStyleSheet(f"color: white; background-color: {colour}; border: 2px solid white; border-radius: 5px")


    def on_click(self, x, y, button, pressed):
        if self.selecting and pressed and button == Button.left:
            # screen = ImageGrab.grab()
            # rgb = screen.getpixel((x, y))
            rgb = pag.pixel(x, y)
            hex_colour = '#{:02x}{:02x}{:02x}'.format(*rgb)
            self.textbox.setText(hex_colour.upper())

            # Colour in the square beside the textbox to show colour
            self.colour_icon.setStyleSheet(f"background-color: {hex_colour}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Roboto", 14))

    # Create an instance of the window
    window = MainWindow()
    window.show()

    # Execute the application
    sys.exit(app.exec_())

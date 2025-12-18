import os
import sys
import re
import ctypes
from PySide6.QtWidgets import(
    QWidget, QPushButton, QLabel, QLineEdit, QHBoxLayout, QApplication
)
from PySide6.QtGui import QFont, QIcon, QPalette
from PySide6.QtCore import Qt
from pynput.mouse import Listener, Button
import pyautogui as pag

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.listening = False
        self.paused = False
        self.setMouseTracking(False)
        self.setWindowIcon(QIcon(f"{os.path.dirname(os.path.realpath(__file__))}/icon.ico"))

        # Set the window properties
        self.setWindowTitle("Colour Picker")
        screen = self.screen()
        resolution = screen.availableGeometry() # Screen resolution
        width, height = resolution.width(), resolution.height() # Screen res width and height
        self.setGeometry(int(0.05*width), int(0.1*height), int(0.2*width), int(0.07*height)) # x, y, width, height. Scale relative to screen
        
        # App written on screen with 96dpi and font size 14. Scale the font depending on dpi
        QApplication.setFont(QFont("Roboto", 12 * int(96 / screen.logicalDotsPerInch())))

        self.setStyleSheet("background-color: #FFFFFF")
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        # Colours
        self.start_colour = "#366FC9"
        self.stop_colour = "#F2433D"
        self.paused_colour = "#A2A2A2"

        # Start/Stop button
        self.exec_btn = QPushButton("Start")
        self.btn_style = f"color: white; background-color: {self.start_colour}; border: 1px solid black; border-radius: 3px"
        self.exec_btn.setStyleSheet(self.btn_style)
        self.exec_btn.setFixedWidth(int(0.05*width))
        self.exec_btn.setFixedHeight(int(0.03*height))
        self.exec_btn.clicked.connect(self.execute)

        # Pause button
        self.pause_btn = QPushButton("Pause")
        self.pause_btn.setStyleSheet(
            self.btn_style.replace(
                f"background-color: {self.start_colour}",
                "background-color: #A2A2A2"
            )
        )
        self.pause_btn.setFixedWidth(int(0.05*width))
        self.pause_btn.setFixedHeight(int(0.03*height))
        self.pause_btn.clicked.connect(self.pause_clicked)

        # Colour label
        self.label = QLabel("Hex colour:", self)
        self.label.setStyleSheet("color: black")
        self.label.setFixedWidth(int(0.05*width))
        self.label.setAlignment(Qt.AlignCenter)

        # Textbox to show hex colour
        self.textbox = QLabel()
        self.textbox.setStyleSheet("color: black; border: 2px solid black; border-radius: 3px")
        self.textbox.setFixedWidth(int(0.05*width))
        self.textbox.setFixedHeight(self.exec_btn.height())
        self.textbox.setAlignment(Qt.AlignCenter)

        # Square icon to show actual colour
        self.colour_icon = QLineEdit()
        self.colour_icon.setStyleSheet("background-color: #FFFFFF; border: 1px solid black")
        self.colour_icon.setReadOnly(True)
        self.colour_icon.setFixedWidth(self.exec_btn.height())
        self.colour_icon.setFixedHeight(self.exec_btn.height())

        # Set up layout
        layout = QHBoxLayout()
        layout.addWidget(self.exec_btn)
        layout.addWidget(self.pause_btn)
        layout.addWidget(self.label)
        layout.addWidget(self.textbox)
        layout.addWidget(self.colour_icon)
        self.setLayout(layout)


    def execute(self):
        if self.exec_btn.text() == "Start":
            bgcolour = self.stop_colour
            text = "Stop"

            # Begin listening for mouse clicks elsewhere
            self.listening = True
            self.listener = Listener(on_click=self.on_click)
            self.listener.start()

        elif self.exec_btn.text() == "Stop":
            bgcolour = self.start_colour
            text = "Start"

            # Stop listening for mouse clicks
            self.listening = False
            self.listener.stop()

            # Reset elements
            self.textbox.setText("")
            self.colour_icon.setStyleSheet(f"background-color: #FFFFFF; border: 1px solid black")

        # Change button style / behaviour
        self.exec_btn.setText(text)
        self.change_stylesheet_colour(self.exec_btn, bgcolour, "background")


    def pause_clicked(self, _):
        """ Toggle the paused attribute to hold the current colour value """
        self.paused = not self.paused
        
        if self.paused:
            self.pause_btn.setText("Unpause")
            exec_btn_colour = self.paused_colour
            label_font_colour = self.paused_colour
            textbox_font_colour = self.paused_colour
        else:
            self.pause_btn.setText("Pause")
            exec_btn_colour = self.start_colour if not self.listening else self.stop_colour
            label_font_colour = "black"
            textbox_font_colour = "black"
        
        self.change_stylesheet_colour(self.exec_btn, colour=exec_btn_colour, key="background")
        self.change_stylesheet_colour(self.label, colour=label_font_colour, key="")
        self.change_stylesheet_colour(self.textbox, colour=textbox_font_colour, key="")


    def on_click(self, x, y, button, pressed):
        # First check if clicked the pause button, don't update colour if so
        wx, wy = self.window().geometry().x(), self.window().geometry().y()
        px, py = wx + self.pause_btn.x(), wy + self.pause_btn.y()
        pw, ph = self.pause_btn.width(), self.pause_btn.height()
        in_pause_btn_x = px <= x <= px + pw
        in_pause_btn_y = py <= y <= py + ph
        if in_pause_btn_x and in_pause_btn_y:
            return

        left_click_pressed = pressed and button == Button.left
        if self.listening and left_click_pressed and not self.paused:
            rgb = pag.pixel(x, y)
            hex_colour = "#{:02x}{:02x}{:02x}".format(*rgb)
            self.textbox.setText(hex_colour.upper())

            # Colour in the square beside the textbox to show colour
            self.colour_icon.setStyleSheet(f"background-color: {hex_colour}; border: 1px solid black; border-radius: 2px")


    def change_stylesheet_colour(self, elem, colour, key):
        """ Change the background colour in the stylesheet of a QT element """
        if "background" in key:
            key = "background-color"
    
        ss = elem.styleSheet()
        elem.setStyleSheet(
            ss.replace(
                re.search(rf"{key}:\s?(#[A-Fa-f0-9]{{6}}|white|black)", ss).group(0),
                f"{key}: {colour}"
            )
        )


if __name__ == "__main__":
    # Set APP ID to be able to use proper icon for windows taskbar
    app_id = "com.colour.picker"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

    app = QApplication(sys.argv)
    app.setFont(QFont("Roboto", 14))

    # Create an instance of the window
    window = MainWindow()
    window.show()

    # Execute the application
    sys.exit(app.exec())

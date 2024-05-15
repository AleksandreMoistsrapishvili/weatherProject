import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel
from weather_UI import WeatherApp

app = QApplication(sys.argv)

class Window(QWidget):
    def __init__(self):
        super().__init__()


window = Window()
window.show()
sys.exit(app.exec())
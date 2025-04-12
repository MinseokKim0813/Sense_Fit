from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QApplication, QDesktopWidget
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
import sys

def show_new_profile_window():
    class NewProfileWindow(QWidget):
        def __init__(self):
            super().__init__()
            self.initUI()

        def initUI(self):
            self.setWindowTitle("Sense Fit")

            # Get screen size and calculate 80% of width and height
            screen = QDesktopWidget().screenGeometry()
            screen_width = screen.width()
            screen_height = screen.height()
            window_width = int(screen_width * 0.8)
            window_height = int(screen_height * 0.8)

            self.setGeometry(100, 100, window_width, window_height)
            self.setStyleSheet("background-color: #2e2e2e;")  # Dark grey background

            # Set font and color
            title_font = QFont('Arial', 32, QFont.Bold)
            input_font = QFont('Arial', 24)
            label_style = "color: white;"
            input_style = "background-color: #3c3c3c; color: white; padding: 10px; border: none; min-width: 200px; max-width: 200px;"

            # Page Title
            self.title_label = QLabel("Create New Profile")
            self.title_label.setFont(title_font)
            self.title_label.setStyleSheet("color: white;")
            self.title_label.setAlignment(Qt.AlignCenter)

            # Name Label and Input
            self.name_label = QLabel("Name")
            self.name_label.setFont(input_font)
            self.name_label.setStyleSheet(label_style)

            self.name_input = QLineEdit()
            self.name_input.setFont(input_font)
            self.name_input.setStyleSheet(input_style)

            # DPI Label and Input
            self.dpi_label = QLabel("Current DPI")
            self.dpi_label.setFont(input_font)
            self.dpi_label.setStyleSheet(label_style)

            self.dpi_input = QLineEdit()
            self.dpi_input.setFont(input_font)
            self.dpi_input.setStyleSheet(input_style)

            # Create Button
            self.create_button = QPushButton("Create")
            self.create_button.setFont(input_font)
            self.create_button.setStyleSheet("""
                QPushButton {
                    background-color: #5e5e5e;
                    color: white;
                    border-radius: 40px;
                    padding: 20px 40px;
                }
                QPushButton:hover {
                    background-color: #7e7e7e;
                }
            """)
            self.create_button.setFixedSize(QSize(200, 80))

            # Layout
            layout = QVBoxLayout()
            layout.setSpacing(40)
            layout.setAlignment(Qt.AlignCenter)

            layout.addWidget(self.title_label)
            layout.addSpacing(20)
            layout.addWidget(self.name_label)
            layout.addWidget(self.name_input)
            layout.addWidget(self.dpi_label)
            layout.addWidget(self.dpi_input)
            layout.addSpacing(10)
            layout.addWidget(self.create_button)

            self.setLayout(layout)
            self.show()

    app = QApplication(sys.argv)
    new_profile = NewProfileWindow()
    sys.exit(app.exec_())

show_new_profile_window()

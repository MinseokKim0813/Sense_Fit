import sys
sys.path.append("..")

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QApplication, QDesktopWidget
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMessageBox
from profile_main import ProfileWindow
from Backend.create_profile import profileHandler

# Create an instance of the profileHandler
profile_handler = profileHandler()

def show_new_profile_window():
    class NewProfileWindow(QWidget):
        def __init__(self):
            super().__init__()
            self.initUI()

        def create_profile(self):
            response = profile_handler.create_profile(self.name_input.text(), self.dpi_input.text())
            
            if 'error' in response:
                # Show error message in the error label instead of QMessageBox
                self.error_label.setText(response['error'])
                self.error_label.setVisible(True)
            else:
                self.profile_window = ProfileWindow()
                self.profile_window.show()
                self.close()


        def initUI(self):
            self.setWindowTitle("Sense Fit")

            screen = QDesktopWidget().screenGeometry()
            window_width = int(screen.width() * 0.4)
            window_height = int(screen.height() * 0.4)
            center_x = int((screen.width() - window_width) / 2)
            center_y = int((screen.height() - window_height) / 2)
            self.setGeometry(center_x, center_y, window_width, window_height)
            self.setStyleSheet("background-color: #2e2e2e;")

            title_font = QFont('Arial', 32, QFont.Bold)
            input_font = QFont('Arial', 24)
            error_font = QFont('Arial', 16)
            label_style = "color: white;"
            input_style = """
                background-color: #3c3c3c;
                color: white;
                padding: 10px;
                border: none;
                min-width: 200px;
                max-width: 200px;
            """

            # Title
            self.title_label = QLabel("Create New Profile")
            self.title_label.setFont(title_font)
            self.title_label.setStyleSheet("color: white;")
            self.title_label.setAlignment(Qt.AlignCenter)

            # Error label (initially hidden)
            self.error_label = QLabel("")
            self.error_label.setFont(error_font)
            self.error_label.setStyleSheet("color: #ff6b6b;")  # Red color for error
            self.error_label.setAlignment(Qt.AlignCenter)
            self.error_label.setVisible(False)
            self.error_label.setWordWrap(True)

            # Name row
            self.name_label = QLabel("Name")
            self.name_label.setFont(input_font)
            self.name_label.setStyleSheet(label_style)
            self.name_input = QLineEdit()
            self.name_input.setFont(input_font)
            self.name_input.setStyleSheet(input_style)
            name_layout = QHBoxLayout()
            name_layout.setAlignment(Qt.AlignCenter)
            name_layout.addWidget(self.name_label)
            name_layout.addSpacing(20)
            name_layout.addWidget(self.name_input)

            # DPI row
            self.dpi_label = QLabel("Current DPI")
            self.dpi_label.setFont(input_font)
            self.dpi_label.setStyleSheet(label_style)
            self.dpi_input = QLineEdit()
            self.dpi_input.setFont(input_font)
            self.dpi_input.setStyleSheet(input_style)
            dpi_layout = QHBoxLayout()
            dpi_layout.setAlignment(Qt.AlignCenter)
            dpi_layout.addWidget(self.dpi_label)
            dpi_layout.addSpacing(20)
            dpi_layout.addWidget(self.dpi_input)

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
            self.create_button.clicked.connect(self.create_profile)
            self.create_button.clicked.connect(self.open_profile_window)

            # Connect input changes to hide error when user types
            self.name_input.textChanged.connect(self.hide_error)
            self.dpi_input.textChanged.connect(self.hide_error)

            # Layout
            layout = QVBoxLayout()
            layout.setSpacing(40)
            layout.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.title_label)
            layout.addWidget(self.error_label)
            layout.addLayout(name_layout)
            layout.addLayout(dpi_layout)

            button_layout = QHBoxLayout()
            button_layout.setAlignment(Qt.AlignCenter)
            button_layout.addWidget(self.create_button)

            layout.addLayout(button_layout)


            self.setLayout(layout)
            self.show()
            
        def hide_error(self):
            # Hide the error when user starts typing
            self.error_label.setVisible(False)

        def open_profile_window(self):
            # Only open if there are no errors (error label is hidden)
            if not self.error_label.isVisible():
                # Optional: you can extract the input data here if needed
                name = self.name_input.text()
                dpi = self.dpi_input.text()
                self.profile_window = ProfileWindow()  # You can pass `name` and `dpi` if needed
                self.profile_window.show()
                self.close()

    return NewProfileWindow()

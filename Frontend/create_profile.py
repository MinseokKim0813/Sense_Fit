import sys
sys.path.append("..")

from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QDesktopWidget
)
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMessageBox
from profile_main import ProfileWindow
from Backend.create_profile import profileHandler

# Create an instance of the profileHandler
profile_handler = profileHandler()

class CreateProfileDialog(QDialog):
    profile_created = pyqtSignal(str, str)  # name, dpi

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SenseFit")

        screen = QDesktopWidget().screenGeometry()
        window_width = int(screen.width() * 0.4)
        window_height = int(screen.height() * 0.4)
        center_x = int((screen.width() - window_width) / 2)
        center_y = int((screen.height() - window_height) / 2)
        self.setGeometry(center_x, center_y, window_width, window_height)
        self.setStyleSheet("background-color: #2e2e2e;")

        title_font = QFont('Arial', 32, QFont.Bold)
        input_font = QFont('Arial', 24)
        label_style = "color: white;"
        input_style = """
            background-color: #3c3c3c;
            color: white;
            padding: 10px;
            border: none;
            min-width: 200px;
            max-width: 200px;
        """

        self.title_label = QLabel("Create New Profile")
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("color: white;")
        self.title_label.setAlignment(Qt.AlignCenter)

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
        self.create_button.clicked.connect(self.on_create_clicked)

        layout = QVBoxLayout()
        layout.setSpacing(40)
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)
        layout.addLayout(name_layout)
        layout.addLayout(dpi_layout)
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(self.create_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def on_create_clicked(self):
        name = self.name_input.text().strip()
        dpi = self.dpi_input.text().strip()
        if name and dpi:
            self.profile_created.emit(name, dpi)
            self.accept()

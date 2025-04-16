from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import os

class ErrorPopup(QDialog):
    def __init__(self, message="Something went wrong. File was not uploaded."):
        super().__init__()
        self.setWindowTitle("Error")
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                border-radius: 20px;
            }
            QLabel#title {
                font-size: 28px;
                font-weight: bold;
                color: white;
            }
            QLabel#message {
                font-size: 16px;
                color: #cccccc;
            }
            QPushButton {
                font-size: 16px;
                padding: 8px 20px;
                border: 2px solid rgb(175, 28, 31);
                border-radius: 6px;
                color: white;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color:rgb(175, 28, 31);
            }
        """)
        self.setFixedSize(500, 220)
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        layout = QVBoxLayout()

        # Icon and "Ooops!" text
        top_layout = QHBoxLayout()
        icon_label = QLabel()
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(current_dir, "Images", "warning.png")
        icon_pixmap = QPixmap(icon_path)
        icon_pixmap = icon_pixmap.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(icon_pixmap)
        print("Looking for icon at:", icon_path)
        print("Exists:", os.path.exists(icon_path))

        title_label = QLabel("Ooops!")
        title_label.setObjectName("title")
        title_label.setFont(QFont("Arial", 24))
        top_layout.addWidget(icon_label)
        top_layout.addSpacing(12)
        top_layout.addWidget(title_label)
        top_layout.addStretch()

        # Message
        message_label = QLabel(message)
        message_label.setObjectName("message")
        message_label.setWordWrap(True)

        # Button
        button = QPushButton("OK")

        button.clicked.connect(self.accept)

        layout.addLayout(top_layout)
        layout.addSpacing(10)
        layout.addWidget(message_label)
        layout.addSpacing(20)
        layout.addWidget(button, alignment=Qt.AlignRight)

        self.setLayout(layout)

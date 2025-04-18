from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import os

class Popup(QDialog):
    def __init__(self, message="Default Message", title="Alert", button_message="OK"):
        super().__init__()
        self.setWindowTitle(title)
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
                padding-top: 10px;
                font-size: 18px;
                color: #cccccc;
            }
            QPushButton {
                font-size: 16px;
                padding: 8px 20px;
                border: 2px solid #cccccc;
                border-radius: 6px;
                color: white;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #cccccc;
            }
        """)
        # self.setFixedSize(500, 250)
        self.setMinimumWidth(500)
        self.setMinimumHeight(250)
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        layout = QVBoxLayout()

        # Icon and "Ooops!" text
        top_layout = QHBoxLayout()
        icon_label = QLabel()
        
        # current_dir = os.path.dirname(os.path.abspath(__file__))
        # icon_path = os.path.join(current_dir, "Images", "warning.png")
        # icon_pixmap = QPixmap(icon_path)
        # icon_pixmap = icon_pixmap.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # icon_label.setPixmap(icon_pixmap)

        title_label = QLabel(title)
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
        button = QPushButton(button_message)

        button.clicked.connect(self.accept)

        layout.addLayout(top_layout)
        layout.addSpacing(10)
        layout.addWidget(message_label)
        layout.addSpacing(20)
        layout.addWidget(button, alignment=Qt.AlignRight)

        self.setLayout(layout)

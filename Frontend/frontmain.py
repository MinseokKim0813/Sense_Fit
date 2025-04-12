import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QLabel, QHBoxLayout, QDesktopWidget
)
from PyQt5.QtCore import Qt

class MainInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SenseFit")

        # Get screen size and calculate 80% of width and height
        screen = QDesktopWidget().screenGeometry()
        screen_width = screen.width()
        screen_height = screen.height()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)

        self.setGeometry(100, 100, window_width, window_height)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout
        main_layout = QVBoxLayout()

        # Title label
        title_label = QLabel("Welcome to Sense_Fit")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        main_layout.addWidget(title_label)

        # Content layout
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)

        # Left panel (navigation)
        left_panel = QLabel("Left Panel")
        left_panel.setAlignment(Qt.AlignCenter)
        left_panel.setStyleSheet("background-color: #e0e0e0; min-width: 200px;")
        content_layout.addWidget(left_panel)

        # Right panel (main area)
        right_panel = QLabel("Main Display Area")
        right_panel.setAlignment(Qt.AlignCenter)
        right_panel.setStyleSheet("background-color: #f5f5f5;")
        content_layout.addWidget(right_panel)

        self.central_widget.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainInterface()
    window.show()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QLabel, QGridLayout, QScrollArea,
    QDesktopWidget, QPushButton, QFrame
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
        start_x = int(screen_width / 2 - window_width / 2)
        start_y = int(screen_height / 2 - window_height / 2)

        self.setGeometry(start_x, start_y, window_width, window_height)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Title Bar
        title_bar = QLabel("Select Profile")
        title_bar.setFixedHeight(60)
        title_bar.setAlignment(Qt.AlignCenter)
        title_bar.setStyleSheet("background-color: #2c3e50; color: white; font-size: 24px; font-weight: bold;")
        main_layout.addWidget(title_bar)

        # Scroll Area for Grid
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Container for Grid
        grid_container = QWidget()
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(20)
        self.grid_layout.setContentsMargins(40, 20, 40, 20)

        # Example: Add 8 placeholder profiles
        for i in range(8):
            profile_card = self.create_profile_card(f"Profile {i+1}")
            row = i // 4
            col = i % 4
            self.grid_layout.addWidget(profile_card, row, col)

        grid_container.setLayout(self.grid_layout)
        scroll_area.setWidget(grid_container)
        main_layout.addWidget(scroll_area)

        self.central_widget.setLayout(main_layout)

    def create_profile_card(self, title):
        card = QFrame()
        card.setFrameShape(QFrame.Box)
        card.setLineWidth(1)
        card.setStyleSheet("background-color: white; border-radius: 8px; padding: 10px;")

        layout = QVBoxLayout()
        label = QLabel(title)
        label.setAlignment(Qt.AlignCenter)
        button = QPushButton("Open")
        layout.addWidget(label)
        layout.addWidget(button)
        card.setLayout(layout)
        return card

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainInterface()
    window.show()
    sys.exit(app.exec_())

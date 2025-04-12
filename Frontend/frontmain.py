import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QLabel, QGridLayout, QScrollArea,
    QDesktopWidget, QPushButton, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal

from new_profile import show_new_profile_window


class AddProfileCard(QFrame):
    clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Box)
        self.setLineWidth(1)
        self.setFixedSize(200, 150)
        self.setStyleSheet("background-color: #ffffff; border-radius: 8px; padding: 10px;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        plus_label = QLabel("+")
        plus_label.setAlignment(Qt.AlignCenter)
        plus_label.setStyleSheet("font-size: 48px; color: #666666;")
        layout.addWidget(plus_label)

        text_label = QLabel("Create New Profile")
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setStyleSheet("font-size: 14px; color: #888888;")
        layout.addWidget(text_label)

        self.setLayout(layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()


class MainInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SenseFit")
        self.profiles = []  # Store profile names or objects

        # Centered window
        screen = QDesktopWidget().screenGeometry()
        w, h = int(screen.width() * 0.8), int(screen.height() * 0.8)
        self.setGeometry(
            int((screen.width() - w) / 2),
            int((screen.height() - h) / 2),
            w, h
        )

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layouts
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        title = QLabel("Select Profile")
        title.setFixedHeight(60)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("background-color: #2c3e50; color: white; font-size: 24px; font-weight: bold;")
        main_layout.addWidget(title)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        self.grid_container = QWidget()
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(20)
        self.grid_layout.setContentsMargins(40, 20, 40, 20)

        self.grid_container.setLayout(self.grid_layout)
        scroll_area.setWidget(self.grid_container)
        main_layout.addWidget(scroll_area)

        self.central_widget.setLayout(main_layout)

        self.add_card = AddProfileCard()
        self.add_card.clicked.connect(self.handle_add_profile)
        self.refresh_grid()

    def refresh_grid(self):
        # Clear current grid
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Re-add the "+" card to (0,0)
        self.grid_layout.addWidget(self.add_card, 0, 0)

        # Add all profile cards starting from (0,1) onward
        for index, title in enumerate(self.profiles):
            row = (index + 1) // 4
            col = (index + 1) % 4
            self.grid_layout.addWidget(self.create_profile_card(title), row, col)

    def handle_add_profile(self):
        self.new_profile_window = show_new_profile_window()


    def create_profile_card(self, title):
        card = QFrame()
        card.setFrameShape(QFrame.Box)
        card.setLineWidth(1)
        card.setFixedSize(200, 150)
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

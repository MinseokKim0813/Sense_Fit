import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QLabel, QGridLayout, QScrollArea,
    QDesktopWidget, QPushButton, QFrame, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from Frontend.create_profile import CreateProfileDialog
from Frontend.profile_main import ProfileWindow
from Backend.create_profile import profileHandler

# Create an instance of the profileHandler
profile_handler = profileHandler()

class ProfileCard(QFrame):
    clicked = pyqtSignal(str, str)  # name, dpi

    def __init__(self, profile_name, profile_dpi, width, height):
        super().__init__()
        self.profile_name = profile_name
        self.profile_dpi = profile_dpi

        self.setFixedSize(width, height)
        self.setFrameShape(QFrame.Box)
        self.setLineWidth(1)
        self.setStyleSheet("background-color: white; border-radius: 8px; padding: 10px;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        name_label = QLabel(profile_name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("font-size: 18px; font-weight: bold; color: black;")
        layout.addWidget(name_label)

        dpi_label = QLabel(f"DPI: {profile_dpi}")
        dpi_label.setAlignment(Qt.AlignCenter)
        dpi_label.setStyleSheet("font-size: 14px; color: #444444;")
        layout.addWidget(dpi_label)

        self.setLayout(layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print(self.profile_name, self.profile_dpi)
            self.clicked.emit(self.profile_name, str(self.profile_dpi))


class AddProfileCard(QFrame):
    clicked = pyqtSignal()

    def __init__(self, width, height):
        super().__init__()
        self.setFixedSize(width, height)
        self.setFrameShape(QFrame.Box)
        self.setLineWidth(1)
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
        self.profiles = profile_handler.get_profiles()
        # [{id: 1, name: "John", dpi: 100}, {id: 2, name: "Jane", dpi: 200}]

        # Center window
        screen = QDesktopWidget().screenGeometry()
        self.window_width = int(screen.width() * 0.8)
        self.window_height = int(screen.height() * 0.8)
        self.setGeometry(
            int((screen.width() - self.window_width) / 2),
            int((screen.height() - self.window_height) / 2),
            self.window_width,
            self.window_height
        )
        self.setStyleSheet("background-color: #1e1e1e; color: white;")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layouts
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Title
        title = QLabel("Select Profile")
        title.setFixedHeight(60)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("background-color: #2c3e50; color: white; font-size: 24px; font-weight: bold;")
        main_layout.addWidget(title)

        # Scrollable area for grid
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

        self.refresh_grid()

    def get_card_size(self):
        spacing = self.grid_layout.spacing() * 3
        margins = self.grid_layout.contentsMargins().left() + self.grid_layout.contentsMargins().right()
        usable_width = self.window_width - margins - spacing
        card_width = usable_width // 4
        card_height = int(card_width * 0.75)
        return card_width, card_height

    def refresh_grid(self):
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        card_width, card_height = self.get_card_size()
        total_items = len(self.profiles) + 1  # profiles + add card
        columns = 4

        for idx in range(total_items):
            row = idx // columns
            col = idx % columns

            if idx < len(self.profiles):
                profile_name = self.profiles[idx]['name']
                profile_dpi = self.profiles[idx]['DPI']
                card = self.create_profile_card(profile_name, profile_dpi, card_width, card_height)
            else:
                card = AddProfileCard(card_width, card_height)
                card.clicked.connect(self.handle_add_profile)

            self.grid_layout.addWidget(card, row, col)
        
        wrapper_layout = QVBoxLayout(self.grid_container)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.addLayout(self.grid_layout)
        wrapper_layout.addStretch()

        # Add invisible fillers to maintain grid shape (fill missing cells in the last row)
        remainder = total_items % columns
        if remainder != 0:
            for col in range(remainder, columns):
                filler = QWidget()
                filler.setFixedSize(card_width, card_height)
                filler.setStyleSheet("background-color: transparent;")
                self.grid_layout.addWidget(filler, total_items // columns, col)

    def handle_add_profile(self):
        dialog = CreateProfileDialog()
        dialog.profile_created.connect(self.switch_to_profile_page)
        dialog.exec_()  # block and wait for the dialog to close

    def switch_to_profile_page(self, name, dpi):
        self.setCentralWidget(ProfileWindow(name, dpi))

    def create_profile_card(self, profile_name, profile_dpi, width, height):
        card = ProfileCard(profile_name, profile_dpi, width, height)
        card.clicked.connect(self.switch_to_profile_page)
        return card

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainInterface()
    window.show()
    sys.exit(app.exec_())

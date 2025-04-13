import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QVBoxLayout, QHBoxLayout, QLabel, QDesktopWidget
)
from PyQt5.QtCore import Qt

from Backend.tracking_module import *

class ProfileWindow(QWidget):
    def __init__(self, name, dpi, main_window=None):
        super().__init__()
        self.main_interface = main_window
        self.profile_name = name
        self.dpi_value = dpi
        self.main_window = main_window
        self.initUI()


    def initUI(self):
        self.setWindowTitle(f"{self.profile_name}'s Profile")

        # Get screen size
        screen = QDesktopWidget().screenGeometry()
        screen_width = screen.width()
        screen_height = screen.height()

        # Set window size to 80% of screen
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        self.resize(window_width, window_height)
        self.move(
            int((screen_width - window_width) / 2),
            int((screen_height - window_height) / 2)
        )

        # Set modern dark background
        self.setStyleSheet("background-color: #1e1e1e; color: white;")

        # -------- UI Elements --------

        #Back Button
        back_button = QPushButton("← Back")
        back_button.clicked.connect(self.go_back)
        back_button.setFixedSize(120, 40)
        back_button.setStyleSheet("font-size: 18px; background-color: #2c2c2c; color: white;")
        back_button.clicked.connect(self.go_back)

        # Title label
        self.title_label = QLabel(f"{self.profile_name}'s Profile ({self.dpi_value} DPI)")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 30px; font-weight: bold;")

        # Button 1 + label
        self.label1 = QLabel("Distance Traveled")
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setStyleSheet("font-size: 20px; color: white;")

        self.button1 = QPushButton("Button 1")
        self.button1.setFixedSize(180, 40)
        self.button1.setStyleSheet("font-size: 14px; color: white; background-color: #2c2c2c;")

        box1 = QVBoxLayout()
        box1.setAlignment(Qt.AlignCenter)
        box1.addWidget(self.label1)
        box1.addSpacing(10)
        box1.addWidget(self.button1)

        # Button 2 + label
        self.label2 = QLabel("DPI Recommendation")
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setStyleSheet("font-size: 20px; color: white;")

        self.button2 = QPushButton("Button 2")
        self.button2.setFixedSize(180, 40)
        self.button2.setStyleSheet("font-size: 14px; color: white; background-color: #2c2c2c;")

        box2 = QVBoxLayout()
        box2.setAlignment(Qt.AlignCenter)
        box2.addWidget(self.label2)
        box2.addSpacing(10)
        box2.addWidget(self.button2)

        # Toggle status label
        self.tracking_status_label = QLabel("Tracking Disabled")
        self.tracking_status_label.setAlignment(Qt.AlignCenter)
        self.tracking_status_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        # Toggle label + button
        self.tracking_label = QLabel("Tracking")
        self.tracking_label.setAlignment(Qt.AlignCenter)
        self.tracking_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        self.toggle_button = QPushButton("Off")
        self.toggle_button.setCheckable(True)
        self.toggle_button.toggled.connect(self.on_toggle)
        self.toggle_button.setFixedSize(200, 50)
        self.toggle_button.setStyleSheet("font-size: 24px; font-weight: bold; background-color: #3a3a3a; color: white;")

        top_button_layout = QHBoxLayout()
        top_button_layout.addStretch()
        top_button_layout.addLayout(box1)
        top_button_layout.addSpacing(int(window_width * 0.3))
        top_button_layout.addLayout(box2)
        top_button_layout.addStretch()

        toggle_row_layout = QHBoxLayout()
        toggle_row_layout.addStretch()
        toggle_row_layout.addWidget(self.tracking_label)
        toggle_row_layout.addSpacing(10)
        toggle_row_layout.addWidget(self.toggle_button)
        toggle_row_layout.addStretch()

        toggle_layout = QVBoxLayout()
        toggle_layout.addWidget(self.tracking_status_label)
        toggle_layout.addSpacing(30)
        toggle_layout.addLayout(toggle_row_layout)

        main_layout = QVBoxLayout()
        main_layout.addSpacing(10)
        # Horizontal layout for back button with left spacing
        back_button_layout = QHBoxLayout()
        back_button_layout.addSpacing(20)  # ← Add left space (adjust value as needed)
        back_button_layout.addWidget(back_button)
        back_button_layout.addStretch()    # Optional: pushes button left while allowing spacing

        main_layout.addLayout(back_button_layout)

        main_layout.addWidget(self.title_label)
        main_layout.addSpacing(int(window_height * 0.1))
        main_layout.addLayout(top_button_layout)
        main_layout.addSpacing(int(window_height * 0.4))
        main_layout.addLayout(toggle_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)
    def go_back(self):
        self.main_interface.build_profile_grid()




    def on_toggle(self, checked):
        if checked:
            self.toggle_button.setText("On")
            self.toggle_button.setStyleSheet("font-size: 24px; font-weight: bold; background-color: #4caf50; color: white;")
            self.tracking_status_label.setText("Tracking Enabled")
            
            # Start tracking
            self.tracker = CursorTracker()
            # self.tracker.show()
        else:
            self.toggle_button.setText("Off")
            self.toggle_button.setStyleSheet("font-size: 24px; font-weight: bold; background-color: #3a3a3a; color: white;")
            self.tracking_status_label.setText("Tracking Disabled")

            # Stop tracking
            if hasattr(self, 'tracker') and self.tracker is not None:
                self.tracker.close()
                self.tracker.deleteLater()
                self.tracker = None

    def go_back(self):
        if self.main_window:
            self.main_window.show_profile_selection()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProfileWindow("Test User", "1200")
    window.show()
    sys.exit(app.exec_())

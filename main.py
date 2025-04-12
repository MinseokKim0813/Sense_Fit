import sys
import pyautogui
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

class CursorTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Global Cursor Tracker")
        self.resize(300, 100)

        # Display label
        self.label = QLabel("Cursor position will show here", self)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Timer to update cursor position every 100 ms
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_cursor_position)
        self.timer.start(100)

    def update_cursor_position(self):
        pos = pyautogui.position()
        self.label.setText(f"Global Cursor Position: x={pos.x}, y={pos.y}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tracker = CursorTracker()
    tracker.show()
    sys.exit(app.exec_())

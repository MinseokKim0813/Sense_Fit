import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My PyQt App")
        self.setGeometry(100, 100, 400, 300)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Example widgets
        self.label = QLabel("Hello, PyQt!")
        self.button = QPushButton("Click Me")

        layout.addWidget(self.label)
        layout.addWidget(self.button)

        # Connect button signal
        self.button.clicked.connect(self.on_button_click)

    def on_button_click(self):
        self.label.setText("Button clicked!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

import sys
import pyautogui  #For accessing the global mouse position
from PyQt5.QtCore import QTimer  #To create timed updates
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget  #Basic PyQt5 GUI elements

class CursorTracker(QWidget):
    def __init__(self):
        super().__init__()
        #Set up main window
        self.setWindowTitle("Global Cursor Tracker")                    #Window title
        self.resize(300, 100)                                           #Set window size

        # Create a label widget to display the cursor position
        self.label = QLabel("Cursor position will show here", self)

        #Set up the layout and add the label
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        #Set up a timer to repeatedly check and update the cursor position
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_cursor_position)         #On timeout, call update function
        self.timer.start(10)                                            #Trigger the timeout every 10 milliseconds (100Hz)

    def update_cursor_position(self):
        #Get the current global position of the mouse cursor
        pos = pyautogui.position()

        #Update the label text with the current x and y coordinates
        self.label.setText(f"Global Cursor Position: x={pos.x}, y={pos.y}")

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)                                        #Create the application
    tracker = CursorTracker()                                           #Create an instance of our tracker window
    tracker.show()                                                      #Show the window
    sys.exit(app.exec_())                                               #Run the application event loop

from Backend.tracking_module import CursorTracker

from PyQt5.QtWidgets import QApplication
import sys
import csv
import os
from datetime import datetime
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

        # Create logs directory if it doesn't exist
        os.makedirs("./logs", exist_ok=True)

        self.csv_file = f"./logs/cursor_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        self.init_csv()

        #Set up a timer to repeatedly check and update the cursor position
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_cursor_position)         #On timeout, call update function
        self.timer.start(10)                                            #Trigger the timeout every 10 milliseconds (100Hz)

    def init_csv(self):
        # Create the file and write header only if it doesn't exist
        try:
            with open(self.csv_file, "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "X", "Y"])
        except FileExistsError:
            pass  # File already exists, so do nothing

    def update_cursor_position(self):
        #Get the current global position of the mouse cursor
        pos = pyautogui.position()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        #Update the label text with the current x and y coordinates
        self.label.setText(f"Global Cursor Position: x={pos.x}, y={pos.y}")

        with open(self.csv_file, "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, pos.x, pos.y])

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)                                        #Create the application
    tracker = CursorTracker()                                           #Create an instance of our tracker window
    tracker.show()                                                      #Show the window
    sys.exit(app.exec_())                                               #Run the application event loop

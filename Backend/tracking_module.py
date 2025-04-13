import sys
import os
import csv
from datetime import datetime
import pyautogui  #For accessing the global mouse position
from PyQt5.QtCore import QTimer  #To create timed updates
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget  #Basic PyQt5 GUI elements

class CursorTracker(QWidget):
    def __init__(self, profile_id):
        super().__init__()
        self.__current_profile = profile_id
        # self.__cursor_data_points = []

        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.__current_session = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.__storage_dir = os.path.join(current_dir, "storage")
        self.__log_file = os.path.join(self.__storage_dir, f"cursor_log_{self.__current_session}.csv")

        self.__init_csv()

        #Set up main window
        self.setWindowTitle("Global Cursor Tracker")                    #Window title
        self.resize(300, 100)                                           #Set window size

        # Create a label widget to display the cursor position
        self.label = QLabel("Cursor position will show here", self)

        #Set up the layout and add the label
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Create the logs directory if it doesn't exist
        if not os.path.exists(self.__storage_dir):
            os.makedirs(self.__storage_dir)

        #Set up a timer to repeatedly check and update the cursor position
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_cursor_position)         #On timeout, call update function
        self.timer.start(10)                                            #Trigger the timeout every 10 milliseconds (100Hz)

    def __init_csv(self):
        # Create the file with the header
        try:
            with open(self.__log_file, "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Profile_ID", self.__current_profile, "Session", self.__current_session])
                writer.writerow(["Timestamp", "X", "Y"])
        except FileExistsError:
            pass  # File already exists, so do nothing

    def update_cursor_position(self):
        #Get the current global position of the mouse cursor
        pos = pyautogui.position()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        try:
        # TODO: Check pos is well defined; this means that pos is not None
            if pos is None:
                # TODO: Close this module and raise an error; the module must be closed
                raise ValueError("Encounted an error retriving the cursor position. Please try again.")
        except Exception as e:
            print(f"Error: {e}")
            self.close()
            return

        with open(self.__log_file, "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, pos.x, pos.y])
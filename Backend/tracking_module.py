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
        self.__storage_dir = os.path.join(current_dir, "storage", "logs")
        self.__log_file = os.path.join(self.__storage_dir, f"cursor_log_{self.__current_session}.csv")

        # Initialize CSV file and ensure storage directory exists
        try:
            self.__init_csv()
        except Exception as e:
            raise Exception(f"Failed to initialize tracking: {str(e)}")

        #Set up main window
        self.setWindowTitle("Global Cursor Tracker")                    #Window title
        self.resize(300, 100)                                           #Set window size

        # Create a label widget to display the cursor position
        # self.label = QLabel("Cursor position will show here", self)

        #Set up the layout and add the label
        layout = QVBoxLayout()
        # layout.addWidget(self.label)
        self.setLayout(layout)

        #Set up a timer to repeatedly check and update the cursor position
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_cursor_position)         #On timeout, call update function
        self.timer.start(10)                                            #Trigger the timeout every 10 milliseconds (100Hz)

    def __init_csv(self):
        # Create the logs directory if it doesn't exist
        try:
            if not os.path.exists(self.__storage_dir):
                os.makedirs(self.__storage_dir)

            # Create the file with the header
            with open(self.__log_file, "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Profile_ID", self.__current_profile, "Session", self.__current_session])
                writer.writerow(["Timestamp", "X", "Y"])
            return True
        except Exception as e:
            raise Exception(f"Error creating log file: {str(e)}")

    def update_cursor_position(self):
        try:
            #Get the current global position of the mouse cursor
            pos = pyautogui.position()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

            # Check if the position is valid
            if pos is None:
                raise ValueError("Failed to retrieve cursor position")
                
            # Write to the log file
            with open(self.__log_file, "a", newline='') as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, pos.x, pos.y])
                
        except Exception as e:
            print(f"Tracking error: {e}")
            # Close tracker on error
            self.close()
            return
    
    def close(self):
        # Ensure timer is stopped when closing
        if hasattr(self, 'timer') and self.timer is not None:
            self.timer.stop()
        super().close()
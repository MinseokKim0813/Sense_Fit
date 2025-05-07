import sys
import os
import csv
from datetime import datetime
import pyautogui  # For accessing the global mouse position
from PyQt5.QtCore import QTimer  # To create timed updates
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget  # Basic PyQt5 GUI elements
from pynput.mouse import Controller as MouseController, Listener as MouseListener, Button
from collections import namedtuple


class CursorTracker(QWidget):
    def __init__(self, profile_id):
        super().__init__()
        self.__current_profile = profile_id
        self.__error = None

        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.__current_session = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.__storage_dir = os.path.join(current_dir, "storage", "logs")
        self.__log_file = os.path.join(self.__storage_dir, f"id_{self.__current_profile}_cursor_log_{self.__current_session}.csv")

        self.clicked_flag = False  # For tracking mouse clicked
        self.mouse_listener = MouseListener(on_click=self.on_click) # Defining mouse_listener
        
        # Initialize CSV file and ensure storage directory exists
        try:
            self.__init_csv()
        except Exception as e:
            raise Exception(f"Failed to initialize tracking: {str(e)}")

        # Set up main window
        self.setWindowTitle("Global Cursor Tracker")                    # Window title
        self.resize(300, 100)                                           # Set window size

        # Set up the layout and add the label
        layout = QVBoxLayout()
        # layout.addWidget(self.label)
        self.setLayout(layout)

        #Set up a timer to repeatedly check and update the cursor position
        self.update_cursor_position()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_cursor_position)         # On timeout, call update function
        self.timer.start(10)                                            # Trigger the timeout every 10 milliseconds (100Hz)

        #Starts listening to mouse clicks
        self.mouse_listener.start()  

    def __init_csv(self):
        # Create the logs directory if it doesn't exist
        try:
            if not os.path.exists(self.__storage_dir):
                os.makedirs(self.__storage_dir)

            # Create the file with the header
            with open(self.__log_file, "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["timestamp", "X", "Y", "clicked"])
            return True
        except Exception as e:
            raise Exception(f"Error creating log file: {str(e)}")
        
    def on_click(self, x, y, button, pressed):
        if button == Button.left and pressed:
            self.clicked_flag = True  # Set flag true briefly

    def get_current_session(self):
        return self.__current_session

    def update_cursor_position(self):
        try:
            # Get the current global position of the mouse cursor
            pos = pyautogui.position()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

            # Stubbing test (uncomment one at a time)
            Point = namedtuple('Point', ['x', 'y'])
            # # case 1: position is null
            # pos = None
            # timestamp = None

            # # case 2: x position is null
            # pos = Point(None, pos.y)
            
            # # case 3: y position is null
            # pos = Point(pos.x, None)

            # # case 4: timestamp is null
            # timestamp = None

            # Check if the position is valid
            if pos is None and timestamp is None:
                raise ValueError("Memory Shortage Detected, tracking has been disabled. Clicking OK will start analysis with existing data.")
            
            if pos is None or pos.x is None or pos.y is None or timestamp is None:
                raise ValueError("Invalid data detected within the tracked data. Tracking has been disabled. Clicking OK will start analysis with existing data.")
            
            clicked = 1 if self.clicked_flag else 0
            self.clicked_flag = False   
            # Write to the log file
            with open(self.__log_file, "a", newline='') as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, pos.x, pos.y, clicked])
                
        except Exception as e:
            self.__error = str(e)
            self.close()
            return
    
    def close(self):
        # Ensure timer is stopped when closing
        if hasattr(self, 'timer') and self.timer is not None:
            self.timer.stop()
        super().close()

    def handle_error(self):
        if self.__error:
            return {"error": self.__error}
        else:
            return {}
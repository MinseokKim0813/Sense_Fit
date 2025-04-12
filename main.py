from Backend.tracking_module import CursorTracker

from PyQt5.QtWidgets import QApplication
import sys


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)                                        #Create the application
    tracker = CursorTracker()                                           #Create an instance of our tracker window
    tracker.show()                                                      #Show the window
    sys.exit(app.exec_())                                               #Run the application event loop

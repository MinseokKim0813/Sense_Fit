from Backend.tracking_module import CursorTracker
# from Frontend.frontmain import MainInterface

from PyQt5.QtWidgets import QApplication
import sys

from Frontend.frontmain import *
from Frontend.create_profile import *
from Frontend.profile_main import *


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainInterface()
    window.show()
    sys.exit(app.exec_())



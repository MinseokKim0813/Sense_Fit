import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QVBoxLayout, QHBoxLayout, QLabel, QDesktopWidget
)
from PyQt5.QtCore import Qt

from Backend.tracking_module import CursorTracker
from Backend.analyze_module import *

class ProfileWindow(QWidget):
    def __init__(self, profile, main_window=None):
        super().__init__()
        self.main_interface = main_window
        self.profile = profile
        self.main_window = main_window
        self.cursor_tracker = None
        self.analyze_module = None
        self.current_session = None
        self.initUI()


    def initUI(self):
        self.setWindowTitle(f"{self.profile['name']}'s Profile")

        # Get screen size
        screen = QDesktopWidget().screenGeometry()
        self.screen_width = screen.width()
        self.screen_height = screen.height()

        # Set window size to 80% of screen
        window_width = int(self.screen_width * 0.8)
        window_height = int(self.screen_height * 0.8)
        self.resize(window_width, window_height)
        self.move(
            int((self.screen_width - window_width) / 2),
            int((self.screen_height - window_height) / 2)
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
        self.title_label = QLabel(f"{self.profile['name']}'s Profile ({self.profile['DPI']} DPI)")
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
        
        # Add tracking status message label
        self.status_message_label = QLabel("")
        self.status_message_label.setAlignment(Qt.AlignCenter)
        self.status_message_label.setStyleSheet("font-size: 16px; color: #4caf50;") # Green color for success
        self.status_message_label.setVisible(False)
        
        # Add analysis error message label
        self.analysis_error_label = QLabel("")
        self.analysis_error_label.setAlignment(Qt.AlignCenter)
        self.analysis_error_label.setStyleSheet("font-size: 16px; color: #ff5252;") # Red color for errors
        self.analysis_error_label.setVisible(False)

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
        main_layout.addSpacing(int(window_height * 0.2))
        
        # Add tracking status label first
        main_layout.addWidget(self.tracking_status_label)
        
        # Add the toggle controls
        main_layout.addLayout(toggle_row_layout)
        
        # Add a fixed height container for status messages below the toggle button
        status_container = QVBoxLayout()
        status_container.addWidget(self.status_message_label)
        status_container.addWidget(self.analysis_error_label)
        
        # Create a container widget with fixed height to hold the status messages
        status_widget = QWidget()
        status_widget.setLayout(status_container)
        status_widget.setFixedHeight(int(window_height * 0.1))  # Fixed height for message area
        
        main_layout.addWidget(status_widget)
        
        # Add minimal spacing instead of a full stretch to reduce bottom padding
        main_layout.addSpacing(20)  # Small fixed spacing instead of stretch
        
        self.setLayout(main_layout)


    def go_back(self):
        self.main_interface.build_profile_grid()


    def on_toggle(self, checked):
        if checked:
            self.toggle_button.setText("On")
            self.toggle_button.setStyleSheet("font-size: 24px; font-weight: bold; background-color: #4caf50; color: white;")
            self.tracking_status_label.setText("Tracking Enabled")
            
            # Start tracking
            try:
                self.cursor_tracker = CursorTracker(self.profile['_id'])
                self.current_session = self.cursor_tracker.get_current_session()
                # Hide any previous message when starting tracking successfully
                self.status_message_label.setVisible(False)
                self.analysis_error_label.setVisible(False)
            except Exception as e:
                # Show error message
                self.status_message_label.setText(f"Failed to start tracking: {str(e)}")
                self.status_message_label.setStyleSheet("font-size: 16px; color: #ff5252;") # Red for error
                self.status_message_label.setVisible(True)
                # Revert toggle button to off state
                self.toggle_button.setChecked(False)
                return
        else:
            self.toggle_button.setText("Off")
            self.toggle_button.setStyleSheet("font-size: 24px; font-weight: bold; background-color: #3a3a3a; color: white;")
            self.tracking_status_label.setText("Tracking Disabled")

            # Stop tracking
            # TODO: Implement error handling; need to receive signal with error msg to the main window that the tracker has stopped
            if hasattr(self, 'cursor_tracker') and self.cursor_tracker is not None:
                try:
                    self.cursor_tracker.close()
                    self.cursor_tracker.deleteLater()
                    self.cursor_tracker = None
                    # Show success message
                    self.status_message_label.setText("Tracking stopped successfully")
                    self.status_message_label.setStyleSheet("font-size: 16px; color: #4caf50;") # Green for success
                    self.status_message_label.setVisible(True)

                except Exception as e:
                    # Show error message
                    self.status_message_label.setText(f"Failed to stop tracking: {str(e)}")
                    self.status_message_label.setStyleSheet("font-size: 16px; color: #ff5252;") # Red for error
                    self.status_message_label.setVisible(True)

                # Start analyzing
                self.analyze_module = AnalyzeModule(self.profile['_id'], self.current_session, self.screen_width, self.screen_height)

                # Check if data points are valid
                if ('error' in self.analyze_module.handle_error()):
                    # Display error message in the UI
                    error_message = self.analyze_module.handle_error()['error']
                    self.analysis_error_label.setText(f"Cursor movement analysis failed: {error_message}")
                    self.analysis_error_label.setVisible(True)
                else:
                    self.analyze_module.get_pause_segments()
                    # print(self.analyze_module.pause_points_list)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProfileWindow({"name": "Test User", "DPI": 1200})
    window.show()
    sys.exit(app.exec_())

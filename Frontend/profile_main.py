import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QVBoxLayout, QHBoxLayout, QLabel, QDesktopWidget, QGridLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt

from Backend.tracking_module import CursorTracker
from Backend.analyze_module import AnalyzeModule
from Backend.calculate_module import DPICalculationModule
from Frontend.error_window import *
from Frontend.alert_window import *
from Frontend.alert_window_one_button import *
from Backend.DPIgraph import DPIGraphEmbed
from Backend.DTgraph import DTGraphEmbed

class ProfileWindow(QWidget):
    def __init__(self, profile, main_window=None, profile_handler=None):
        super().__init__()
        self.main_interface = main_window
        self.profile = profile
        self.main_window = main_window
        self.cursor_tracker = None
        self.analyze_module = None
        self.current_session = None
        self.profile_handler = profile_handler
        self.initUI()



    def initUI(self):
        self.setWindowTitle(f"{self.profile['name']}'s Profile")

        # Get screen size
        screen = QDesktopWidget().screenGeometry()
        self.screen_width = screen.width()
        self.screen_height = screen.height()

        # Set window size to 80% of screen
        window_width = int(self.screen_width * 0.8)
        half_width = window_width // 2

        # Set modern dark background
        self.setStyleSheet("background-color: #1e1e1e; color: white;")

        # -------- UI Elements --------

        # Navigation
        back_button = QPushButton("\u2190 Back")
        back_button.clicked.connect(self.go_back)
        back_button.setFixedSize(120, 40)
        back_button.setStyleSheet("font-size: 18px; background-color: #2c2c2c; color: white;")

        self.title_label = QLabel(f"{self.profile['name']}'s Profile ({self.profile['DPI']} DPI)")
        self.title_label.setStyleSheet("font-size: 50px; font-weight: bold;")
    

        # Distance Traveled Section (Left)
        self.label1 = QLabel("Distance Traveled")
        self.label1.setStyleSheet("font-size: 30px; color: white;")
        self.label1.setAlignment(Qt.AlignHCenter)

        self.button1 = QPushButton("View Data")
        self.button1.setFixedSize(180, 40)
        self.button1.setStyleSheet("font-size: 14px; color: white; background-color: #2c2c2c;")
        self.button1.clicked.connect(self.toggle_dt_graph)

        self.dt_plot_widget = DTGraphEmbed(self.profile)
        self.dt_plot_widget.hide()
        self.dt_plot_widget.setFixedHeight(300)
        self.dt_plot_widget.setFixedWidth(half_width - 40)

        left_container = QWidget()
        left_container.setFixedWidth(half_width)
        self.left_layout = QVBoxLayout(left_container)
        self.left_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.addWidget(self.label1, alignment=Qt.AlignHCenter)
        self.left_layout.addWidget(self.button1, alignment=Qt.AlignHCenter)
        self.left_layout.addWidget(self.dt_plot_widget, alignment=Qt.AlignHCenter)
        self.left_layout.addStretch()

        # DPI Recommendation Section (Right)
        self.label2 = QLabel("DPI History")
        self.label2.setStyleSheet("font-size: 30px; color: white;")
        self.label2.setAlignment(Qt.AlignHCenter)

        self.button2 = QPushButton("View Data")
        self.button2.setFixedSize(180, 40)
        self.button2.setStyleSheet("font-size: 14px; color: white; background-color: #2c2c2c;")
        self.button2.clicked.connect(self.toggle_dpi_graph)

        self.dpi_plot_widget = DPIGraphEmbed(self.profile)
        self.dpi_plot_widget.hide()
        self.dpi_plot_widget.setFixedHeight(300)
        self.dpi_plot_widget.setFixedWidth(half_width - 40)

        right_container = QWidget()
        right_container.setFixedWidth(half_width)
        right_layout = QVBoxLayout(right_container)
        right_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addWidget(self.label2, alignment=Qt.AlignHCenter)
        right_layout.addWidget(self.button2, alignment=Qt.AlignHCenter)
        right_layout.addWidget(self.dpi_plot_widget, alignment=Qt.AlignHCenter)
        right_layout.addStretch()

        # Combine into a horizontal layout
        graphs_horizontal = QHBoxLayout()
        graphs_horizontal.setSpacing(0)
        graphs_horizontal.setContentsMargins(0, 0, 0, 0)
        graphs_horizontal.addWidget(left_container)
        graphs_horizontal.addWidget(right_container)

        # Wrap in a container with fixed height
        graphs_container = QWidget()
        graphs_container.setFixedHeight(450)
        graphs_container.setLayout(graphs_horizontal)

        # Tracking Toggle
        self.tracking_status_label = QLabel("Tracking Disabled")
        self.tracking_status_label.setAlignment(Qt.AlignCenter)
        self.tracking_status_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        self.tracking_label = QLabel("Tracking")
        self.tracking_label.setAlignment(Qt.AlignCenter)
        self.tracking_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        self.toggle_button = QPushButton("Off")
        self.toggle_button.setCheckable(True)
        self.toggle_button.toggled.connect(self.on_toggle)
        self.toggle_button.setFixedSize(200, 50)
        self.toggle_button.setStyleSheet("font-size: 24px; font-weight: bold; background-color: #3a3a3a; color: white;")

        self.status_message_label = QLabel("")
        self.status_message_label.setAlignment(Qt.AlignCenter)
        self.status_message_label.setStyleSheet("font-size: 16px; color: #4caf50;")
        self.status_message_label.setVisible(False)

        self.analysis_error_label = QLabel("")
        self.analysis_error_label.setAlignment(Qt.AlignCenter)
        self.analysis_error_label.setStyleSheet("font-size: 16px; color: #ff5252;")
        self.analysis_error_label.setVisible(False)

        # === LAYOUT COMPOSITION ===
        top_layout = QGridLayout()
        top_layout.addWidget(back_button, 0, 0, alignment=Qt.AlignLeft | Qt.AlignTop)
        top_layout.addWidget(self.title_label, 0, 0, 1, 3, alignment=Qt.AlignHCenter | Qt.AlignTop)

        toggle_row_layout = QHBoxLayout()
        toggle_row_layout.addStretch()
        toggle_row_layout.addWidget(self.tracking_label)
        toggle_row_layout.addSpacing(0)
        toggle_row_layout.addWidget(self.toggle_button)
        toggle_row_layout.addStretch()

        status_container = QVBoxLayout()
        status_container.addWidget(self.status_message_label)
        status_container.addWidget(self.analysis_error_label)
        status_widget = QWidget()
        status_widget.setLayout(status_container)
        status_widget.setFixedHeight(int(self.screen_height * 0.1))

        main_layout = QVBoxLayout()
        main_layout.addSpacing(10)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(graphs_container)
        main_layout.addWidget(self.tracking_status_label)
        main_layout.addLayout(toggle_row_layout)
        main_layout.addWidget(status_widget)
        main_layout.addSpacing(20)

        self.setLayout(main_layout)

    def toggle_dt_graph(self):
        if self.dt_plot_widget.isHidden():
            self.dt_plot_widget.show()
            self.dt_plot_widget.plot_dt_history()
        else:
            self.dt_plot_widget.hide()
    
    def toggle_dpi_graph(self):
        if self.dpi_plot_widget.isHidden():
            self.dpi_plot_widget.show()
            self.dpi_plot_widget.plot_dpi_history()
        else:
            self.dpi_plot_widget.hide()

    def go_back(self):
        try:
            if self.cursor_tracker is not None:
                error_popup = ErrorPopup("Please stop tracking before going back.")
                error_popup.exec_()
                return
        except Exception as e:
            error_popup = ErrorPopup(f"Unexpected error: {str(e)}")
            error_popup.exec_()
            return

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
                
                if 'error' in self.cursor_tracker.handle_error():
                    error_message = self.cursor_tracker.handle_error()['error']
                    error_popup = ErrorPopup(message=error_message)
                    error_popup.exec_()
                    self.toggle_button.setChecked(False)
                    self.toggle_button.setText("Off")
                    self.toggle_button.setStyleSheet("font-size: 24px; font-weight: bold; background-color: #3a3a3a; color: white;")
                    self.tracking_status_label.setText("Tracking Disabled")   
                    return

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

                    error_popup = ErrorPopup(message=error_message)
                    error_popup.exec_()
                else:
                    movement_data = self.analyze_module.analyze_tracking_data()

                    # Log the total distance of the tracking session
                    self.profile_handler.update_session_total_distance(self.profile['_id'], self.current_session, movement_data["total_distance"])

                    # Display window to ask if the user wants to proceed to calculation
                    alert_message = "We have analyzed your movement for the current session. Would you like us to recommend a DPI that fits better based on your movement?"
                    dpi_popup = Popup(alert_message, "Movement Analyzed", "Get DPI", "No")
                    dpi_popup.exec_()

                    # If user clicks "Get DPI", proceed to calculation
                    if dpi_popup.result() == QDialog.Accepted:
                        # TODO: Implement calculation
                        DPI_calculation_module = DPICalculationModule(self.profile, movement_data["analysis_result"])

                        if (DPI_calculation_module.dpi['out_of_bounds_flag'] == True):
                            # Display error message in the UI
                            error_message = f"Our calculated DPI is {DPI_calculation_module.dpi['DPI_recommendation']}. \nThis is outside the valid range: (100-3200).\nWe did not update your DPI. Please try again."

                            error_popup = ErrorPopup(message=error_message)
                            error_popup.exec_()

                            return

                        elif (DPI_calculation_module.dpi['large_diff_flag'] == True):
                            # Display window to ask if the user wants to proceed to calculation
                            alert_message = f"Our calculated DPI is {DPI_calculation_module.dpi['DPI_recommendation']}. \nKeep in mind that this is a large difference from your current DPI: {self.profile['DPI']}.\n"
                            large_diff_popup = Popup_OK_Only(alert_message, "Warning", "Large Difference", "OK")
                            large_diff_popup.exec_()

                        self.profile['DPI'] = DPI_calculation_module.dpi['DPI_recommendation']
                        self.profile_handler.update_dpi(self.profile['_id'], DPI_calculation_module.dpi['DPI_recommendation'])
                        # Update the title label with the new DPI
                        self.title_label.setText(f"{self.profile['name']}'s Profile ({self.profile['DPI']} DPI)")

                        # add the new dpi to self.profile for dpi history
                        updated_profile = self.profile_handler.refresh_profile(self.profile["_id"])
                        self.profile = updated_profile
                        self.dpi_plot_widget.profile = updated_profile
                        self.dpi_plot_widget.plot_dpi_history()
                        self.dt_plot_widget.profile = updated_profile
                        self.dt_plot_widget.plot_dt_history()

                    else:
                        self.status_message_label.setText("DPI not calculated")
                        self.status_message_label.setStyleSheet("font-size: 16px; color: #FCAE1E;") # Warm Orange for warning
                        self.status_message_label.setVisible(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProfileWindow({"name": "Test User", "DPI": 1200})
    window.show()
    sys.exit(app.exec_())

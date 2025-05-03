import pyqtgraph as pg
import json
import os
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QComboBox, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt

class DTGraphEmbed(QWidget):
    def __init__(self, profile: dict):
        super().__init__()
        self.profile = profile
        
        # Create main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.layout.setSpacing(0)  # Remove spacing between widgets
        
        # Create controls widget (dropdown)
        self.controls_widget = QWidget()
        self.controls_layout = QHBoxLayout(self.controls_widget)
        self.controls_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        
        # Add stretch first to push dropdown to the right
        self.controls_layout.addStretch()
        
        # Create dropdown for time frame options
        self.dropdown = QComboBox()
        self.dropdown.addItems(["24 hours", "1 week", "1 month"])
        self.dropdown.setCurrentIndex(0)  # Default to 24 hours view
        self.dropdown.currentIndexChanged.connect(self.update_time_frame)
        self.dropdown.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: black;
                padding: 5px;
                border: 1px solid #ccc;
                min-width: 150px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: black;
                selection-background-color: #0078d7;
                selection-color: white;
            }
        """)
        self.controls_layout.addWidget(self.dropdown)
        
        # Create graph
        self.graph_widget = pg.PlotWidget()
        self.graph_widget.setBackground('w')
        self.graph_widget.setLabel("left", "Distance Traveled")
        self.graph_widget.setLabel("bottom", "Date")
        
        # Disable auto-ranging to keep the view fixed
        self.graph_widget.setAutoVisible(y=False)
        
        # Lock the ViewBox to prevent x-axis scaling
        self.graph_widget.getViewBox().setMouseEnabled(x=False, y=False)
        
        # Add controls and graph to main layout
        self.layout.addWidget(self.controls_widget)
        self.layout.addWidget(self.graph_widget, 1)  # Give graph widget stretch factor of 1
        
        # Initialize with default visualization
        self.plot_dt_history()
        
    def update_time_frame(self):
        """Update the graph based on selected time frame"""
        self.plot_dt_history()
    
    def plot_dt_history(self):
        # Extract history
        data_points = []
        
        # Get current time frame
        time_frame = self.dropdown.currentText()
        current_date = datetime.now().date()
        current_datetime = datetime.now()
        
        # Determine the date range based on selected time frame
        if time_frame == "24 hours":
            # Last 24 hours - show data points with actual timestamps
            max_days_ago = 1
            # For 24-hour view, we need to consider the full datetime, not just the date
            time_threshold = current_datetime - timedelta(days=1)
        elif time_frame == "1 week":
            # Last 7 days
            max_days_ago = 7
        elif time_frame == "1 month":
            # Last 30 days
            max_days_ago = 30
        else:
            max_days_ago = 1  # Default to 1 day
        
        # Temporary storage for aggregating data by day
        daily_data = {}  # date -> total distance
            
        for entry in self.profile["session_total_distance"]:
            date_info = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
            
            if time_frame == "24 hours":
                # For 24-hour view, check if the timestamp is within the last 24 hours
                if date_info >= time_threshold:
                    # Store the full datetime object for 24-hour view
                    # Use hours as the x value for sorting
                    hours_ago = (current_datetime - date_info).total_seconds() / 3600.0
                    data_points.append((hours_ago, entry["total_distance"], date_info))
            else:
                # For week and month views, aggregate by day
                date_info_date = date_info.date()
                date_diff = (current_date - date_info_date).days
                
                # Only include data points within the selected time frame
                if date_diff <= max_days_ago:
                    # Aggregate data by day
                    if date_info_date in daily_data:
                        daily_data[date_info_date] += entry["total_distance"]
                    else:
                        daily_data[date_info_date] = entry["total_distance"]

        # For weekly and monthly views, convert the aggregated daily data to data points
        if time_frame != "24 hours":
            for date, total_distance in daily_data.items():
                date_diff = (current_date - date).days
                data_points.append((date_diff, total_distance, date))

        # Sort data by date/time (oldest entries first for consistent display)
        data_points.sort(key=lambda item: item[0], reverse=True)
        
        # Create new x and y
        x = []
        y = []
        x_map = {}  # Map to store date/time to x position mapping
        x_pos = 0
        
        for time_diff, distance, date_obj in data_points:
            x.append(x_pos)
            y.append(distance)
            x_map[x_pos] = date_obj
            x_pos += 1

        if (len(x) == 0 or len(y) == 0):
            # No data within selected time frame
            self.graph_widget.clear()
            return

        self.graph_widget.clear()
        
        # Always use bar graph as default visualization
        bargraph = pg.BarGraphItem(x=x, height=y, width=0.6, brush='b')
        self.graph_widget.addItem(bargraph)
        
        # Set Y-axis to start from 0 and extend to max value plus some padding
        self.graph_widget.setYRange(0, max(y) * 1.1, padding=0)
        
        # Set X-axis ticks with appropriate format based on time frame
        if len(x) > 0:
            tick_labels = {}
            
            if time_frame == "24 hours":
                # For 24-hour view, use 24-hour time format (14:30, 23:15)
                for x_val, datetime_obj in x_map.items():
                    # Compare date of data point to current date
                    if datetime_obj.date() == current_datetime.date():
                        time_label = datetime_obj.strftime("%H:%M")
                    else:
                        # Previous day but within 24 hours
                        time_label = f"-1D:{datetime_obj.strftime('%H:%M')}"
                    tick_labels[x_val] = time_label
            else:
                # For week/month views, use Month-Day format
                for x_val, date_obj in x_map.items():
                    month_day = date_obj.strftime("%b-%d")
                    tick_labels[x_val] = month_day
                    
            self.graph_widget.getAxis('bottom').setTicks([tick_labels.items()])

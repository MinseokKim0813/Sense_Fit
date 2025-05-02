import pyqtgraph as pg
import json
import os
from datetime import datetime
import numpy as np

class DTGraphEmbed(pg.PlotWidget):
    def __init__(self, profile: dict):
        super().__init__()
        self.setBackground('w')
        self.setVisible(False)  # start hidden
        self.setLabel("left", "Distance Traveled")
        self.setLabel("bottom", "Date")
        self.profile = profile
        
        # Disable auto-ranging to keep the view fixed
        self.setAutoVisible(y=False)
        
        # Lock the ViewBox to prevent x-axis scaling
        self.getViewBox().setMouseEnabled(x=False, y=False)

    def plot_dt_history(self):
        # Extract history
        x = []
        y = []

        for entry in self.profile["session_total_distance"]:
            date_info = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
            
            # Get only the date part without time
            date_info_date = date_info.date()
            current_date = datetime.now().date()
            
            # Calculate date difference in days
            date_diff = (current_date - date_info_date).days
            x.append(date_diff)
            y.append(entry["total_distance"])

        if (len(x) == 0 or len(y) == 0):
            return

        self.clear()
        
        # Create bar graph instead of line graph
        bargraph = pg.BarGraphItem(x=x, height=y, width=0.6, brush='b')
        self.addItem(bargraph)
        
        # Set Y-axis to start from 0 and extend to max value plus some padding
        self.getPlotItem().getViewBox().setYRange(0, max(y) * 1.1, padding=0)
        
        # Set X-axis ticks for better readability if you have enough data points
        if len(x) > 0:
            # Create tick labels (e.g., "1 day ago", "2 days ago", etc.)
            tick_labels = {}
            for day in x:
                if day == 0:
                    tick_labels[day] = "Today"
                elif day == 1:
                    tick_labels[day] = "1 day ago"
                else:
                    tick_labels[day] = f"{day} days ago"
                    
            self.getAxis('bottom').setTicks([tick_labels.items()])

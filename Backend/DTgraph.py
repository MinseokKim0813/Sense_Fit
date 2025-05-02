import pyqtgraph as pg
import json
import os
from datetime import datetime

class DTGraphEmbed(pg.PlotWidget):
    def __init__(self, profile: dict):
        super().__init__()
        self.setBackground('w')
        self.setVisible(False)  # start hidden
        self.setLabel("left", "Distance Traveled")
        self.setLabel("bottom", "Date")
        self.profile = profile

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
        self.plot(x, y, pen=pg.mkPen('blue', width=2), symbol='o')

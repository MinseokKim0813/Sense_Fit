import pyqtgraph as pg
import json
import os
from datetime import datetime


class DPIGraphEmbed(pg.PlotWidget):
    def __init__(self, profile: dict):
        super().__init__()
        self.setBackground('w')
        self.setVisible(False)  # start hidden
        self.profile = profile
        self.setLabel("left", "DPI")
        self.setLabel("bottom", "Time")

    def plot_dpi_history(self):

        # Extract history
        x = []
        y = []

        for entry in self.profile["DPI_history"]:
            date_info = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
            
            # Get only the date part without time
            date_info_date = date_info.date()
            current_date = datetime.now().date()
            
            # Calculate date difference in days
            date_diff = (current_date - date_info_date).days

            print(f"Date difference in days: {date_diff}")

            x.append(date_diff)
            y.append(entry["DPI"])

        if (len(x) == 0 or len(y) == 0):
            return

        # for entry in profile.get("DPI_history", []):
        #     if isinstance(entry, dict) and "DPI" in entry and "timestamp" in entry:
        #         try:
        #             date_info = datetime.strptime(entry["timestamp"], "%Y-%m-%d")
        #             print(date_info)
        #             x.append(date_info)
        #             y.append(entry["DPI"])
        #         except:
        #             continue

        # if not x or not y:
        #     return

        self.clear()
        self.plot(x, y, pen=pg.mkPen('blue', width=2), symbol='o')

import pyqtgraph as pg
import json
import os
from datetime import datetime
from statistics import mean

class DPIGraphEmbed(pg.PlotWidget):
    def __init__(self, profile: dict):
        super().__init__()
        self.setBackground('w')
        self.setLabel("left", "DPI")
        self.setLabel("bottom", "Date")
        self.profile = profile
        self.plot_dpi_history()

    def plot_dpi_history(self):
        # Extract history
        data_points = []
        
        # Get all entries and sort by date
        all_entries = []
        for entry in self.profile["DPI_history"]:
            date_info = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
            all_entries.append((date_info, entry["DPI"]))
        
        # Sort by date (oldest to newest)
        all_entries.sort(key=lambda x: x[0])
        
        if not all_entries:
            self.clear()
            return

        # If we have more than 5 entries, we need to average the older ones
        if len(all_entries) > 5:
            # Keep the 4 most recent entries as is
            data_points = all_entries[-4:]
            
            # Average the remaining older entries
            older_entries = all_entries[:-4]
            avg_dpi = mean(entry[1] for entry in older_entries)
            # Use the timestamp of the oldest entry in the averaged group
            oldest_date = older_entries[0][0]
            data_points.insert(0, (oldest_date, avg_dpi))
        else:
            data_points = all_entries

        # Create x and y arrays
        x = list(range(len(data_points)))  # Use simple indices for x-axis
        y = [point[1] for point in data_points]
        
        # Create date labels for x-axis
        tick_labels = {}
        for i, (date_obj, _) in enumerate(data_points):
            if i == 0 and len(all_entries) > 5:
                # For the first point (averaged older entries), show "Before"
                time_label = "Before"
            else:
                # For other points, show date and hour
                time_label = date_obj.strftime("%b-%d %H")
            tick_labels[i] = time_label

        self.clear()
        self.plot(x, y, pen=pg.mkPen('blue', width=2), symbol='o')
        
        # Set Y-axis to start from 0 and extend to max value plus some padding
        self.setYRange(0, max(y) * 1.1, padding=0)
        
        # Set X-axis ticks with date labels
        axis = self.getAxis('bottom')
        axis.setTicks([[(i, label) for i, label in tick_labels.items()]])
        
        # Ensure the last tick is visible by setting the range
        if x:
            self.setXRange(-0.5, len(x) - 0.5)

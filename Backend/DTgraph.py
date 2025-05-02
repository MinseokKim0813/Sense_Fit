import pyqtgraph as pg
import json
import os
from datetime import datetime

class DTGraphEmbed(pg.PlotWidget):
    def __init__(self, profile_id):
        super().__init__()
        self.profile_id = profile_id
        self.setBackground('w')
        self.setVisible(False)  # start hidden
        self.setLabel("left", "Distance Traveled")
        self.setLabel("bottom", "Date")
        self.plot_dt_history()

    def plot_dt_history(self):
        # Load profile
        file_path = os.path.join(os.path.dirname(__file__), "../Backend/storage/profiles.json")
        with open(file_path, "r") as f:
            profiles = json.load(f)

        profile = next((p for p in profiles if p["_id"] == self.profile_id), None)
        if not profile:
            return

        # Extract history
        x = []
        y = []
        for entry in profile.get("session_total_distance", []):
            if isinstance(entry, dict) and "total_distance" in entry and "timestamp" in entry:
                try:
                    dt = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
                    timestamp = dt.timestamp()  # convert to float (seconds since epoch)
                    x.append(timestamp)
                    y.append(entry["total_distance"])
                except Exception as e:
                    print("Error parsing entry:", entry, e)
                    continue

        if not x or not y:
            return

        self.clear()
        self.plot(x, y, pen=pg.mkPen('blue', width=2), symbol='o')

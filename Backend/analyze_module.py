import os
from datetime import datetime
import csv
import pandas as pd
import numpy as np

class AnalyzeModule:
    def __init__(self, profile_id: int, session: str):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.__storage_dir = os.path.join(current_dir, "storage", "logs")
        self.__log_file = os.path.join(self.__storage_dir, f"id_{profile_id}_cursor_log_{session}.csv")

        # if self.__log_file is not found, raise an error
        if not os.path.exists(self.__log_file):
            raise Exception(f"Tracking log file not found: {self.__log_file}")

        self.__cursor_log = []

        try:
            with open(self.__log_file, "r") as file:
                reader = csv.reader(file)

                for row in reader:
                    cursor_log = {}
                    cursor_log['timestamp'] = row[0]
                    cursor_log['x'] = row[1]
                    cursor_log['y'] = row[2]

                    self.__cursor_log.append(cursor_log)

            file.close()
        except Exception as e:
            # Here we need to catch error from missing connectivity to the storage (Test Case 9)
            raise Exception(f"Error reading tracking log file: {str(e)}")

    def analyze_tracking_data(self) -> dict:
        # TODO: Make algorithm to analyze the tracking data
        pass

    def validate_data_length(self):
        # TODO: Implement data validation mentioned in the test cases 10
        pass

    def validate_timestamps(self):
        # TODO: Implement data validation mentioned in the test cases 11
        pass

    def validate_cursor_positions(self):
        # TODO: Implement data validation mentioned in the test cases 12
        pass

    def get_pause_segments(self, threshold: int = 5):
        """
        Finds all pause segments where the cursor moved within a small threshold
        (X and Y changes are less than or equal to the threshold).

        Args:
            threshold (int): Maximum allowed pixel movement to consider as pause.

        Returns:
            list of dict: Each dict has 'start_index', 'end_index', 'x', 'y'.
        """
        df = pd.read_csv(self.__log_file)

        pause_segments = []
        start_idx = None

        for i in range(1, len(df)):
            dx = abs(df.loc[i, 'X'] - df.loc[i - 1, 'X'])
            dy = abs(df.loc[i, 'Y'] - df.loc[i - 1, 'Y'])
            within_threshold = dx <= threshold and dy <= threshold

            if within_threshold:
                if start_idx is None:
                    start_idx = i - 1
            else:
                if start_idx is not None:
                    pause_segments.append({
                        "start_index": int(start_idx),
                        "end_index": int(i - 1),
                        "x": int(df.loc[start_idx, 'X']),
                        "y": int(df.loc[start_idx, 'Y'])
                    })

                    start_idx = None

        # Handle final pause at end
        if start_idx is not None:
            pause_segments.append({
                "start_index": start_idx,
                "end_index": len(df) - 1,
                "x": int(df.loc[start_idx, 'X']),
                "y": int(df.loc[start_idx, 'Y'])
            })

        self.pause_points_list = pause_segments
        return pause_segments


# TODO: Do we need this?
# Parse timestamps and get the latest file
def extract_timestamp(file_path):
    # Example: id_2_cursor_log_2025-04-14_23-33-29.csv
    filename = os.path.basename(file_path)
    try:
        timestamp_str = filename.split("cursor_log_")[1].replace(".csv", "")
        return datetime.strptime(timestamp_str, "%Y-%m-%d_%H-%M-%S")
    except (IndexError, ValueError):
        return datetime.min  # fallback if format is off


# TODO: Should we keep this since the TrackingModule can handle this?
def retrieve_tracking_data(profile):
    profile_id = profile["_id"]
    log_dir = "Backend/storage/logs"
    matching_files = []

    # Get all the tracking file paths for the profile
    for filename in os.listdir(log_dir):
        if filename.startswith(f"id_{profile_id}") and filename.endswith(".csv"):
            file_path = os.path.join(log_dir, filename)
            matching_files.append(file_path)
    

    if matching_files:
        latest_file = max(matching_files, key=extract_timestamp)
    else:
        latest_file = None

    return latest_file

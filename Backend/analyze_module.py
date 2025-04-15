import os
from datetime import datetime
import csv
import math
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
                    cursor_log['clicked'] = row[3]

                    self.__cursor_log.append(cursor_log)

            file.close()

        except Exception as e:
            # Here we need to catch error from missing connectivity to the storage (Test Case 9)
            raise Exception(f"Error reading tracking log file: {str(e)}")

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

    # Returns a list of indices of the 'valid' clicked positions
    def find_clicked_positions(self) -> list[int]:
        clicked_positions = []

        for i in range(len(self.__cursor_log)):
            if self.__cursor_log[i]['clicked'] == '1':
                clicked_positions.append({**self.__cursor_log[i], 'index': i})
        
        # Remove clicks that are too close to each other (0.5 seconds) to count double clicks as one click
            time_before = datetime.strptime(clicked_positions[i - 1]['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
            time_now = datetime.strptime(clicked_positions[i]['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
            if ((time_now - time_before).total_seconds() <= 0.5):
                clicked_positions[i]['index'] = -1

        clicked_positions = [data_point['index'] for data_point in clicked_positions if data_point['index'] != -1]
        
        return clicked_positions

    def analyze_tracking_data(self) -> dict:
        analysis_result = {}

        # TODO: Make algorithm to analyze the tracking data
        clicked_positions = self.find_clicked_positions()

        return analysis_result

    def get_angle(self, dy: int, dx: int) -> float:
        return math.atan2(dy, dx) * (180 / math.pi)



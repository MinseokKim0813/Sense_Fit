import os
from datetime import datetime
import csv
import math
import pandas as pd
import numpy as np

class AnalyzeModule:
    def __init__(self, profile_id: int, session: str, screen_width: int, screen_height: int) -> None:
        self.screen_width = screen_width
        self.screen_height = screen_height

        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.__storage_dir = os.path.join(current_dir, "storage", "logs")
        self.__log_file = os.path.join(self.__storage_dir, f"id_{profile_id}_cursor_log_{session}.csv")
        self.__error = None

        # if self.__log_file is not found, raise an error (Test Case 9, in progress)
        if not os.path.exists(self.__log_file):
            raise Exception(f"Tracking log file not found: {self.__log_file}")

        self.__cursor_log = []

        try:
            with open(self.__log_file, "r") as file:
                reader = csv.reader(file)
                
                next(reader) # Skip the first row (header)

                for row in reader:
                    #print(row)
                    if len(row) != 4:
                        #print(row)
                        continue

                    cursor_log = {}
                    cursor_log['timestamp'] = row[0]
                    cursor_log['x'] = row[1]
                    cursor_log['y'] = row[2]
                    cursor_log['clicked'] = row[3]

                    self.__cursor_log.append(cursor_log)

            file.close()

            if (not self.validate_data_length()):
                raise Exception("Cursor tracking data is not sufficient. Please make sure the tracking persists for at least 1 second.")

            if (not self.validate_timestamps()):
                raise Exception("The timestamp of the tracking data is missing or invalid. Please try again.")

            if (not self.validate_cursor_positions()):
                raise Exception("The data points of the tracking data are missing, invalid, or out of range. Please try again.")
            
            if (not self.validate_extreme_movements()):
                raise Exception("Unusual cursor movement (No movement, Abrupt movement, Restless movement) detected. Please try again with natural movement behavior.")

        except Exception as e:
            print("Data points assertion failed for AnalyzeModule: ", e)
            self.__error = str(e)

    def validate_data_length(self) -> bool:
        # The tracking data must have at least 100 data points
        return len(self.__cursor_log) >= 100

    def validate_timestamps(self) -> bool:

        data_points = self.__cursor_log

        # Phase 1: Check if the timestamp is missing or invalid
        for i in range(len(data_points)):
            if (not data_points[i]['timestamp']):
                return False
            else:
                try:
                    datetime.strptime(data_points[i]['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
                except ValueError:
                    return False
        
        # Phase 2: Check if the timestamps are consistent
        for i in range(1, len(data_points)):
            timestamp_current = datetime.strptime(data_points[i]['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
            timestamp_before = datetime.strptime(data_points[i - 1]['timestamp'], "%Y-%m-%d %H:%M:%S.%f")

            if (timestamp_current < timestamp_before):
                return False
        return True

    def validate_cursor_positions(self) -> bool:
        data_points = self.__cursor_log

        # Check if the cursor position exists and is in integers
        try:
            for data_point in data_points:
                if (not data_point['x'] or not data_point['y']):
                    return False
                
                # If the data point is not an integer, the assertion fails (see exception)
                # Otherwise, the data point is type-casted to an integer
                data_point['x'] = int(data_point['x'])
                data_point['y'] = int(data_point['y'])

                # if the "clicked" entry is not valid, set it to 0
                if (data_point['clicked'] == '0' or data_point['clicked'] == '1'):
                    data_point['clicked'] = int(data_point['clicked'])
                else:
                    data_point['clicked'] = 0

                #Check if the cursor position is within the screen
                if (data_point['x'] < 0 or data_point['x'] >= self.screen_width or data_point['y'] < 0 or data_point['y'] >= self.screen_height):
                    return False

        except Exception as e:
            return False
        return True
    
    def validate_extreme_movements(self):
        data_points = self.__cursor_log

        cursor_moved_flag = False
        cursor_paused_flag = False

        for i in range(0,len(data_points)-1):
                x_pos1 = data_points[i]['x']
                y_pos1 = data_points[i]['y']
                x_pos2 = data_points[i+1]['x']
                y_pos2 = data_points[i+1]['y']

                distance_traveled = (x_pos2-x_pos1)**2 + (y_pos2-y_pos1)**2

                # for abrupt change in cursor position
                if(distance_traveled >= 250000):
                    return False

                # Check if the cursor positions have moved at all
                if (x_pos1 != x_pos2 or y_pos1 != y_pos2):
                    cursor_moved_flag = True

                # Check if the cursor ever paused
                if (x_pos1 == x_pos2 and y_pos1 == y_pos2):
                    cursor_paused_flag = True

        if not cursor_moved_flag:
            return False
        
        if not cursor_paused_flag:
            return False
        
        return True

    # Error handler to be used in the frontend
    def handle_error(self):
        if self.__error:
            return {"error": self.__error}
        else:
            return {"message": "Data points are valid!"}

    def get_pause_segments(self, threshold: int = 5) -> list[dict]:
        """
        Finds all pause segments where the cursor moved within a small threshold
        (X and Y changes are less than or equal to the threshold).

        Args:
            threshold (int): Maximum allowed pixel movement to consider as pause.

        Returns:
            list of dict: Each dict has 'start_index', 'end_index', 'x', 'y'.
        """
        data_points = self.__cursor_log

        pause_segments = []
        start_idx = None

        for i in range(1, len(data_points)):
            dx = abs(data_points[i]['x'] - data_points[i - 1]['x'])
            dy = abs(data_points[i]['y'] - data_points[i - 1]['y'])
            within_threshold = dx <= threshold and dy <= threshold

            if within_threshold:
                if start_idx is None:
                    start_idx = i - 1
            else:
                if start_idx is not None:

                    timestamp_end = datetime.strptime(data_points[i - 1]['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
                    timestamp_start = datetime.strptime(data_points[start_idx]['timestamp'], "%Y-%m-%d %H:%M:%S.%f")

                    if ((timestamp_end - timestamp_start).total_seconds() > 0.5):
                        pause_segments.append({
                            "start_index": start_idx,
                            "end_index": i - 1,
                            "x": int(data_points[start_idx]['x']),
                            "y": int(data_points[start_idx]['y'])
                        })

                    start_idx = None

        # Handle final pause at end
        if start_idx is not None:
            pause_segments.append({
                "start_index": start_idx,
                "end_index": len(data_points) - 1,
                "x": int(data_points[start_idx]['x']),
                "y": int(data_points[start_idx]['y'])
            })

        self.__pause_points_list = pause_segments
        return pause_segments

    # Returns a list of indices of the 'valid' clicked positions
    def find_end_points(self) -> list[int]:
        clicked_positions = []

        for i in range(len(self.__cursor_log)):
            if self.__cursor_log[i]['clicked'] == 1:
                clicked_positions.append({**self.__cursor_log[i], 'index': i})
        
        # TODO: Remove clicks that are too close to each other (0.5 seconds) to count double clicks as one click
            # time_before = datetime.strptime(clicked_positions[i - 1]['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
            # time_now = datetime.strptime(clicked_positions[i]['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
            # if ((time_now - time_before).total_seconds() <= 0.5):
            #     clicked_positions[i]['index'] = -1

        clicked_positions = [data_point['index'] for data_point in clicked_positions if data_point['index'] != -1]
        
        return clicked_positions
    
    def find_start_points(self, end_positions) -> list[int]:
        start_positions = []
        data_points = self.__cursor_log
        i = 0
        j = 25
        slope_before = None

        for end_position in end_positions:
            while (end_position > 0 and data_points[end_position]['x'] == data_points[end_position - 1]['x'] and data_points[end_position]['y'] == data_points[end_position - 1]['y']):
                end_position -= 1
            while end_position >= j:
                dx = data_points[end_position - j]['x'] - data_points[end_position - i]['x']
                dy = data_points[end_position - j]['y'] - data_points[end_position - i]['y']
                
                if self.is_paused(dx,dy):
                    i += 1
                    j += 1
                    continue

                slope_now = self.get_angle_from_delta(dx,dy)
                if slope_before is not None:
                    if self.angle_diff(slope_before, slope_now) > 30:
                        start_positions.append(data_points[end_position - i])
                        break
                    
                slope_before = slope_now
                i += 25
                j += 25
            i = 0
            j = 25
            slope_before = None

        return start_positions

    def analyze_tracking_data(self) -> dict:
        analysis_result = {}

        # TODO: Make algorithm to analyze the tracking data
        end_positions = self.find_end_points()
        start_positions = self.find_start_points(end_positions)
        print(start_positions)
        return analysis_result
    
    def get_angle_from_delta(self,dx, dy):
        angle = math.atan2(dy, dx) * (180 / math.pi)
        return angle
    
    def angle_diff(self, a1, a2):
        return min(abs(a1 - a2), 360 - abs(a1 - a2))
    
    def is_paused(self, dx, dy):
        return dx == 0 and dy == 0

if __name__ == "__main__":
    # Test AnalyzeModule here
    am = AnalyzeModule(1, "2025-04-17_00-56-53", 5000, 4000)
    #print(am.get_slope(-1,-5))

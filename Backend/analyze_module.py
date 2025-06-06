import os
from datetime import datetime
import csv
import math

class AnalyzeModule:
    def __init__(self, profile_id: int, session: str, screen_width: int, screen_height: int) -> None:
        self.screen_width = screen_width
        self.screen_height = screen_height

        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.__storage_dir = os.path.join(current_dir, "storage", "logs")
        self.__log_file = os.path.join(self.__storage_dir, f"id_{profile_id}_cursor_log_{session}.csv")
        self.total_distance = 0
        self.__error = None

        # If self.__log_file is not found, raise an error (Test Case 9)
        if not os.path.exists(self.__log_file):
            raise Exception(f"Tracking log file not found: {self.__log_file}")

        self.__cursor_log = []

        try:
            with open(self.__log_file, "r") as file:
                reader = csv.reader(file)
                
                next(reader) # Skip the first row (header)

                for row in reader:
                    if len(row) != 4:
                        continue

                    cursor_log = {}
                    cursor_log['timestamp'] = row[0]
                    cursor_log['x'] = row[1]
                    cursor_log['y'] = row[2]
                    cursor_log['clicked'] = row[3]

                    self.__cursor_log.append(cursor_log)

            file.close()

            if (not self.validate_data_length()):
                raise Exception("Cursor tracking data is not sufficient. Please make sure the tracking persists for at least 10 second.")

            if (not self.validate_timestamps()):
                raise Exception("The timestamp of the tracking data is missing or invalid. Please try again.")

            if (not self.validate_cursor_positions()):
                raise Exception("The data points of the tracking data are missing, invalid, or out of range. Please try again.")
            
            check_extreme_movements = self.validate_extreme_movements()
            if ("error" in check_extreme_movements):
                raise Exception(check_extreme_movements["error"] + " Please try again with natural movement behavior.")

        except Exception as e:
            self.__error = str(e)

    def validate_data_length(self) -> bool:
        # The tracking data must have at least 1000 data points
        return len(self.__cursor_log) >= 100 # Have 100 for testing purposes; TODO, change back to 1000

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
    
    def validate_extreme_movements(self) -> dict:
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
                    return {"error": "Unusual cursor movement (Abrupt movement) detected."}

                # Check if the cursor positions have moved at all
                if (x_pos1 != x_pos2 or y_pos1 != y_pos2):
                    cursor_moved_flag = True

                # Check if the cursor ever paused
                if (x_pos1 == x_pos2 and y_pos1 == y_pos2):
                    cursor_paused_flag = True

        if not cursor_moved_flag:
            return {"error": "Unusual cursor movement (No movement) detected."}
        
        if not cursor_paused_flag:
            return {"error": "Unusual cursor movement (Restless movement) detected."}
        
        return {"message": "Cursor movement is valid"}

    # Error handler to be used in the frontend
    def handle_error(self):
        if self.__error:
            return {"error": self.__error}
        else:
            return {"message": "Data points are valid!"}

    def get_pause_segments(self, threshold: int = 15) -> list[dict]:
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
            dx = data_points[i]['x'] - data_points[i - 1]['x']
            dy = data_points[i]['y'] - data_points[i - 1]['y']
            distance = math.sqrt(dx**2 + dy**2)
            within_threshold = distance <= threshold


            if within_threshold:
                if start_idx is None:
                    start_idx = i - 1
            else:
                if start_idx is not None:

                    timestamp_end = datetime.strptime(data_points[i - 1]['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
                    timestamp_start = datetime.strptime(data_points[start_idx]['timestamp'], "%Y-%m-%d %H:%M:%S.%f")

                    if ((timestamp_end - timestamp_start).total_seconds() > 0.1):
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
        
        for i in range(1, len(clicked_positions)):
            time_before = datetime.strptime(clicked_positions[i - 1]['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
            time_now = datetime.strptime(clicked_positions[i]['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
            if ((time_now - time_before).total_seconds() <= 0.4):
                clicked_positions[i]['index'] = -1

        clicked_positions = [data_point['index'] for data_point in clicked_positions if data_point['index'] != -1]
        
        return clicked_positions
    
    def analyze_all_segment(self, end_positions) -> list[dict]:
        all_segment = []                                    # Return list of objects "segment"
        data_points = self.__cursor_log                     # Call data points
        i = 0                                               # Pointer for the nearer cursor data
        j = 25                                              # Pointer for further cursor data
        slope_before = None                                 # To compare two slopes
        prev_click_point = 0                                # Make sure the start for an end point comes after the previous end point
        overshoot_flag = False                              # Detect overshoot existence
        self.get_pause_segments()                           # Updates __pause_point_list

        # Each click point will become the end_position of a trajectory segment for analysis
        for end_position in end_positions:
            segment = {"start_index": None, "end_index": None, "PD_list": [], "OS_distance": None, "TD": None}

            # Remove consecutive identical coordinates at the end of the segment (where the cursor was stationary)
            while (end_position > 0 and data_points[end_position]['x'] == data_points[end_position - 1]['x'] and data_points[end_position]['y'] == data_points[end_position - 1]['y']):
                end_position -= 1

            # Boundary check to prevent negative index
            while end_position >= j:
                # Boundary check to prevent duplicate starting points
                if prev_click_point < end_position - j:
                    dx = data_points[end_position - j]['x'] - data_points[end_position - i]['x']
                    dy = data_points[end_position - j]['y'] - data_points[end_position - i]['y']
                    
                    # Check for pause points, and disregard these points
                    if self.is_paused(dx,dy):
                        i += 1
                        j += 1
                        continue

                    slope_now = self.get_angle_from_delta(dx,dy)

                    if slope_before is not None:
                        # Check if the slope abruptly changes (meaning that the cursor is overshooting)
                        if not overshoot_flag:
                            if 130 <= self.angle_diff(slope_before, slope_now):
                                overshoot_flag = True
                                segment['OS_distance'] = (end_position - i) # temporily use index as distance
                                slope_before = slope_now
                                i += 25
                                j += 25
                                continue

                        # If the angle diff is more than 30 degrees, the system identifies the second latest cursor data point as the start point for the corresponding endpoint
                        if self.angle_diff(slope_before, slope_now) > 30:

                            segment['start_index'] = (end_position - i)         #add second latest cursor data index as the segment's start index
                            segment['end_index'] = end_position                 #add the current end point index to segment's end_index
                            break

                    # Update the slope before the next iteration
                    slope_before = slope_now
                    i += 25
                    j += 25

                # If goes beyond boundary save analyzed start_index and end_index for the segment
                else:
                    segment['start_index'] = (end_position - i)
                    segment['end_index'] = end_position
                    break
            
            # If index becomes negative, the start_index of the segment is 0
            if end_position < j:
                segment['start_index'] = 0
                segment['end_index'] = end_position

            # For counting pausepoints in one segment
            segment["PD_list"] = self.get_pause_distance(segment["start_index"], segment["end_index"], segment["OS_distance"])

            if segment['OS_distance'] is not None:
                segment['OS_distance'] = self.get_distance(segment["end_index"], segment['OS_distance'])

            segment['TD'] = self.get_distance(segment["start_index"], segment["end_index"])

            # Reset the variables for the next segment
            i = 0
            j = 25
            slope_before = None
            prev_click_point = end_position
            overshoot_flag = False
            all_segment.append(segment)

        return all_segment

    def analyze_tracking_data(self) -> dict:
        end_positions = self.find_end_points()
        all_segment = self.analyze_all_segment(end_positions)
        self.total_distance = self.get_total_distance()
        return {"analysis_result": all_segment, "total_distance": self.total_distance}
    
    def get_total_distance(self) -> float:
        TD = 0
        for i in range(1, len(self.__cursor_log)):
            TD += self.get_distance(i, i-1)
        return TD
    
    def get_angle_from_delta(self,dx, dy):
        angle = math.atan2(dy, dx) * (180 / math.pi)
        if (angle < 0):
            angle += 360
        return angle
    
    def angle_diff(self, a1, a2):
        diff = abs(a1 - a2)
        if diff > 180:
            diff = 360 - diff
        return diff
    
    def is_paused(self, dx, dy):
        distance = math.sqrt(dx**2 + dy**2)
        threshold = 15
        within_threshold = distance <= threshold
        return within_threshold
    
    def get_distance(self, index1, index2):
        x1 = self.__cursor_log[index1]["x"]
        x2 = self.__cursor_log[index2]["x"]
        y1 = self.__cursor_log[index1]["y"]
        y2 = self.__cursor_log[index2]["y"]

        return math.sqrt((x1-x2)**2 + (y1-y2)**2)
    
    def get_pause_distance(self, startpoint: int, endpoint: int, OS_index: int) -> list[int]:
        paused_points = self.__pause_points_list                          #updates __pause_point_list
        PDList = []
        
        paused_points_within_segment = [startpoint]
        for each in paused_points:
            if startpoint <= each["start_index"] and endpoint >= each["end_index"]:

                # Skip OS_index check if OS_index is None
                if OS_index is None or (not (each["start_index"] <= OS_index <= each["end_index"])
                    and not (each["start_index"] <= endpoint <= each["end_index"])):
                    paused_points_within_segment.append(each["start_index"])

        for i in range(1, len(paused_points_within_segment)):
            distance = self.get_distance(paused_points_within_segment[i-1], paused_points_within_segment[i])
            # Only add non-zero distances to avoid 0.0 in PDList
            if distance > 0:
                PDList.append(distance)

        return PDList


if __name__ == "__main__":
    # Test AnalyzeModule here
    pass

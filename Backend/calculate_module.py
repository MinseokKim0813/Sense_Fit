import os
import csv
class DPICalculationModule:
    def __init__(self, current_profile, current_session, movement_data):
        self.__current_profile = current_profile
        self.__movement_data = movement_data
        self.__error = None
        
        self.__tracking_data = []

        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.__log_file = os.path.join(current_dir, f"id_{current_profile['_id']}_cursor_log_{current_session}.csv")

        try:
            with open(self.__log_file, "r") as file:
                reader = csv.reader(file)
                next(reader) # Skip the first row (header)

                for row in reader:
                    if len(row) != 4:
                        continue

                    cursor_log = {}
                    cursor_log['timestamp'] = row[0]
                    cursor_log['x'] = int(row[1])
                    cursor_log['y'] = int(row[2])
                    cursor_log['clicked'] = row[3]

                    self.__tracking_data.append(cursor_log)
                    

        except Exception as e:
            self.__error = f"Failed to read tracking data: {str(e)}"
                
                
    def calculate_dpi(self) -> int:
        return 1500
            

import os
import csv
import math

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

        self.dpi = self.calculate_dpi()
                
    def calculate_dpi(self) -> int:
        suggestion = 0
        count = 0

        for seg in self.__movement_data:
            #when mix
            if len(seg["PD_list"]) != 0 and seg["OS_distance"] is not None:
                temp = self.calculate_mix(seg["PD_list"], seg["OS_distance"], seg["TD"])
                count += 1
            #when only over shoot exist
            elif len(seg["PD_list"]) == 0 and seg["OS_distance"] is not None:
                temp = self.calculate_OS(seg["OS_distance"], seg["TD"])
                count += 1
            #when only over paused exist
            elif len(seg["PD_list"]) != 0 and seg["OS_distance"] is None:
                temp = self.calculate_paused(seg["PD_list"], seg["TD"])
                count += 1
            else:
                continue
            suggestion += temp

        if (count == 0 or suggestion == 0):
            return self.__current_profile['DPI']
        else:
            sug = self.__current_profile['DPI'] * (suggestion/count)
            now = self.__current_profile['DPI']
            diff = (sug-now) * 0.6
            now += diff
            now = math.floor(now/10) * 10
            # print(diff, 'Sug:', sug, "now:", now)
            
            return now
    
    def calculate_paused(self, PDList : list[float], TD : float) -> float:
        avg_paused = 0

        for PD in PDList:
            avg_paused += PD

        avg_paused /= len(PDList)

        return TD/avg_paused
    
    # OS_distance is the distance between the click point and the overshoot occured point
    def calculate_OS(self, OS_distance: float, TD : float) -> float:
        return TD / (OS_distance + TD)
    
    def calculate_mix(self, PDList : list[float], OSD: float, TD : float):
        paused = self.calculate_paused(PDList, TD)
        OSed = self.calculate_OS(OSD, TD)
        return (paused + OSed)/2
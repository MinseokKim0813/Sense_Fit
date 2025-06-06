import os
import csv
import math

class DPICalculationModule:
    def __init__(self, current_profile, movement_data):
        self.__current_profile = current_profile
        self.__movement_data = movement_data
        self.__error = None
        self.dpi = self.calculate_dpi()
                
    def calculate_dpi(self) -> int:
        suggestion = 0
        count = 0

        for seg in self.__movement_data:
            # When both pause(s) and an overshoot exist
            if len(seg["PD_list"]) != 0 and seg["OS_distance"] is not None:
                temp = self.calculate_mix(seg["PD_list"], seg["OS_distance"], seg["TD"])
                count += 1
            # When only a overshoot exists
            elif len(seg["PD_list"]) == 0 and seg["OS_distance"] is not None:
                temp = self.calculate_OS(seg["OS_distance"], seg["TD"])
                count += 1
            # When only pause(s) exist
            elif len(seg["PD_list"]) != 0 and seg["OS_distance"] is None:
                temp = self.calculate_paused(seg["PD_list"], seg["TD"])
                count += 1
            else:
                continue
            suggestion += temp

        response = { "DPI_recommendation": None, "out_of_bounds_flag": False, "large_diff_flag": False }

        if (count == 0 or suggestion == 0):
            response["DPI_recommendation"] = self.__current_profile['DPI']
        else:
            sug = self.__current_profile['DPI'] * (suggestion/count)
            now = self.__current_profile['DPI']
            diff = (sug-now) * 0.6
            now += diff
            now = math.floor(now/10) * 10
            response["DPI_recommendation"] = now

            if abs(diff) > 400:
                response["large_diff_flag"] = True
            
            if not (100 <= now <= 3200):
                response["out_of_bounds_flag"] = True
            
        return response
    
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
    
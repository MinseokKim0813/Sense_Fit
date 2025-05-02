import os
import json
from datetime import datetime
def is_alphanumeric(char: str) -> bool:
    return (ord('a') <= ord(char) <= ord('z')) or (ord('A') <= ord(char) <= ord('Z')) or (ord('0') <= ord(char) <= ord('9'))


def get_current_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def format_timestamp(timestamp: str) -> str:
    return datetime.strptime(timestamp, "%Y-%m-%d_%H-%M-%S").strftime("%Y-%m-%d %H:%M:%S")


class ProfileHandler:
    def __init__(self):
        self.__profiles = []

        current_dir = os.path.dirname(os.path.realpath(__file__))

        self.__storage_dir = os.path.join(current_dir, "storage")
        self.__profiles_file = os.path.join(self.__storage_dir, "profiles.json")
        
        # Create storage directory if it doesn't exist
        os.makedirs(self.__storage_dir, exist_ok=True)
        
        # Load profiles from the file if it exists  
        if os.path.exists(self.__profiles_file):
            with open(self.__profiles_file, "r") as file:
                self.__profiles = json.load(file)

        # If file doesn't exist, create the file of an empty list
        else:
            with open(self.__profiles_file, "w") as file:
                json.dump([], file, indent=4)

    def create_profile(self, name: str, initialDPI: str) -> dict:
        try:
            # Chick if name or initialDPI is empty
            if not name or not initialDPI:
                raise ValueError("Please provide both a name and initial DPI")
            
            # Check if name contains only letters and numbers
            for char in name:
                if not is_alphanumeric(char) and not char.isspace():
                    raise ValueError("Name must contain only letters and numbers")
            
            # Check if name does not contain only spaces
            if name.isspace():
                raise ValueError("Name cannot contain only spaces")
            
            # Check if name is between 1 and 20 characters
            if not (1 <= len(name) <= 20):
                raise ValueError("Name must be between 1 and 20 characters")

            # Check if initialDPI is a number
            for char in initialDPI:
                if not char.isdigit():
                    raise ValueError("Initial DPI must be a number")

            initialDPI = int(initialDPI)
            
            # Check if initialDPI is between 100 and 3200
            if not (100 <= initialDPI <= 3200):
                raise ValueError("Initial DPI must be between 100 and 3200")
                
            # Check if profile name already exists
            for profile in self.__profiles:
                if profile['name'] == name:
                    raise ValueError("Profile already exists")
        
            # Check if there is at most 8 profiles
            if len(self.__profiles) >= 8:
                raise ValueError("You can only have at most 8 profiles")
            
        except Exception as e:
            return {"error": str(e)}

        new_profile = {}

        # Assign _id to profile for backend internal use
        if len(self.__profiles) == 0:
            new_profile['_id'] = 1
        else:
            new_profile['_id'] = self.__profiles[-1]['_id'] + 1

        new_profile['name'] = name
        new_profile['DPI'] = initialDPI
        new_profile['DPI_history'] = [{"timestamp": get_current_timestamp(), "DPI": initialDPI}]
        new_profile['session_total_distance'] = []
        self.__profiles.append(new_profile)

        with open(self.__profiles_file, "w") as file:
            json.dump(self.__profiles, file, indent=4)

        return {"message": "Profile created successfully", "profile": self.__profiles[-1]}
    
    def delete_profile(self, name: str) -> dict:
        for profile in self.__profiles:
            if profile['name'] == name:
                self.__profiles.remove(profile)

                with open(self.__profiles_file, "w") as file:
                    json.dump(self.__profiles, file, indent=4)

                return {"message": "Profile deleted successfully"}
            
        return {"error": "Profile not found"}
    
    def get_profiles(self):
        return self.__profiles
    
    def find_profile(self, name: str) -> dict:
        for profile in self.__profiles:
            if profile['name'] == name:
                return profile
        return {"error": "Profile not found"}
    
    def update_profile_dpi(self, name: str, new_dpi: int) -> dict:
        for profile in self.__profiles:
            if profile['name'] == name:
                # Check if new_dpi is between 100 and 3200
                if not (100 <= new_dpi <= 3200):
                    raise ValueError("New DPI must be between 100 and 3200")

                profile['DPI'] = new_dpi

                with open(self.__profiles_file, "w") as file:
                    json.dump(self.__profiles, file, indent=4)

                return {"message": "Profile updated successfully"}
            
        return {"error": "Profile not found"}
    
    def update_dpi(self, profile_id: int, dpi: int) -> dict:
        for profile in self.__profiles:
            
            if profile['_id'] == profile_id:
                profile['DPI'] = dpi
                profile['DPI_history'].append({"timestamp": get_current_timestamp(), "DPI": dpi})

                with open(self.__profiles_file, "w") as file:
                    json.dump(self.__profiles, file, indent=4)

                return {"message": "Profile updated successfully"}
            
        return {"error": "Profile not found"}
    
    def update_session_total_distance(self, profile_id: int, timestamp: str, total_distance: int) -> dict:
        for profile in self.__profiles:
            if profile['_id'] == profile_id:
                profile['session_total_distance'].append({"timestamp": format_timestamp(timestamp), "total_distance": round(total_distance)})

                with open(self.__profiles_file, "w") as file:
                    json.dump(self.__profiles, file, indent=4)

                return {"message": "Profile updated successfully"}
            
        return {"error": "Profile not found"}
    
if __name__ == "__main__":
    # Test create_profile here
    pass

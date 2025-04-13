import os
import json

class profileHandler:
    def __init__(self):
        self.__profiles = []

        current_dir = os.path.dirname(os.path.realpath(__file__))

        self.__storage_dir = os.path.join(current_dir, "storage")
        self.__profiles_file = os.path.join(self.__storage_dir, "profiles.json")
        
        # Create storage directory if it doesn't exist
        os.makedirs(self.__storage_dir, exist_ok=True)
        
        # Load profiles from file if it exists  
        if os.path.exists(self.__profiles_file):
            with open(self.__profiles_file, "r") as file:
                self.__profiles = json.load(file)

    def create_profile(self, name, initialDPI):

        try:
            for char in initialDPI:
                if not char.isdigit():
                    raise ValueError("Initial DPI must be a number")

            initialDPI = int(initialDPI)

            if not (1 <= len(name) <= 20):
                raise ValueError("Name must be between 1 and 20 characters")
            
            if not (100 <= initialDPI <= 3200):
                raise ValueError("Initial DPI must be between 100 and 3200")
            
            for char in name:
                if not char.isalnum() and not char.isspace():
                    raise ValueError("Name must contain only letters and numbers")
        
        except ValueError as e:
            return {"error": str(e)}

        new_profile = {}
        new_profile['name'] = name
        new_profile['initialDPI'] = initialDPI
        self.__profiles.append(new_profile)

        with open(self.__profiles_file, "w") as file:
            json.dump(self.__profiles, file, indent=4)

        return {"message": "Profile created successfully", "profile": self.__profiles[-1]}
    
    def get_profiles(self):
        return self.__profiles
    

if __name__ == "__main__":
    profileHandler = profileHandler()
    profileHandler.create_profile("John", "100")
    print(profileHandler.get_profiles())
import os
from datetime import datetime


# Parse timestamps and get the latest file
def extract_timestamp(file_path):
    # Example: id_2_cursor_log_2025-04-14_23-33-29.csv
    filename = os.path.basename(file_path)
    try:
        timestamp_str = filename.split("cursor_log_")[1].replace(".csv", "")
        return datetime.strptime(timestamp_str, "%Y-%m-%d_%H-%M-%S")
    except (IndexError, ValueError):
        return datetime.min  # fallback if format is off


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

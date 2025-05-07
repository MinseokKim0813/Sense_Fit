from Backend.analyze_module import AnalyzeModule
import os
import pytest
from unittest.mock import patch

# To simulate temp log files
from tempfile import TemporaryDirectory
import csv
from datetime import datetime, timedelta

def write_log_file(filepath, rows):
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'x', 'y', 'clicked'])  # Header
        writer.writerows(rows)

def generate_valid_rows(n=100):
    start = datetime.now()
    rows = []
    for i in range(n):
        time = (start + timedelta(milliseconds=i*100)).strftime('%Y-%m-%d %H:%M:%S.%f')
        rows.append([time, 100 + i, 100 + i, '0' if i % 2 == 0 else '1'])
    return rows




def test_valid_log():
    with TemporaryDirectory() as temp_dir:
        logs_path = os.path.join(temp_dir, "storage", "logs")
        os.makedirs(logs_path)
        file_path = os.path.join(logs_path, "id_1_cursor_log_sessionA.csv")
        write_log_file(file_path, generate_valid_rows())

        with patch("analyze_module.os.path.dirname", return_value=temp_dir):
            analyzer = AnalyzeModule(profile_id=1, session="sessionA", screen_width=1920, screen_height=1080)
            assert analyzer.handle_error() == {"message": "Data points are valid!"}


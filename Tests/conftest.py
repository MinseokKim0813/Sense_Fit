import pytest
import os
import csv
from datetime import datetime, timedelta
from tempfile import TemporaryDirectory

# --------- Helpers ---------

def write_log_file(filepath, rows):
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'x', 'y', 'clicked'])
        writer.writerows(rows)

def generate_valid_rows(n=100):
    start = datetime.now()
    rows = []
    for i in range(n):
        time = (start + timedelta(milliseconds=i*100)).strftime('%Y-%m-%d %H:%M:%S.%f')
        # Increment x and y every two steps to create pauses
        current_value = 100 + (i // 2)
        clicked = '0' if i % 2 == 0 else '1'
        rows.append([time, current_value, current_value, clicked])
    return rows

# --------- Fixtures ---------

@pytest.fixture
def temp_log_dir():
    with TemporaryDirectory() as temp_dir:
        logs_path = os.path.join(temp_dir, "storage", "logs")
        os.makedirs(logs_path)
        yield temp_dir, logs_path

@pytest.fixture
def create_valid_log_file(temp_log_dir):
    temp_dir, logs_path = temp_log_dir
    file_path = os.path.join(logs_path, "id_1_cursor_log_sessionA.csv")
    write_log_file(file_path, generate_valid_rows())
    return temp_dir  # used in patching

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


def generate_invalid_timestamp_rows(n=100):
    rows = generate_valid_rows(n)
    # Swap timestamps of two entries to create inconsistency
    if len(rows) > 10:
        rows[5][0], rows[10][0] = rows[10][0], rows[5][0]
    return rows

def generate_out_of_bounds_rows(n=100):
    rows = generate_valid_rows(n)
    for i in range(len(rows)):
        if i == 50:
            rows[i][1] = "1921"  # Out of screen_width (1920)
            rows[i][2] = "1081"  # Out of screen_height (1080)
    return rows

def generate_abrupt_movement_rows(n=100):
    rows = []
    start = datetime.now()
    for i in range(n):
        time = (start + timedelta(milliseconds=i*100)).strftime('%Y-%m-%d %H:%M:%S.%f')
        if i == 50:
            x = 1000  # Large jump from previous position (100 + 49 = 149)
            y = 1000
        else:
            x = 100 + i
            y = 100 + i
        rows.append([time, x, y, '0'])
    return rows


def generate_no_movement_rows(n=100):
    start = datetime.now()
    rows = []
    for i in range(n):
        time = (start + timedelta(milliseconds=i*100)).strftime('%Y-%m-%d %H:%M:%S.%f')
        rows.append([time, 100, 100, '0'])  # All positions are (100, 100)
    return rows

def generate_no_pause_rows(n=100):
    start = datetime.now()
    rows = []
    for i in range(n):
        time = (start + timedelta(milliseconds=i*100)).strftime('%Y-%m-%d %H:%M:%S.%f')
        x = 100 + i * 20
        y = 100 + i * 20
        clicked = int(0)
        rows.append([time, x, y, clicked])

    return rows


def generate_single_pause_rows(n=100):
    start = datetime.now()
    rows = []
    for i in range(n):
        time = (start + timedelta(milliseconds=i*100)).strftime('%Y-%m-%d %H:%M:%S.%f')
        if 5 <= i <= 10:
            # Pause at (0, 0) for 6 data points (0.6 seconds)
            x, y = 0, 0
        else:
            x, y = 0 + i*20, 0 + i*20
        rows.append([time, x, y, '0'])
    return rows

def generate_multiple_pause_rows(n=100):
    start = datetime.now()
    rows = []
    for i in range(n):
        time = (start + timedelta(milliseconds=i*100)).strftime('%Y-%m-%d %H:%M:%S.%f')
        if 5 <= i <= 10 or 20 <= i <= 25:
            # Two pauses
            x, y = 100, 100
        else:
            x, y = 100 + i*20, 100 + i*20
        rows.append([time, x, y, '0'])
    return rows

def generate_edge_pause_rows(n=100):
    start = datetime.now()
    rows = []
    for i in range(n):
        time = (start + timedelta(milliseconds=i*100)).strftime('%Y-%m-%d %H:%M:%S.%f')
        if i <= 5 or i >= 95:
            # Pause at start (indices 0-5) and end (indices 95-99)
            x, y = 100, 100
        else:
            x, y = 100 + i*20, 100 + i*20
        rows.append([time, x, y, '0'])
    return rows

def generate_short_pause_rows(n=100):
    start = datetime.now()
    rows = []
    for i in range(n):
        time = (start + timedelta(milliseconds=i*10)).strftime('%Y-%m-%d %H:%M:%S.%f')  # 10ms steps
        if 5 <= i <= 8:
            # 4 data points * 10ms = 40ms total (below 0.1s threshold)
            x, y = 100, 100
        else:
            x, y = 100 + i*20, 100 + i*20
        rows.append([time, x, y, '0'])
    return rows

def generate_no_clicks_rows(n=100):
    start = datetime.now()
    rows = []
    for i in range(n):
        time = (start + timedelta(milliseconds=i*100)).strftime('%Y-%m-%d %H:%M:%S.%f')
        rows.append([time, 100 + i, 100 + i, '0'])  # All clicks are '0'
    return rows

def generate_single_click_rows(n=100):
    start = datetime.now()
    rows = []
    for i in range(n):
        time = (start + timedelta(milliseconds=i*100)).strftime('%Y-%m-%d %H:%M:%S.%f')
        click = '1' if i == 50 else '0'  # Single click at index 50
        rows.append([time, 100 + i, 100 + i, click])
    return rows

def generate_rapid_clicks_rows(n=100):
    start = datetime.now()
    rows = []
    for i in range(n):
        time = (start + timedelta(milliseconds=i*100)).strftime('%Y-%m-%d %H:%M:%S.%f')
        # Clicks at indices 10 (0ms), 11 (100ms), 20 (1000ms)
        click = '1' if i in [10, 11, 20] else '0'
        rows.append([time, 100 + i, 100 + i, click])
    return rows

def generate_valid_multiclick_rows(n=100):
    start = datetime.now()
    rows = []
    for i in range(n):
        time = (start + timedelta(milliseconds=i*500)).strftime('%Y-%m-%d %H:%M:%S.%f')  # 500ms steps
        # Clicks at indices 0 (0ms), 2 (1000ms), 4 (2000ms)
        click = '1' if i in [0, 2, 4] else '0'
        rows.append([time, 100 + i, 100 + i, click])
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


@pytest.fixture
def create_short_log_file(temp_log_dir):
    temp_dir, logs_path = temp_log_dir
    file_path = os.path.join(logs_path, "id_1_cursor_log_sessionA.csv")
    write_log_file(file_path, generate_valid_rows(n=50))  # Only 50 rows
    return temp_dir



@pytest.fixture
def create_invalid_timestamps_log(temp_log_dir):
    temp_dir, logs_path = temp_log_dir
    file_path = os.path.join(logs_path, "id_1_cursor_log_sessionA.csv")
    write_log_file(file_path, generate_invalid_timestamp_rows())
    return temp_dir

@pytest.fixture
def create_out_of_bounds_log(temp_log_dir):
    temp_dir, logs_path = temp_log_dir
    file_path = os.path.join(logs_path, "id_1_cursor_log_sessionA.csv")
    write_log_file(file_path, generate_out_of_bounds_rows())
    return temp_dir

@pytest.fixture
def create_abrupt_movement_log(temp_log_dir):
    temp_dir, logs_path = temp_log_dir
    file_path = os.path.join(logs_path, "id_1_cursor_log_sessionA.csv")
    write_log_file(file_path, generate_abrupt_movement_rows())
    return temp_dir

@pytest.fixture
def create_no_movement_log(temp_log_dir):
    temp_dir, logs_path = temp_log_dir
    file_path = os.path.join(logs_path, "id_1_cursor_log_sessionA.csv")
    write_log_file(file_path, generate_no_movement_rows())
    return temp_dir

@pytest.fixture
def create_no_pause_log(temp_log_dir):
    temp_dir, logs_path = temp_log_dir
    file_path = os.path.join(logs_path, "id_1_cursor_log_sessionA.csv")
    write_log_file(file_path, generate_no_pause_rows())
    return temp_dir

@pytest.fixture
def create_single_pause_log(temp_log_dir):
    temp_dir, logs_path = temp_log_dir
    file_path = os.path.join(logs_path, "id_1_cursor_log_sessionA.csv")
    write_log_file(file_path, generate_single_pause_rows())
    return temp_dir

@pytest.fixture
def create_multiple_pause_log(temp_log_dir):
    temp_dir, logs_path = temp_log_dir
    file_path = os.path.join(logs_path, "id_1_cursor_log_sessionA.csv")
    write_log_file(file_path, generate_multiple_pause_rows())
    return temp_dir

@pytest.fixture
def create_edge_pause_log(temp_log_dir):
    temp_dir, logs_path = temp_log_dir
    file_path = os.path.join(logs_path, "id_1_cursor_log_sessionA.csv")
    write_log_file(file_path, generate_edge_pause_rows())
    return temp_dir

@pytest.fixture
def create_short_pause_log(temp_log_dir):
    temp_dir, logs_path = temp_log_dir
    file_path = os.path.join(logs_path, "id_1_cursor_log_sessionA.csv")
    write_log_file(file_path, generate_short_pause_rows())
    return temp_dir

@pytest.fixture
def create_no_clicks_log(temp_log_dir):
    temp_dir, logs_path = temp_log_dir
    file_path = os.path.join(logs_path, "id_1_cursor_log_sessionA.csv")
    write_log_file(file_path, generate_no_clicks_rows())
    return temp_dir

@pytest.fixture
def create_single_click_log(temp_log_dir):
    temp_dir, logs_path = temp_log_dir
    file_path = os.path.join(logs_path, "id_1_cursor_log_sessionA.csv")
    write_log_file(file_path, generate_single_click_rows())
    return temp_dir

@pytest.fixture
def create_rapid_clicks_log(temp_log_dir):
    temp_dir, logs_path = temp_log_dir
    file_path = os.path.join(logs_path, "id_1_cursor_log_sessionA.csv")
    write_log_file(file_path, generate_rapid_clicks_rows())
    return temp_dir

@pytest.fixture
def create_valid_multiclick_log(temp_log_dir):
    temp_dir, logs_path = temp_log_dir
    file_path = os.path.join(logs_path, "id_1_cursor_log_sessionA.csv")
    write_log_file(file_path, generate_valid_multiclick_rows())
    return temp_dir
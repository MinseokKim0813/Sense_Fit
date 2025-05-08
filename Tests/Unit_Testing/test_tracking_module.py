from unittest.mock import patch
from Backend.tracking_module import CursorTracker
import pytest
import os
import csv
from datetime import datetime


def test_csv_initialization(tmp_path, qtbot):
    # Mock storage directory to a temporary path
    with patch("os.path.realpath", return_value=str(tmp_path)):
        profile_id = 1
        tracker = CursorTracker(profile_id)
        qtbot.addWidget(tracker)
        
        log_file = tracker._CursorTracker__log_file
        assert os.path.exists(log_file)
        
        with open(log_file, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            assert header == ["timestamp", "X", "Y", "clicked"]

@patch("pyautogui.position")
def test_error_logging(mock_position, tmp_path, qtbot):
    mock_position.return_value = (100, 200)  # Fixed position
    with patch("os.path.realpath", return_value=str(tmp_path)):
        tracker = CursorTracker(1)
        qtbot.addWidget(tracker)
        
        # Simulate timer timeout to trigger logging
        tracker.update_cursor_position()
        
        # Read log file
        with open(tracker._CursorTracker__log_file, 'r') as f:
            rows = list(csv.reader(f))
            last_row = rows[-1]
            assert last_row[1] == "X"
            assert last_row[2] == "Y"
            assert last_row[3] == "clicked"
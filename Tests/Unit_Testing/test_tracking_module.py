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
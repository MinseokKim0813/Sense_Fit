from unittest.mock import patch
from Backend.analyze_module import AnalyzeModule
import pytest

def test_valid_log(create_valid_log_file):
    with patch("Backend.analyze_module.os.path.dirname", return_value=create_valid_log_file):
        analyzer = AnalyzeModule(profile_id=1, session="sessionA", screen_width=1920, screen_height=1080)
        assert analyzer.handle_error() == {"message": "Data points are valid!"}


def test_insufficient_data(create_short_log_file):
    with patch("Backend.analyze_module.os.path.dirname", return_value=create_short_log_file):
        analyzer = AnalyzeModule(profile_id=1, session="sessionA", screen_width=1920, screen_height=1080)
        result = analyzer.handle_error()
        assert "error" in result
        assert "Cursor tracking data is not sufficient" in result["error"]


def test_invalid_timestamps(create_invalid_timestamps_log):
    with patch("Backend.analyze_module.os.path.dirname", return_value=create_invalid_timestamps_log):
        analyzer = AnalyzeModule(profile_id=1, session="sessionA", screen_width=1920, screen_height=1080)
        result = analyzer.handle_error()
        assert "error" in result
        assert "timestamp of the tracking data is missing or invalid" in result["error"]

def test_out_of_bounds_positions(create_out_of_bounds_log):
    with patch("Backend.analyze_module.os.path.dirname", return_value=create_out_of_bounds_log):
        analyzer = AnalyzeModule(profile_id=1, session="sessionA", screen_width=1920, screen_height=1080)
        result = analyzer.handle_error()
        assert "error" in result

def test_abrupt_movement(create_abrupt_movement_log):
    with patch("Backend.analyze_module.os.path.dirname", return_value=create_abrupt_movement_log):
        analyzer = AnalyzeModule(profile_id=1, session="sessionA", screen_width=1920, screen_height=1080)
        result = analyzer.handle_error()
        assert "error" in result
        assert "Unusual cursor movement (Abrupt movement)" in result["error"]

def test_no_movement(create_no_movement_log):
    with patch("Backend.analyze_module.os.path.dirname", return_value=create_no_movement_log):
        analyzer = AnalyzeModule(profile_id=1, session="sessionA", screen_width=1920, screen_height=1080)
        result = analyzer.handle_error()
        assert "error" in result
        assert "Unusual cursor movement (No movement)" in result["error"]

def test_missing_log_file():
    with patch("Backend.analyze_module.os.path.dirname", return_value="/non/existent/directory"):
        with pytest.raises(Exception) as exc_info:
            AnalyzeModule(profile_id=1, session="sessionA", screen_width=1920, screen_height=1080)
        assert "Tracking log file not found" in str(exc_info.value)

def test_no_pauses(create_no_pause_log):
    with patch("Backend.analyze_module.os.path.dirname", return_value=create_no_pause_log):
        analyzer = AnalyzeModule(profile_id=1, session="sessionA", screen_width=3840, screen_height=2160)
        pause_segments = analyzer.get_pause_segments()
        assert len(pause_segments) == 0  # Expect no pauses

def test_single_pause(create_single_pause_log):
    with patch("Backend.analyze_module.os.path.dirname", return_value=create_single_pause_log):
        analyzer = AnalyzeModule(profile_id=1, session="sessionA", screen_width=3840, screen_height=2160)
        pause_segments = analyzer.get_pause_segments()
        assert len(pause_segments) == 1
        segment = pause_segments[0]
        assert segment["start_index"] == 5
        assert segment["end_index"] == 10
        assert segment["x"] == 0
        assert segment["y"] == 0

def test_multiple_pauses(create_multiple_pause_log):
    with patch("Backend.analyze_module.os.path.dirname", return_value=create_multiple_pause_log):
        analyzer = AnalyzeModule(profile_id=1, session="sessionA", screen_width=3840, screen_height=2160)
        pause_segments = analyzer.get_pause_segments()
        assert len(pause_segments) == 2
        # Validate first pause
        assert pause_segments[0]["start_index"] == 5
        assert pause_segments[0]["end_index"] == 10
        # Validate second pause
        assert pause_segments[1]["start_index"] == 20
        assert pause_segments[1]["end_index"] == 25
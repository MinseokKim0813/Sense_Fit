from unittest.mock import patch
from Backend.analyze_module import AnalyzeModule

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
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

def test_edge_pauses(create_edge_pause_log):
    with patch("Backend.analyze_module.os.path.dirname", return_value=create_edge_pause_log):
        analyzer = AnalyzeModule(profile_id=1, session="sessionA", screen_width=3840, screen_height=2160)
        pause_segments = analyzer.get_pause_segments()
        assert len(pause_segments) == 2
        # Validate start pause
        assert pause_segments[0]["start_index"] == 0
        assert pause_segments[0]["end_index"] == 5
        # Validate end pause
        assert pause_segments[1]["start_index"] == 95
        assert pause_segments[1]["end_index"] == 99

def test_short_pause_ignored(create_short_pause_log):
    with patch("Backend.analyze_module.os.path.dirname", return_value=create_short_pause_log):
        analyzer = AnalyzeModule(profile_id=1, session="sessionA", screen_width=3840, screen_height=2160)
        pause_segments = analyzer.get_pause_segments()
        assert len(pause_segments) == 0  # Duration too short

def test_custom_threshold(create_single_pause_log):
    with patch("Backend.analyze_module.os.path.dirname", return_value=create_single_pause_log):
        analyzer = AnalyzeModule(profile_id=1, session="sessionA", screen_width=3840, screen_height=2160)
        # Use threshold=5 (smaller than movement during non-pause)
        pause_segments = analyzer.get_pause_segments(threshold=5)
        assert len(pause_segments) == 1  # Still detects the pause

def test_no_clicks(create_no_clicks_log):
    with patch("Backend.analyze_module.os.path.dirname", return_value=create_no_clicks_log):
        analyzer = AnalyzeModule(profile_id=1, session="sessionA", screen_width=3840, screen_height=2160)
        end_positions = analyzer.find_end_points()
        assert end_positions == []

def test_single_click(create_single_click_log):
    with patch("Backend.analyze_module.os.path.dirname", return_value=create_single_click_log):
        analyzer = AnalyzeModule(profile_id=1, session="sessionA", screen_width=3840, screen_height=2160)
        end_positions = analyzer.find_end_points()
        assert end_positions == [50]

def test_rapid_clicks_filtered(create_rapid_clicks_log):
    with patch("Backend.analyze_module.os.path.dirname", return_value=create_rapid_clicks_log):
        analyzer = AnalyzeModule(profile_id=1, session="sessionA", screen_width=3840, screen_height=2160)
        end_positions = analyzer.find_end_points()
        # Expect only the first (index 10) and third (index 20) clicks
        assert end_positions == [10, 20]

def test_valid_multiclick(create_valid_multiclick_log):
    with patch("Backend.analyze_module.os.path.dirname", return_value=create_valid_multiclick_log):
        analyzer = AnalyzeModule(profile_id=1, session="sessionA", screen_width=3840, screen_height=2160)
        end_positions = analyzer.find_end_points()
        assert end_positions == [0, 2, 4]

def test_edge_clicks(create_edge_clicks_log):
    with patch("Backend.analyze_module.os.path.dirname", return_value=create_edge_clicks_log):
        analyzer = AnalyzeModule(profile_id=1, session="sessionA", screen_width=3840, screen_height=2160)
        end_positions = analyzer.find_end_points()
        assert end_positions == [0, 99]  # Both clicks are valid

def test_no_end_points(create_no_clicks_log):
    with patch("Backend.analyze_module.os.path.dirname", return_value=create_no_clicks_log):
        analyzer = AnalyzeModule(profile_id=1, session="sessionA", screen_width=3840, screen_height=2160)
        end_positions = analyzer.find_end_points()
        segments = analyzer.analyze_all_segment(end_positions)
        assert segments == []

def test_single_segment(create_single_endpoint_log):
    with patch("Backend.analyze_module.os.path.dirname", return_value=create_single_endpoint_log):
        analyzer = AnalyzeModule(profile_id=1, session="sessionA", screen_width=3840, screen_height=2160)
        end_positions = analyzer.find_end_points()
        segments = analyzer.analyze_all_segment(end_positions)
        
        assert len(segments) == 1
        segment = segments[0]
        assert segment["start_index"] == 0  # Should start from beginning
        assert segment["end_index"] == 80
        assert isinstance(segment["TD"], float)  # Total distance
        assert isinstance(segment["PD_list"], list)  # Pause distances

def test_multiple_segments(create_multiple_endpoint_log):
    with patch("Backend.analyze_module.os.path.dirname", return_value=create_multiple_endpoint_log):
        analyzer = AnalyzeModule(profile_id=1, session="sessionA", screen_width=3840, screen_height=2160)
        end_positions = analyzer.find_end_points()
        segments = analyzer.analyze_all_segment(end_positions)
        
        assert len(segments) == 3
        # Verify segment boundaries
        assert segments[0]["end_index"] == 20
        assert segments[1]["end_index"] == 60
        assert segments[2]["end_index"] == 90

def test_pause_in_segment(create_paused_segment_log):
    with patch("Backend.analyze_module.os.path.dirname", return_value=create_paused_segment_log):
        analyzer = AnalyzeModule(profile_id=1, session="sessionA", screen_width=3840, screen_height=2160)
        end_positions = analyzer.find_end_points()
        segments = analyzer.analyze_all_segment(end_positions)
        
        assert len(segments[0]["PD_list"]) > 0  # Should detect pauses
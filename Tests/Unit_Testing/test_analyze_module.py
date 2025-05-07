from unittest.mock import patch
from Backend.analyze_module import AnalyzeModule

def test_valid_log(create_valid_log_file):
    with patch("Backend.analyze_module.os.path.dirname", return_value=create_valid_log_file):
        analyzer = AnalyzeModule(profile_id=1, session="sessionA", screen_width=1920, screen_height=1080)
        assert analyzer.handle_error() == {"message": "Data points are valid!"}

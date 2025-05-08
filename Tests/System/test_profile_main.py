from Frontend.profile_main import ProfileWindow
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton
import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture
def profile_data():
    return {
        '_id': 1,
        'name': 'Test Profile',
        'DPI': 1200,
        'DPI_history': [],
        'session_total_distance': []
    }

@pytest.fixture
def profile_handler_mock():
    with patch('Backend.profile_handler.ProfileHandler') as mock:
        handler_instance = mock.return_value
        yield handler_instance

@pytest.fixture
def main_window_mock():
    with patch('Frontend.frontmain.MainInterface') as mock:
        window_instance = mock.return_value
        window_instance.build_profile_grid = MagicMock()
        yield window_instance

@pytest.fixture
def profile_window(qtbot, profile_data, main_window_mock, profile_handler_mock):
    # Mock the graph widgets
    with patch('Backend.DPIgraph.DPIGraphEmbed'):
        with patch('Backend.DTgraph.DTGraphEmbed'):
            window = ProfileWindow(profile_data, main_window_mock, profile_handler_mock)
            qtbot.addWidget(window)
            return window

def test_initialization(profile_window, profile_data):
    """Test that ProfileWindow initializes correctly"""
    # Check window title
    assert profile_window.windowTitle() == f"{profile_data['name']}'s Profile"
    
    # Check that profile data is set correctly
    assert profile_window.profile == profile_data
    
    # Check that UI elements are correctly initialized
    assert profile_window.title_label.text() == f"{profile_data['name']}'s Profile ({profile_data['DPI']} DPI)"
    assert profile_window.tracking_status_label.text() == "Tracking Disabled"
    assert profile_window.toggle_button.text() == "Off"

def test_go_back_normal(profile_window, qtbot):
    """Test going back to the main interface normally"""
    # Ensure no tracking is active
    profile_window.cursor_tracker = None
    
    # Find the back button - first find all buttons, then find the one with Back text
    buttons = profile_window.findChildren(QPushButton)
    back_button = None
    for button in buttons:
        if button.text() == "\u2190 Back":
            back_button = button
            break
    
    assert back_button is not None, "Back button not found"
    
    # Click the back button
    qtbot.mouseClick(back_button, Qt.LeftButton)
    
    # Main window's build_profile_grid should be called
    profile_window.main_interface.build_profile_grid.assert_called_once()


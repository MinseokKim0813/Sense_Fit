from pytestqt.qt_compat import qt_api
from Frontend.frontmain import MainInterface, ProfileCard, AddProfileCard

import pytest
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel
from unittest.mock import patch, MagicMock

@pytest.fixture
def app(qtbot, profile_handler_mock):
    with patch('Frontend.frontmain.ProfileHandler', return_value=profile_handler_mock):
        main_window = MainInterface()
        qtbot.addWidget(main_window)
        return main_window

@pytest.fixture
def profile_handler_mock():
    with patch('Frontend.frontmain.ProfileHandler') as mock:
        handler_instance = mock.return_value
        handler_instance.get_profiles.return_value = [
            {'_id': 1, 'name': 'Test Profile 1', 'DPI': 800, 'DPI_history': [], 'session_total_distance': []},
            {'_id': 2, 'name': 'Test Profile 2', 'DPI': 1600, 'DPI_history': [], 'session_total_distance': []}
        ]
        
        def find_profile_side_effect(name):
            for profile in handler_instance.get_profiles.return_value:
                if profile['name'] == name:
                    return profile
            return {"error": "Profile not found"}
            
        handler_instance.find_profile.side_effect = find_profile_side_effect
        
        yield handler_instance

def test_main_interface_initialization(qtbot, profile_handler_mock):
    with patch('Frontend.frontmain.ProfileHandler', return_value=profile_handler_mock):
        main_window = MainInterface()
        qtbot.addWidget(main_window)
        
        assert main_window.windowTitle() == "SenseFit"
        assert len(main_window.profiles) == 2

def test_profile_card_creation(qtbot, profile_handler_mock):

    test_profile = {'_id': 1, 'name': 'Test Profile', 'DPI': 800, 'DPI_history': [], 'session_total_distance': []}
    
    card = ProfileCard(test_profile, 200, 150)
    qtbot.addWidget(card)
    
    labels = card.findChildren(QLabel)
    name_label = labels[0]
    dpi_label = labels[1]
    
    assert test_profile['name'] in name_label.text()
    assert str(test_profile['DPI']) in dpi_label.text()
    
    with qtbot.waitSignal(card.clicked, timeout=1000) as blocker:
        qtbot.mouseClick(card, Qt.LeftButton)
    
    assert blocker.args[0] == test_profile

def test_add_profile_card(qtbot):
    card = AddProfileCard(200, 150)
    qtbot.addWidget(card)
    
    labels = card.findChildren(QLabel)
    plus_label = labels[0] 
    text_label = labels[1] 
    
    assert "+" in plus_label.text()
    assert "Create New Profile" in text_label.text()
    
    with qtbot.waitSignal(card.clicked, timeout=1000):
        qtbot.mouseClick(card, Qt.LeftButton)


def test_handle_add_profile(qtbot, profile_handler_mock):
    with patch('Frontend.frontmain.ProfileHandler', return_value=profile_handler_mock):
        with patch('Frontend.frontmain.CreateProfileDialog') as dialog_mock:
            dialog_instance = dialog_mock.return_value
            
            main_window = MainInterface()
            qtbot.addWidget(main_window)
            
            main_window.handle_add_profile()
            
            dialog_mock.assert_called_once_with(profile_handler_mock)
            
            assert dialog_instance.profile_created.connect.called

def test_main_window_functionality(app):
    assert app.windowTitle() == "SenseFit"
    
    title = app.findChild(QLabel)
    assert "Select Profile" in title.text()
    
    assert app.grid_layout is not None
    assert app.grid_layout.count() > 0

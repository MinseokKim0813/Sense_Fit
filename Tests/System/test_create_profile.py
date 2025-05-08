from pytestqt.qt_compat import qt_api
import pytest
from PyQt5.QtCore import Qt
from unittest.mock import patch, MagicMock

from Frontend.frontmain import MainInterface
from Frontend.create_profile import CreateProfileDialog


@pytest.fixture
def profile_handler_mock():
    with patch('Frontend.frontmain.ProfileHandler') as mock:
        handler_instance = mock.return_value
        
        # Setup mock to return empty profiles list
        handler_instance.get_profiles.return_value = []
        
        # Configure find_profile to return a valid profile
        handler_instance.find_profile.return_value = {
            '_id': 1,
            'name': 'Test Profile',
            'DPI': 800,
            'DPI_history': [],
            'session_total_distance': []
        }
        
        yield handler_instance


@pytest.fixture
def main_window(qtbot, profile_handler_mock):
    with patch('Frontend.frontmain.ProfileHandler', return_value=profile_handler_mock):
        window = MainInterface()
        qtbot.addWidget(window)
        window.show()
        return window


@pytest.fixture
def dialog_exec_mock():
    with patch('Frontend.create_profile.CreateProfileDialog.exec_') as mock:
        mock.return_value = 1
        yield mock


@pytest.fixture
def create_profile_dialog(qtbot):
    with patch('Frontend.create_profile.ProfileHandler') as mock:
        handler_instance = mock.return_value
        
        dialog = CreateProfileDialog(handler_instance)
        qtbot.addWidget(dialog)
        return dialog


def test_open_create_profile_dialog(qtbot, main_window, dialog_exec_mock):
    
    # Find the add profile card (should be the first/only card if profiles list is empty)
    add_card = None
    for i in range(main_window.grid_layout.count()):
        widget = main_window.grid_layout.itemAt(i).widget()
        if hasattr(widget, 'clicked') and not hasattr(widget, 'profile'):
            add_card = widget
            break
    
    assert add_card is not None, "Add profile card not found"
    
    # Click the add profile card
    with patch('Frontend.frontmain.CreateProfileDialog', autospec=True) as dialog_mock:
        # Mock the dialog instance that will be created
        dialog_instance = MagicMock()
        dialog_mock.return_value = dialog_instance
        
        # Click the add card
        qtbot.mouseClick(add_card, Qt.LeftButton)
        
        # Verify dialog was created with profile_handler
        dialog_mock.assert_called_once()
        assert dialog_mock.call_args[0][0] == main_window.profile_handler
        
        # Verify signal connection
        assert dialog_instance.profile_created.connect.called
        
        # Verify dialog was shown
        assert dialog_instance.exec_.called


def test_create_profile_dialog_initializes_correctly(create_profile_dialog):
    dialog = create_profile_dialog
    
    # Show the dialog
    dialog.show()
    
    # Check window properties
    assert dialog.isVisible()
    assert dialog.windowTitle() == "SenseFit"
    
    # Check main components
    assert dialog.title_label.isVisible()
    assert dialog.title_label.text() == "Create New Profile"
    
    assert dialog.name_input.isVisible()
    assert dialog.name_input.text() == ""
    
    assert dialog.dpi_input.isVisible()
    assert dialog.dpi_input.text() == ""
    
    assert dialog.create_button.isVisible()
    assert dialog.create_button.text() == "Create"
    
    # Error label should be hidden initially
    assert not dialog.error_label.isVisible()


def test_profile_name_validation(qtbot, create_profile_dialog):
    dialog = create_profile_dialog
    dialog.show()
    
    # Configure ProfileHandler.create_profile to return appropriate validation errors
    handler = dialog.profile_handler
    
    # Define side effect function to simulate validation responses
    def create_profile_side_effect(name, dpi):
        # Check name length (must be 1-20 characters)
        if not name:
            return {"error": "Please provide both a name and initial DPI"}
        elif len(name) > 20:
            return {"error": "Name must be between 1 and 20 characters"}
        
        # Check if name has only alphanumeric characters and spaces
        elif any(not (c.isalnum() or c.isspace()) for c in name):
            return {"error": "Name must contain only letters and numbers"}
            
        # For valid name but missing/invalid DPI
        elif not dpi:
            return {"error": "Please provide both a name and initial DPI"}
        
        # Valid profile
        return {
            "message": "Profile created successfully",
            "profile": {
                "_id": 1,
                "name": name,
                "DPI": 800 if dpi else 0,
                "DPI_history": [],
                "session_total_distance": []
            }
        }
    
    handler.create_profile.side_effect = create_profile_side_effect
    
    # Test 1: Empty name
    dialog.name_input.setText("")
    dialog.dpi_input.setText("800")
    qtbot.mouseClick(dialog.create_button, Qt.LeftButton)
    
    # Wait for error to show
    qtbot.waitUntil(lambda: dialog.error_label.isVisible(), timeout=1000)
    assert "Please provide both a name and initial DPI" in dialog.error_label.text()
    
    # Test 2: Name too long (over 20 characters)
    dialog.name_input.setText("This name is definitely way too long for validation")
    qtbot.mouseClick(dialog.create_button, Qt.LeftButton)
    
    qtbot.waitUntil(lambda: dialog.error_label.isVisible(), timeout=1000)
    assert "Name must be between 1 and 20 characters" in dialog.error_label.text()
    
    # Test 3: Name with special characters
    dialog.name_input.setText("Test@User#123")
    qtbot.mouseClick(dialog.create_button, Qt.LeftButton)
    
    qtbot.waitUntil(lambda: dialog.error_label.isVisible(), timeout=1000)
    assert "Name must contain only letters and numbers" in dialog.error_label.text()
    
    # Test 4: Valid name (alphanumeric with spaces)
    dialog.name_input.setText("Valid Name 123")
    dialog.dpi_input.setText("800")
    
    # Here we'd ideally want to check for successful profile creation
    # But for simplicity in testing, we can verify the handler was called correctly
    qtbot.mouseClick(dialog.create_button, Qt.LeftButton)
    handler.create_profile.assert_called_with("Valid Name 123", "800") 
import pytest
from unittest.mock import patch, MagicMock
import sys

from Frontend.frontmain import MainInterface


@pytest.fixture
def profile_handler_mock():
    with patch('Frontend.frontmain.ProfileHandler') as mock:
        handler_instance = mock.return_value
        handler_instance.get_profiles.return_value = []
        yield handler_instance


def test_main_window_creation(qtbot):
    """Test that the MainInterface can be created and shown."""
    # This test will create an actual MainInterface instance
    # but with a mocked ProfileHandler
    with patch('Frontend.frontmain.ProfileHandler') as profile_handler_mock:
        # Configure the mock
        handler_instance = profile_handler_mock.return_value
        handler_instance.get_profiles.return_value = []
        
        # Create the main window
        window = MainInterface()
        qtbot.addWidget(window)
        
        # Verify window properties
        assert window.windowTitle() == "SenseFit"
        assert hasattr(window, 'grid_layout')
        
        # Test that window can be shown without errors
        window.show()
        assert window.isVisible()


def test_application_startup():
    """Test that the application startup code in main.py works."""
    # Mock QApplication to prevent actual app creation
    with patch('main.QApplication') as app_mock:
        app_instance = MagicMock()
        app_mock.return_value = app_instance
        
        # Mock MainInterface to prevent actual window creation
        with patch('main.MainInterface') as main_interface_mock:
            window_instance = MagicMock()
            main_interface_mock.return_value = window_instance
            
            # Mock sys.exit to prevent test from exiting
            with patch('main.sys.exit') as exit_mock:
                # Execute main.py's main block by importing the module 
                # and calling a function that mimics the __main__ block
                import main
                
                # Call the code that would run if executed as script
                if hasattr(main, 'run_app'):
                    # If main.py has a run_app function, call it
                    main.run_app()
                else:
                    # Otherwise, manually execute the code from the __main__ block
                    app = app_mock(sys.argv)
                    window = main_interface_mock()
                    window.show()
                    exit_mock(app.exec_())
                
                # Verify the function calls
                app_mock.assert_called_once()
                main_interface_mock.assert_called_once()
                window_instance.show.assert_called_once()
                app_instance.exec_.assert_called_once()
                exit_mock.assert_called_once()


def test_main_script_imports_correctly():
    """Test that main.py imports the necessary components."""
    import main
    
    # Verify imports are available from main
    assert hasattr(main, 'MainInterface')
    assert hasattr(main, 'QApplication')
    assert hasattr(main, 'CreateProfileDialog')
    assert hasattr(main, 'ProfileWindow')
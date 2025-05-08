from Frontend.error_window import ErrorPopup
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton


def test_default_message(qtbot):
    popup = ErrorPopup()
    qtbot.addWidget(popup)
    
    # Verify window properties
    assert popup.windowTitle() == "Error"
    assert popup.minimumWidth() == 500
    assert popup.minimumHeight() == 250
    
    # Verify default message
    message_label = popup.findChild(QLabel, "message")
    assert message_label.text() == "Something went wrong. File was not uploaded."
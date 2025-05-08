from Frontend.alert_window_one_button import Popup_OK_Only
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton

def test_default_initialization(qtbot):
    popup = Popup_OK_Only()
    qtbot.addWidget(popup)
    
    assert popup.windowTitle() == "Warning"
    assert popup.findChild(QLabel, "message").text() == "Default Message"
    ok_btn = next(b for b in popup.findChildren(QPushButton) if b.text() == "OK")
    assert ok_btn
from Frontend.alert_window import Popup
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton


def test_default_initialization(qtbot):
    popup = Popup()
    qtbot.addWidget(popup)
    
    assert popup.windowTitle() == "Alert"
    assert popup.findChild(QLabel, "message").text() == "Default Message"
    ok_btn = next(b for b in popup.findChildren(QPushButton) if b.text() == "OK")
    no_btn = next(b for b in popup.findChildren(QPushButton) if b.text() == "NO")
    assert ok_btn and no_btn
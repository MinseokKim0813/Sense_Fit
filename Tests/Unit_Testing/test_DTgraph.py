import pytest
from PyQt5.QtWidgets import QApplication
from Backend.DTgraph import DTGraphEmbed
from datetime import datetime, timedelta
import pyqtgraph as pg

def test_empty_data(qtbot):
    profile = {"session_total_distance": []}
    widget = DTGraphEmbed(profile)
    qtbot.addWidget(widget)
    
    # Verify empty graph
    assert len(widget.graph_widget.listDataItems()) == 0

def test_24h_time_frame(qtbot):
    now = datetime.now()
    profile = {
        "session_total_distance": [
            {"timestamp": (now - timedelta(hours=23)).strftime("%Y-%m-%d %H:%M:%S"), "total_distance": 100},
            {"timestamp": (now - timedelta(hours=25)).strftime("%Y-%m-%d %H:%M:%S"), "total_distance": 200}  # Expired
        ]
    }
    widget = DTGraphEmbed(profile)
    qtbot.addWidget(widget)
    
    # Should show 1 bar
    bars = [item for item in widget.graph_widget.items() if isinstance(item, pg.BarGraphItem)]
    assert len(bars) == 1
    assert bars[0].opts['height'] == [100]
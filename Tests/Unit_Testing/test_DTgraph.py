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

def test_weekly_aggregation(qtbot):
    now = datetime.now()
    profile = {
        "session_total_distance": [
            # Same day entries
            {"timestamp": (now - timedelta(days=1)).strftime("%Y-%m-%d 10:00:00"), "total_distance": 50},
            {"timestamp": (now - timedelta(days=1)).strftime("%Y-%m-%d 15:00:00"), "total_distance": 75},
            # Older than 7 days
            {"timestamp": (now - timedelta(days=8)).strftime("%Y-%m-%d 09:00:00"), "total_distance": 200}
        ]
    }
    widget = DTGraphEmbed(profile)
    qtbot.addWidget(widget)
    widget.dropdown.setCurrentIndex(1)  # Switch to weekly view
    
    # Should aggregate to 1 bar with 125 (50+75)
    bars = [item for item in widget.graph_widget.items() if isinstance(item, pg.BarGraphItem)]
    assert bars[0].opts['height'] == [125]

def test_yaxis_scaling(qtbot):
    profile = {
        "session_total_distance": [
            {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "total_distance": 1500}
        ]
    }
    widget = DTGraphEmbed(profile)
    qtbot.addWidget(widget)
    
    ymin, ymax = widget.graph_widget.getViewBox().viewRange()[1]
    assert ymin == 0.0
    assert ymax == 1500 * 1.1  # 1650
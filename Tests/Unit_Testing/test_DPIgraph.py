import pytest
from PyQt5.QtWidgets import QApplication
from Backend.DPIgraph import DPIGraphEmbed


def test_empty_dpi_history(qtbot):
    profile = {"DPI_history": []}
    widget = DPIGraphEmbed(profile)
    qtbot.addWidget(widget)
    
    # Verify no data is plotted
    assert len(widget.plotItem.listDataItems()) == 0


def test_exactly_five_entries(qtbot):
    history = [
        {"timestamp": f"2023-01-0{i+1} 10:00:00", "DPI": 800 + i*100}
        for i in range(5)
    ]
    profile = {"DPI_history": history}
    widget = DPIGraphEmbed(profile)
    qtbot.addWidget(widget)
    
    # Verify all 5 points are plotted
    items = widget.plotItem.listDataItems()
    x_data, y_data = items[0].getData()
    assert len(y_data) == 5

def test_more_than_five_entries(qtbot):
    history = [
        {"timestamp": f"2023-01-0{i+1} 10:00:00", "DPI": 800}
        for i in range(6)
    ]
    profile = {"DPI_history": history}
    widget = DPIGraphEmbed(profile)
    qtbot.addWidget(widget)
    
    # Verify averaged data + recent entries
    items = widget.plotItem.listDataItems()
    x_data, y_data = items[0].getData()
    assert y_data[0] == 800  # Average of first 2 entries
    assert list(y_data[1:]) == [800, 800, 800, 800]  # Last 4 entries

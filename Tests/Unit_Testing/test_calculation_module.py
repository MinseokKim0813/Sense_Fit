from unittest.mock import patch
from Backend.calculate_module import DPICalculationModule
import pytest

@pytest.fixture
def calculate_module():
    current_profile = {'_id': 1, 'name': 'test', 'DPI': 100, 'DPI_history': [], 'session_total_distance': []}
    return DPICalculationModule(current_profile, [])

def test_create_calculate_module(calculate_module):
    # calculate_module = calculate_module()
    assert calculate_module is not None

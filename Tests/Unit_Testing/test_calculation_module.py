from Backend.calculate_module import DPICalculationModule
import pytest

@pytest.fixture
def profile():
    return {'_id': 1, 'name': 'test', 'DPI': 600, 'DPI_history': [], 'session_total_distance': []}

def test_create_calculate_module(profile):
    calculate_module = DPICalculationModule(profile, [])
    assert calculate_module is not None

def test_calculate_dpi_pause_points(profile):
    calculate_module = DPICalculationModule(profile, [{'start_index': 0, 'end_index': 73, 'PD_list': [], 'OS_distance': None, 'TD': 414}, {'start_index': 98, 'end_index': 217, 'PD_list': [126, 80], 'OS_distance': None, 'TD': 400}])
    assert calculate_module.calculate_dpi()['DPI_recommendation'] > profile['DPI']
    

def test_calculate_dpi_overshoot(profile):
    calculate_module = DPICalculationModule(profile, [{'start_index': 55, 'end_index': 187, 'PD_list': [], 'OS_distance': 92, 'TD': 486}])
    assert calculate_module.calculate_dpi()['DPI_recommendation'] < profile['DPI']

def test_calculate_dpi_pause_and_overshoot(profile):
    calculate_module = DPICalculationModule(profile, [{'start_index': 25, 'end_index': 383, 'PD_list': [210, 74], 'OS_distance': 55, 'TD': 435}, {'start_index': 408, 'end_index': 524, 'PD_list': [], 'OS_distance': 52, 'TD': 456}])
    assert calculate_module.calculate_dpi()['DPI_recommendation'] != profile['DPI']

def test_calculate_dpi_out_of_bounds():
    profile_low_dpi = {'_id': 1, 'name': 'test', 'DPI': 100, 'DPI_history': [], 'session_total_distance': []}
    calculate_module = DPICalculationModule(profile_low_dpi, [{'start_index': 55, 'end_index': 187, 'PD_list': [], 'OS_distance': 92, 'TD': 486}])
    assert calculate_module.calculate_dpi()['DPI_recommendation'] < profile_low_dpi['DPI']
    assert calculate_module.calculate_dpi()['out_of_bounds_flag'] == True

from Backend.profile_handler import ProfileHandler
import pytest
import json
import math
import random
from tempfile import TemporaryDirectory
import os
from unittest.mock import patch
from datetime import datetime

@pytest.fixture
def make_temp_dir():
    def _make_temp_dir(profile_count):
        temp_dir = TemporaryDirectory()
        profiles_path = os.path.join(temp_dir.name, "storage")
        os.makedirs(profiles_path)
        profile_file = os.path.join(profiles_path, "profiles.json")
        generate_profile_file(profile_file, profile_count)
        return temp_dir, profiles_path
    
    return _make_temp_dir

@pytest.fixture
def make_profile_handler():
    def _make_profile_handler(temp_dir, profiles_path):
        with patch("Backend.profile_handler.os.path.dirname", return_value=temp_dir.name):
            return ProfileHandler()
    return _make_profile_handler

def generate_profile_file(filepath, profile_count):
    with open(filepath, 'w', newline='') as file:
        json_data = []

        for i in range(profile_count):
            profile = {
                "_id": i+1,
                "name": f"profile_{i+1}",
                "DPI": math.floor(random.random() * 3100) + 100,
                "DPI_history": [],
                "session_total_distance": []
            }

            json_data.append(profile)

        json.dump(json_data, file, indent=4)


def test_initialize_profile_handler(make_temp_dir, make_profile_handler):
    temp_dir, profiles_path = make_temp_dir(profile_count=1)
    profile_handler = make_profile_handler(temp_dir, profiles_path)
    assert len(profile_handler.get_profiles()) == 1

def test_create_profile_normal(make_temp_dir, make_profile_handler):
    temp_dir, profiles_path = make_temp_dir(profile_count=1)
    profile_handler = make_profile_handler(temp_dir, profiles_path)
    response = profile_handler.create_profile("test profile", "1000")
    assert response["message"] == "Profile created successfully"

def test_create_profile_long_name(make_temp_dir, make_profile_handler):
    temp_dir, profiles_path = make_temp_dir(profile_count=1)
    profile_handler = make_profile_handler(temp_dir, profiles_path)
    response = profile_handler.create_profile("test profile exceeding 20 chars", "1000")
    assert "error" in response

def test_create_profile_name_only_spaces(make_temp_dir, make_profile_handler):
    temp_dir, profiles_path = make_temp_dir(profile_count=1)
    profile_handler = make_profile_handler(temp_dir, profiles_path)
    response = profile_handler.create_profile("     ", "1000")
    assert "error" in response

def test_create_profile_name_empty(make_temp_dir, make_profile_handler):
    temp_dir, profiles_path = make_temp_dir(profile_count=1)
    profile_handler = make_profile_handler(temp_dir, profiles_path)
    response = profile_handler.create_profile("", "1000")
    assert "error" in response



def test_create_profile_DPI_out_of_range(make_temp_dir, make_profile_handler):
    temp_dir, profiles_path = make_temp_dir(profile_count=1)
    profile_handler = make_profile_handler(temp_dir, profiles_path)
    response = profile_handler.create_profile("test profile", "10000")
    assert "error" in response

def test_create_profile_duplicate_name(make_temp_dir, make_profile_handler):
    temp_dir, profiles_path = make_temp_dir(profile_count=1)
    profile_handler = make_profile_handler(temp_dir, profiles_path)
    profile_handler.create_profile("test_profile", "1000")
    profile_handler.create_profile("test profile", "1200")
    response = profile_handler.create_profile("test profile", "1800")
    assert "error" in response

def test_create_profile_DPI_non_numeric(make_temp_dir, make_profile_handler):
    temp_dir, profiles_path = make_temp_dir(profile_count=1)
    profile_handler = make_profile_handler(temp_dir, profiles_path)
    response = profile_handler.create_profile("test profile", "non_numeric")
    assert "error" in response

def test_create_profile_exceeding_max_profiles(make_temp_dir, make_profile_handler):
    temp_dir, profiles_path = make_temp_dir(profile_count=8)
    profile_handler = make_profile_handler(temp_dir, profiles_path)
    profile_handler.create_profile("test_profile", "1000")
    response = profile_handler.create_profile("test profile", "1200")
    assert "error" in response

def test_create_profile_from_empty_file(make_temp_dir, make_profile_handler):
    temp_dir, profiles_path = make_temp_dir(profile_count=0)
    profile_handler = make_profile_handler(temp_dir, profiles_path)
    response = profile_handler.create_profile("test profile", "1000")
    assert response["message"] == "Profile created successfully"

def test_delete_profile_normal(make_temp_dir, make_profile_handler):
    temp_dir, profiles_path = make_temp_dir(profile_count=1)
    profile_handler = make_profile_handler(temp_dir, profiles_path)
    profile_handler.create_profile("test profile", "1000")
    response = profile_handler.delete_profile("test profile")
    assert response["message"] == "Profile deleted successfully"

def test_delete_profile_non_existent(make_temp_dir, make_profile_handler):
    temp_dir, profiles_path = make_temp_dir(profile_count=1)
    profile_handler = make_profile_handler(temp_dir, profiles_path)
    response = profile_handler.delete_profile("nonExistentProfile")
    assert "error" in response

def test_delete_profile_empty_file(make_temp_dir, make_profile_handler):
    pass

def test_refresh_profile_normal(make_temp_dir, make_profile_handler):
    temp_dir, profiles_path = make_temp_dir(profile_count=0)
    profile_handler = make_profile_handler(temp_dir, profiles_path)
    profile_handler.create_profile("test profile", "1000")
    response = profile_handler.refresh_profile(1)
    assert "error" not in response

def test_refresh_profile_non_existent(make_temp_dir, make_profile_handler):
    temp_dir, profiles_path = make_temp_dir(profile_count=0)
    profile_handler = make_profile_handler(temp_dir, profiles_path)
    response = profile_handler.refresh_profile(1)
    assert "error" in response

def test_find_profile_normal(make_temp_dir, make_profile_handler):
    temp_dir, profiles_path = make_temp_dir(profile_count=1)
    profile_handler = make_profile_handler(temp_dir, profiles_path)
    profile_handler.create_profile("test profile", "1000")
    response = profile_handler.find_profile("test profile")
    assert response["name"] == "test profile"
    
def test_find_profile_non_existent(make_temp_dir, make_profile_handler):
    temp_dir, profiles_path = make_temp_dir(profile_count=0)
    profile_handler = make_profile_handler(temp_dir, profiles_path)
    response = profile_handler.find_profile(1)
    assert response["error"] == "Profile not found"

def test_update_profile_dpi_normal(make_temp_dir, make_profile_handler):
    temp_dir, profiles_path = make_temp_dir(profile_count=1)
    profile_handler = make_profile_handler(temp_dir, profiles_path)
    profile_handler.create_profile("test profile", "1000")
    response = profile_handler.update_profile_dpi("test profile", 1200)
    assert response["message"] == "Profile updated successfully"

def test_update_profile_dpi_non_existent(make_temp_dir, make_profile_handler):
    temp_dir, profiles_path = make_temp_dir(profile_count=0)
    profile_handler = make_profile_handler(temp_dir, profiles_path)
    response = profile_handler.update_profile_dpi("nonExistentProfile", 1200)
    assert "error" in response

def test_update_profile_dpi_out_of_range(make_temp_dir, make_profile_handler):
    temp_dir, profiles_path = make_temp_dir(profile_count=0)
    profile_handler = make_profile_handler(temp_dir, profiles_path)
    profile_handler.create_profile("test profile", "1000")
    with pytest.raises(ValueError, match="New DPI must be between 100 and 3200"):
        profile_handler.update_profile_dpi("test profile", 3800)
    
def test_update_dpi(make_temp_dir, make_profile_handler):
    temp_dir, profiles_path = make_temp_dir(profile_count=0)
    profile_handler = make_profile_handler(temp_dir, profiles_path)
    profile_handler.create_profile("test profile", "1000")
    profile_handler.update_dpi(1, 1400)
    assert profile_handler.get_profiles()[0]["DPI"] == 1400

def test_update_dpi_non_existent(make_temp_dir, make_profile_handler):
    temp_dir, profiles_path = make_temp_dir(profile_count=0)
    profile_handler = make_profile_handler(temp_dir, profiles_path)
    response = profile_handler.update_dpi(1, 1400)
    assert "error" in response

def test_update_session_total_distance_normal(make_temp_dir, make_profile_handler):
    temp_dir, profiles_path = make_temp_dir(profile_count=0)
    profile_handler = make_profile_handler(temp_dir, profiles_path)
    profile_handler.create_profile("test profile", "1000")
    profile_handler.update_session_total_distance(1, datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), 1000)
    assert profile_handler.get_profiles()[0]["session_total_distance"][0]["total_distance"] == 1000

def test_update_session_total_distance_non_existent(make_temp_dir, make_profile_handler):
    temp_dir, profiles_path = make_temp_dir(profile_count=0)
    profile_handler = make_profile_handler(temp_dir, profiles_path)
    response = profile_handler.update_session_total_distance(1, datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), 1000)
    assert "error" in response

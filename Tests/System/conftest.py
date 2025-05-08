import pytest
from Frontend.frontmain import MainInterface

@pytest.fixture
def app():
    return MainInterface()
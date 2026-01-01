"""
Configuration for advanced feature tests.
"""
import pytest
from src.services.task_storage import initialize_storage


@pytest.fixture(autouse=True)
def reset_task_storage():
    """
    Reset the global task storage before each test to ensure clean state.
    This fixture runs automatically for all tests in the advanced test suite.
    """
    initialize_storage()
"""Dependency Track API Tests."""

import pytest
import requests_mock

from src import __version__
from src.dependency_track_api import DependencyTrack


@pytest.fixture(name="dependency_track_api")
def mock_dependency_track_api_fixture():
    """Fixture to mock DependencyTrack API."""
    with requests_mock.Mocker() as mocker:
        mocker.get("http://localhost:8081/api/version", json={"version": "4.10.1"})
        yield DependencyTrack(url="http://localhost:8081", api_key="dummy_api_key")


def test_dependency_track_api_version():
    """Test Dependency Track API Version."""
    assert __version__ == "0.1.0"


def test_dependency_track_api_with_mock(dependency_track_api):
    """Test Dependency Track API with mocked DependencyTrack."""
    assert dependency_track_api.host == "http://localhost:8081"
    assert dependency_track_api.get_version()["version"] == "4.10.1"
    dependency_track_api.close()

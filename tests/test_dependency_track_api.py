"""Dependency Track API Tests."""

import pytest

from dependency_track_api import DependencyTrack, DependencyTrackApiError, __version__


def test_dependency_track_api_version():
    """Test Dependency Track API Version."""
    assert __version__ == "0.1.3"


class MockResponse:
    """Mock class to simulate requests.Response."""

    def __init__(self, json_data: dict, status_code: int = 200):
        """Construct the MockResponse."""
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        """Return the JSON data."""
        return self.json_data

    def code(self):
        """Return the status code."""
        return self.status_code


@pytest.fixture(name="dependency_track_api")
def mock_dependency_track_api_fixture(mocker):
    """Mock DependencyTrack API."""
    mocker.patch(
        "dependency_track_api.requests.Session.get",
        return_value=MockResponse({"version": "4.10.1"}),
    )
    yield DependencyTrack(api_host="http://localhost:8081", api_key="dummy_api_key")


def test_dependency_track_api(dependency_track_api):
    """Test Dependency Track API with mocked DependencyTrack."""
    assert dependency_track_api.get_version()["version"] == "4.10.1"


def test_dependency_track_api_error_handling():
    """Test Dependency Track API error handling."""
    with pytest.raises(DependencyTrackApiError):
        mock_response = MockResponse({"message": "Not Found"}, status_code=404)
        dependency_track = DependencyTrack(
            api_host="http://localhost:8081", api_key="dummy_api_key"
        )
        dependency_track.session.get = lambda *args, **kwargs: mock_response
        dependency_track.get_version()

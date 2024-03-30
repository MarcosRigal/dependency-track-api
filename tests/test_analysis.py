"""Tests for the analysis module."""

from unittest.mock import MagicMock

import pytest

from dependency_track_api import DependencyTrack, DependencyTrackApiError


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


# Fixture for mocking DependencyTrack API
@pytest.fixture(name="dependency_track_api")
def mock_dependency_track_api_fixture(mocker):
    """Mock DependencyTrack API."""
    mocker.patch(
        "dependency_track_api.session.requests.Session.put",
        return_value=MockResponse({}),
    )
    mocker.patch(
        "dependency_track_api.session.requests.Session.get",
        return_value=MockResponse({}),
    )
    yield DependencyTrack(api_host="http://localhost:8081", api_key="dummy_api_key")


def test_retrieve_analysis_success(dependency_track_api):
    """Test retrieve analysis success."""
    dependency_track_api.session.get = MagicMock(
        return_value=MockResponse({"analysis_data": "dummy_data"}, status_code=200)
    )
    assert dependency_track_api.retrieve_analysis(
        project="dummy_project", component="dummy_component", vulnerability="dummy_vulnerability"
    ) == {"analysis_data": "dummy_data"}


def test_retrieve_analysis_unauthorized(dependency_track_api):
    """Test retrieve analysis unauthorized."""
    dependency_track_api.session.get = MagicMock(
        return_value=MockResponse({"message": "Unauthorized"}, status_code=401)
    )
    with pytest.raises(DependencyTrackApiError):
        dependency_track_api.retrieve_analysis(
            project="dummy_project",
            component="dummy_component",
            vulnerability="dummy_vulnerability",
        )


def test_retrieve_analysis_not_found(dependency_track_api):
    """Test retrieve analysis not found."""
    dependency_track_api.session.get = MagicMock(
        return_value=MockResponse({"message": "Not Found"}, status_code=404)
    )
    with pytest.raises(DependencyTrackApiError):
        dependency_track_api.retrieve_analysis(
            project="dummy_project",
            component="dummy_component",
            vulnerability="dummy_vulnerability",
        )


def test_update_analysis_success(dependency_track_api):
    """Test update analysis success."""
    dependency_track_api.session.put = MagicMock(
        return_value=MockResponse({"updated_analysis_data": "dummy_data"}, status_code=200)
    )
    assert dependency_track_api.update_analysis({"analysis_request": "dummy_request"}) == {
        "updated_analysis_data": "dummy_data"
    }


def test_update_analysis_unauthorized(dependency_track_api):
    """Test update analysis unauthorized."""
    dependency_track_api.session.put = MagicMock(
        return_value=MockResponse({"message": "Unauthorized"}, status_code=401)
    )
    with pytest.raises(DependencyTrackApiError):
        dependency_track_api.update_analysis({"analysis_request": "dummy_request"})


def test_update_analysis_not_found(dependency_track_api):
    """Test update analysis not found."""
    dependency_track_api.session.put = MagicMock(
        return_value=MockResponse({"message": "Not Found"}, status_code=404)
    )
    with pytest.raises(DependencyTrackApiError):
        dependency_track_api.update_analysis({"analysis_request": "dummy_request"})

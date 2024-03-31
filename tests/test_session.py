"""Tests for the DependencyTrackAPISession class."""

from unittest.mock import MagicMock

import pytest

from dependency_track_api import DependencyTrackAPISession


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


@pytest.fixture(name="dependency_track_api_session")
def mock_dependency_track_api_session_fixture():
    """Fixture for DependencyTrackAPISession."""
    return DependencyTrackAPISession(
        session_api_host="http://localhost:8081", session_api_key="dummy_api_key"
    )


def test_get_method(dependency_track_api_session):
    """Test get method."""
    dependency_track_api_session.session.get = MagicMock(
        return_value=MockResponse({"data": "dummy_data"}, status_code=200)
    )
    response = dependency_track_api_session.get("http://example.com")
    assert response.json() == {"data": "dummy_data"}
    assert response.status_code == 200


def test_post_method(dependency_track_api_session):
    """Test post method."""
    dependency_track_api_session.session.post = MagicMock(
        return_value=MockResponse({"data": "dummy_data"}, status_code=201)
    )
    response = dependency_track_api_session.post("http://example.com", json={"key": "value"})
    assert response.json() == {"data": "dummy_data"}
    assert response.status_code == 201


def test_put_method(dependency_track_api_session):
    """Test put method."""
    dependency_track_api_session.session.put = MagicMock(
        return_value=MockResponse({"data": "dummy_data"}, status_code=204)
    )
    response = dependency_track_api_session.put("http://example.com", json={"key": "value"})
    assert response.json() == {"data": "dummy_data"}
    assert response.status_code == 204


def test_delete_method(dependency_track_api_session):
    """Test delete method."""
    dependency_track_api_session.session.delete = MagicMock(
        return_value=MockResponse({"data": "dummy_data"}, status_code=204)
    )
    response = dependency_track_api_session.delete("http://example.com")
    assert response.json() == {"data": "dummy_data"}
    assert response.status_code == 204

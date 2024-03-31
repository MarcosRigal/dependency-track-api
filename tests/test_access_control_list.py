"""Test for the access control list module."""

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
        return_value=MockResponse(
            {
                "team": "d15a83fd-da70-9387-a698-6e9bc1ec1591",
                "project": "3cc0deca-3f9f-516c-30e0-ce14e7cdcdfb",
            }
        ),
    )
    yield DependencyTrack(api_host="http://localhost:8081", api_key="dummy_api_key")


def test_add_acl_mapping_success(dependency_track_api):
    """Test add ACL mapping success."""
    assert dependency_track_api.add_acl_mapping(
        team="d15a83fd-da70-9387-a698-6e9bc1ec1591",
        project="3cc0deca-3f9f-516c-30e0-ce14e7cdcdfb",
    ) == {
        "team": "d15a83fd-da70-9387-a698-6e9bc1ec1591",
        "project": "3cc0deca-3f9f-516c-30e0-ce14e7cdcdfb",
    }


def test_add_acl_mapping_unauthorized(dependency_track_api):
    """Test add ACL mapping unauthorized."""
    dependency_track_api.session.put = MagicMock(
        return_value=MockResponse({"message": "Unauthorized"}, status_code=401)
    )
    with pytest.raises(DependencyTrackApiError):
        dependency_track_api.add_acl_mapping(
            team="d15a83fd-da70-9387-a698-6e9bc1ec1591",
            project="3cc0deca-3f9f-516c-30e0-ce14e7cdcdfb",
        )


def test_add_acl_mapping_project_not_found(dependency_track_api):
    """Test add ACL mapping project not found."""
    dependency_track_api.session.put = MagicMock(
        return_value=MockResponse(
            {"message": "The UUID of the team or project could not be found"}, status_code=404
        )
    )
    with pytest.raises(DependencyTrackApiError):
        dependency_track_api.add_acl_mapping(
            team="d15a83fd-da70-9387-a698-6e9bc1ec1591",
            project="3cc0deca-3f9f-516c-30e0-ce14e7cdcdfb",
        )


def test_add_acl_mapping_mapping_already_exists(dependency_track_api):
    """Test add ACL mapping mapping already exists."""
    dependency_track_api.session.put = MagicMock(
        return_value=MockResponse(
            {"message": "A mapping with the same team and project already exists"}, status_code=409
        )
    )
    with pytest.raises(DependencyTrackApiError):
        dependency_track_api.add_acl_mapping(
            team="d15a83fd-da70-9387-a698-6e9bc1ec1591",
            project="3cc0deca-3f9f-516c-30e0-ce14e7cdcdfb",
        )


def test_delete_acl_mapping_success(dependency_track_api):
    """Test delete ACL mapping success."""
    dependency_track_api.session.delete = MagicMock(return_value=MockResponse({}, status_code=200))
    dependency_track_api.delete_mapping(
        team_uuid="d15a83fd-da70-9387-a698-6e9bc1ec1591",
        project_uuid="3cc0deca-3f9f-516c-30e0-ce14e7cdcdfb",
    )


def test_delete_acl_mapping_unauthorized(dependency_track_api):
    """Test delete ACL mapping unauthorized."""
    dependency_track_api.session.delete = MagicMock(
        return_value=MockResponse({"message": "Unauthorized"}, status_code=401)
    )
    with pytest.raises(DependencyTrackApiError):
        dependency_track_api.delete_mapping(
            team_uuid="d15a83fd-da70-9387-a698-6e9bc1ec1591",
            project_uuid="3cc0deca-3f9f-516c-30e0-ce14e7cdcdfb",
        )


def test_delete_acl_mapping_team_or_project_not_found(dependency_track_api):
    """Test delete ACL mapping team or project not found."""
    dependency_track_api.session.delete = MagicMock(
        return_value=MockResponse(
            {"message": "The UUID of the team or project could not be found"}, status_code=404
        )
    )
    with pytest.raises(DependencyTrackApiError):
        dependency_track_api.delete_mapping(
            team_uuid="d15a83fd-da70-9387-a698-6e9bc1ec1591",
            project_uuid="3cc0deca-3f9f-516c-30e0-ce14e7cdcdfb",
        )


def test_delete_acl_mapping_unexpected_status(dependency_track_api):
    """Test delete ACL mapping unexpected status."""
    dependency_track_api.session.delete = MagicMock(
        return_value=MockResponse({"message": "Unexpected status"}, status_code=500)
    )
    with pytest.raises(DependencyTrackApiError):
        dependency_track_api.delete_mapping(
            team_uuid="d15a83fd-da70-9387-a698-6e9bc1ec1591",
            project_uuid="3cc0deca-3f9f-516c-30e0-ce14e7cdcdfb",
        )


def test_retrieve_projects_for_team_success(dependency_track_api):
    """Test retrieve projects for team success."""
    dependency_track_api.session.get = MagicMock(
        return_value=MockResponse(["project_uuid_1", "project_uuid_2"], status_code=200)
    )
    assert dependency_track_api.retrieve_projects_for_team("team_uuid") == [
        "project_uuid_1",
        "project_uuid_2",
    ]


def test_retrieve_projects_for_team_unauthorized(dependency_track_api):
    """Test retrieve projects for team unauthorized."""
    dependency_track_api.session.get = MagicMock(
        return_value=MockResponse({"message": "Unauthorized"}, status_code=401)
    )
    with pytest.raises(DependencyTrackApiError):
        dependency_track_api.retrieve_projects_for_team("team_uuid")


def test_retrieve_projects_for_team_team_or_project_not_found(dependency_track_api):
    """Test retrieve projects for team team or project not found."""
    dependency_track_api.session.get = MagicMock(
        return_value=MockResponse(
            {"message": "The UUID of the team, project, or team could not be found"},
            status_code=404,
        )
    )
    with pytest.raises(DependencyTrackApiError):
        dependency_track_api.retrieve_projects_for_team("team_uuid")


def test_retrieve_projects_for_team_unexpected_status(dependency_track_api):
    """Test retrieve projects for team unexpected status."""
    dependency_track_api.session.get = MagicMock(
        return_value=MockResponse({"message": "Unexpected status"}, status_code=500)
    )
    with pytest.raises(DependencyTrackApiError):
        dependency_track_api.retrieve_projects_for_team("team_uuid")

"""Exceptions for the DependencyTrack API client."""


class DependencyTrackApiError(Exception):
    """Custom exception class for Dependency Track API errors."""

    def __init__(self, description, response):
        """Construct the DependencyTrackApiError."""
        super().__init__(description)
        self.description = description
        self.response = response
        self.message = response.json().get("message", "Unknown error")
        self.status_code = response.status_code

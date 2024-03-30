"""Main Dependency Track API Class."""

__version__ = "0.1.2"


from typing import Dict

import requests

from .access_control_list import AccessControlList
from .exceptions import DependencyTrackApiError


class DependencyTrack(AccessControlList):
    """
    Main Dependency Track API Class.

    This class provides methods to interact with the Dependency Track API.
    """

    def __init__(self, api_host: str, api_key: str):
        """
        Dependency Track API Class Constructor.

        Args:
            api_host (str): The host where is located the Dependency Track API instance.
            api_key (str): The API key for accessing the Dependency Track API.
        """
        super().__init__(api_host, api_key)
        self.api_host = api_host
        self.api_key = api_key
        self.api_base_url = self.api_host + "/api"
        self.session = requests.Session()
        self.session.headers.update({"X-Api-Key": f"{self.api_key}"})

    def close(self) -> None:
        """
        Close Dependency Track API Session.

        This method closes the session used to interact with the Dependency Track API.
        """
        self.session.close()

    def get_version(self) -> Dict:
        """
        Get Dependency Track API Version.

        Returns:
            dict: A dictionary containing information about the Dependency Track API version.

            The dictionary includes the following fields:
            - version (str): The version of the Dependency Track API.
            - timestamp (str): The timestamp when the version information was retrieved.
            - systemUuid (str): The UUID of the system.
            - uuid (str): The UUID of the Dependency Track instance.
            - application (str): The name of the Dependency Track application.
            - framework (dict): A dictionary containing information about the framework including:
                - name (str): The name of the framework.
                - version (str): The version of the framework.
                - timestamp (str): The timestamp when the framework information was retrieved.
                - uuid (str): The UUID of the framework instance.
        """
        response = self.session.get(f"{self.api_host}/version")

        if response.status_code == 200:
            return response.json()

        description = "Error while quering the api."
        raise DependencyTrackApiError(description, response)

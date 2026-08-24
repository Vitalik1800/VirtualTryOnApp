import json
from urllib.request import urlopen


class AccessoriesApiClient:
    """Client for communication with the accessories API."""

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8000"
    ) -> None:
        self.base_url = base_url

    def get_accessories(self) -> list[dict]:
        """Get available accessories from the server."""

        url = f"{self.base_url}/accessories/"

        with urlopen(url, timeout=5) as response:
            data = response.read().decode("utf-8")

        return json.loads(data)

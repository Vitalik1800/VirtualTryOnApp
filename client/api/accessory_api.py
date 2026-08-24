import requests


class AccessoryApi:
    """Provides access to the accessory API."""

    BASE_URL = "http://127.0.0.1:8000"

    def get_accessories(self) -> list[dict]:
        """Return accessories from the server."""

        response = requests.get(
            f"{self.BASE_URL}/accessories/",
            timeout=5
        )

        response.raise_for_status()

        return response.json()

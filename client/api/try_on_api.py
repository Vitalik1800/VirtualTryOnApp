import requests


class TryOnApi:
    """Provides access to the try-on API."""

    BASE_URL = "http://127.0.0.1:8000"

    def save_try_on(
        self,
        accessory_id: int,
        center_x: float,
        center_y: float,
        width: float,
        angle: float
    ) -> dict:
        """Save a virtual try-on."""

        response = requests.post(
            f"{self.BASE_URL}/try-on/",
            json={
                "accessory_id": accessory_id,
                "center_x": center_x,
                "center_y": center_y,
                "width": width,
                "angle": angle
            },
            timeout=5
        )

        response.raise_for_status()

        return response.json()

    def get_try_ons(self) -> list[dict]:
        """Return saved virtual try-ons."""

        response = requests.get(
            f"{self.BASE_URL}/try-on/",
            timeout=5
        )

        response.raise_for_status()

        return response.json()


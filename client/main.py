import customtkinter as ctk

from client.accessories.api_client import AccessoriesApiClient
from client.ui.main_window import MainWindow


class VirtualTryOnApp(ctk.CTk):
    """Main application."""

    def __init__(self) -> None:
        super().__init__()

        self.title("Virtual Try-On")
        self.geometry("1200x720")

        self.api_client = AccessoriesApiClient()

        self.main_window = MainWindow(
            self
        )

        self.main_window.pack(
            fill="both",
            expand=True
        )

        self._load_accessories()

    def _load_accessories(self) -> None:
        """Load accessories from the server."""

        try:
            accessories = self.api_client.get_accessories()

            print(
                f"Loaded accessories: {len(accessories)}"
            )

        except Exception as error:
            print(
                f"Failed to load accessories: {error}"
            )
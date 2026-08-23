import customtkinter as ctk


class StatusPanel(ctk.CTkFrame):
    """Displays the current state of the Virtual Try-On application."""

    def __init__(self, master) -> None:
        super().__init__(master)

        self.status_label = ctk.CTkLabel(
            self,
            text="Status: Ready",
            anchor="w"
        )

        self.status_label.pack(
            fill="x",
            padx=15,
            pady=(10, 5)
        )

        self.camera_label = ctk.CTkLabel(
            self,
            text="Camera: Off",
            anchor="w"
        )

        self.camera_label.pack(
            fill="x",
            padx=15,
            pady=5
        )

        self.accessory_label = ctk.CTkLabel(
            self,
            text="Accessory: None",
            anchor="w"
        )

        self.accessory_label.pack(
            fill="x",
            padx=15,
            pady=(5, 10)
        )

    def set_status(self, status: str) -> None:
        """Update application status."""

        self.status_label.configure(
            text=f"Status: {status}"
        )

    def set_camera_status(self, status: str) -> None:
        """Update camera status."""

        self.camera_label.configure(
            text=f"Camera: {status}"
        )

    def set_accessory(self, accessory: str) -> None:
        """Update selected accessory."""

        self.accessory_label.configure(
            text=f"Accessory: {accessory}"
        )

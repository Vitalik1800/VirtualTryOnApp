import customtkinter as ctk

from client.ui.control_panel import ControlPanel
from client.ui.status_panel import StatusPanel
from client.ui.video_preview import VideoPreview


class MainWindow(ctk.CTkFrame):
    """Main application window."""

    def __init__(self, master) -> None:
        super().__init__(master)

        self.pack(
            fill="both",
            expand=True
        )

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_columnconfigure(
            1,
            weight=0
        )

        self.grid_rowconfigure(
            0,
            weight=1
        )

        self._create_layout()

    def _create_layout(self) -> None:
        self.video_preview = VideoPreview(
            self
        )

        self.video_preview.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        self.control_panel = ControlPanel(
            self,
            on_start_camera=self._on_start_camera,
            on_stop_camera=self._on_stop_camera,
            on_accessory_selected=self._on_accessory_selected
        )

        self.control_panel.grid(
            row=0,
            column=1,
            sticky="ns",
            padx=10,
            pady=10
        )

        self.status_panel = StatusPanel(
            self
        )

        self.status_panel.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=(0, 10)
        )

    def _on_start_camera(self) -> None:
        self.status_panel.set_status("Camera started")
        self.status_panel.set_camera_status("On")
        self.status_panel.set_accessory(
            self.control_panel.selected_category
        )

    def _on_stop_camera(self) -> None:
        self.status_panel.set_status("Ready")
        self.status_panel.set_camera_status("Off")
        self.status_panel.set_accessory(
            self.control_panel.selected_category
        )

    def _on_accessory_selected(self, category: str) -> None:
        self.status_panel.set_status("Ready")
        self.status_panel.set_accessory(
            category
        )
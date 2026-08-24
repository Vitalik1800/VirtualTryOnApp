import customtkinter as ctk

from client.camera.camera_manager import CameraManager
from client.ui.control_panel import ControlPanel
from client.ui.status_panel import StatusPanel
from client.ui.video_preview import VideoPreview


class MainWindow(ctk.CTkFrame):
    """Main application window."""

    def __init__(self, master) -> None:
        super().__init__(master)

        self.camera_manager = CameraManager()
        self.camera_update_id = None
        self.camera_read_errors = 0

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

    def update_camera_frame(self) -> None:
        """Read and display the next camera frame."""

        if not self.camera_manager.is_opened():
            self.camera_update_id = None
            return

        frame = self.camera_manager.read_frame()

        if frame is None:
            self.camera_read_errors += 1

            if self.camera_read_errors >= 10:
                self._handle_camera_error(
                    "Camera stopped returning frames"
                )
                return

        else:
            self.camera_read_errors = 0

            image = self.camera_manager.prepare_frame(
                frame
            )

            if image is not None:
                self.video_preview.show_frame(
                    image
                )

        self.camera_update_id = self.after(
            30,
            self.update_camera_frame
        )

    def _on_start_camera(self) -> None:
        """Start the camera."""

        if self.camera_manager.is_opened():
            return

        self.camera_read_errors = 0

        if self.camera_manager.open():
            self.status_panel.set_status(
                "Camera started"
            )

            self.status_panel.set_camera_status(
                "On"
            )

            self.status_panel.set_accessory(
                self.control_panel.selected_category
            )

            self.update_camera_frame()

        else:
            self.status_panel.set_status(
                "Camera unavailable"
            )

            self.status_panel.set_camera_status(
                "Off"
            )

    def _on_stop_camera(self) -> None:
        """Stop the camera."""

        if self.camera_update_id is not None:
            self.after_cancel(
                self.camera_update_id
            )

            self.camera_update_id = None

        self.camera_manager.release()

        self.status_panel.set_status(
            "Ready"
        )

        self.status_panel.set_camera_status(
            "Off"
        )

        self.status_panel.set_accessory(
            self.control_panel.selected_category
        )

    def _on_accessory_selected(
            self,
            category: str
    ) -> None:
        """Handle accessory category selection."""

        self.status_panel.set_status(
            "Ready"
        )

        self.status_panel.set_accessory(
            category
        )

    def _handle_camera_error(
        self,
        message: str
    ) -> None:
        """Handle a camera error."""

        if self.camera_update_id is not None:
            self.after_cancel(
                self.camera_update_id
            )

            self.camera_update_id = None

        self.camera_manager.release()

        self.status_panel.set_status(
            message
        )

        self.status_panel.set_camera_status(
            "Off"
        )

        self.status_panel.set_accessory(
            self.control_panel.selected_category
        )

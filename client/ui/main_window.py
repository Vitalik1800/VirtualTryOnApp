import customtkinter as ctk
import requests

from client.accessories.accessory_manager import AccessoryManager
from client.accessories.accessory_renderer import AccessoryRenderer
from client.camera.camera_manager import CameraManager
from client.ui.control_panel import ControlPanel
from client.ui.status_panel import StatusPanel
from client.ui.video_preview import VideoPreview
from client.vision.face_detector import FaceDetector
from client.api.try_on_api import TryOnApi
from client.recording.video_recorder import VideoRecorder
from client.capture.image_capture import ImageCapture


class MainWindow(ctk.CTkFrame):
    """Main application window."""

    def __init__(self, master) -> None:
        super().__init__(master)

        self.camera_manager = CameraManager()
        self.face_detector = FaceDetector()

        self.accessory_manager = AccessoryManager()
        self.accessory_renderer = AccessoryRenderer()
        self.try_on_api = TryOnApi()
        self.video_recorder = VideoRecorder()
        self.image_capture = ImageCapture()

        self.current_frame = None
        self.current_try_on_position = None

        self.accessory_manager.load_accessories()

        self.accessory_manager.load_database_ids()

        print(
            "Loaded accessories:",
            len(self.accessory_manager.accessories)
        )

        print(
            "Selected accessory:",
            self.accessory_manager
            .get_selected_accessory()
            .name
        )

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
            on_accessory_selected=self._on_accessory_selected,
            on_save_try_on=self._save_try_on,
            on_record=self._toggle_recording,
            on_capture=self._capture
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
        """Read, process and display the next camera frame."""

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

            landmarks = self.face_detector.get_landmarks(
                frame
            )

            if landmarks is not None:
                key_landmarks = (
                    self.face_detector.get_key_landmarks(
                        landmarks,
                        frame.shape[1],
                        frame.shape[0]
                    )
                )

                frame = self.face_detector.draw_key_landmarks(
                    frame,
                    key_landmarks
                )

                active_accessory = (
                    self.accessory_manager
                    .get_selected_accessory()
                )

                if active_accessory is not None:
                    position = (
                        self.accessory_manager
                        .calculate_position(
                            key_landmarks
                        )
                    )

                    if position is not None:
                        self.current_try_on_position = position

                        frame = (
                            self.accessory_renderer.render(
                                frame=frame,
                                accessory_image=active_accessory.image,
                                center_x=position["center_x"],
                                center_y=position["center_y"],
                                width=position["width"],
                                angle=position["angle"]
                            )
                        )

                self.status_panel.set_status(
                    "Face detected"
                )

            else:
                self.status_panel.set_status(
                    "Face not detected"
                )

            self.current_frame = frame.copy()

            if self.video_recorder.is_recording():
                written = self.video_recorder.write(
                    frame
                )

                if not written:
                    self.video_recorder.stop()

                    self.control_panel.record_button.configure(
                        text="Record"
                    )

                    self.status_panel.set_status(
                        "Recording error"
                    )

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

        if self.video_recorder.is_recording():
            self.video_recorder.stop()

            self.control_panel.record_button.configure(
                text="Record"
            )

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
        """Select the next accessory from the category."""

        selected = (
            self.accessory_manager
            .select_next_by_category(
                category
            )
        )

        if selected:
            active_accessory = (
                self.accessory_manager
                .get_selected_accessory()
            )

            self.status_panel.set_status(
                f"{category}: {active_accessory.name}"
            )

        else:
            self.status_panel.set_status(
                f"No {category} accessories"
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

    def _save_try_on(self) -> None:
        """Save the current virtual try-on."""

        accessory = (
            self.accessory_manager
            .get_selected_accessory()
        )

        if accessory is None:
            self.status_panel.set_status(
                "No accessory selected"
            )
            return

        if accessory.id is None:
            self.status_panel.set_status(
                "Accessory ID is missing"
            )
            return

        if self.current_try_on_position is None:
            self.status_panel.set_status(
                "No active try-on"
            )
            return

        position = self.current_try_on_position

        try:
            result = self.try_on_api.save_try_on(
                accessory_id=accessory.id,
                center_x=position["center_x"],
                center_y=position["center_y"],
                width=position["width"],
                angle=position["angle"]
            )

            self.status_panel.set_status(
                f"Try-on saved: #{result['id']}"
            )

        except requests.RequestException:
            self.status_panel.set_status(
                "Failed to save try-on"
            )

    def _toggle_recording(self) -> None:
        """Start or stop video recording."""

        if not self.camera_manager.is_opened():
            self.status_panel.set_status(
                "Camera is not running"
            )
            return

        if self.video_recorder.is_recording():
            self.video_recorder.stop()

            self.status_panel.set_status(
                "Recording stopped"
            )

            self.control_panel.record_button.configure(
                text="Record"
            )

            return

        frame_width = (
            self.camera_manager.get_frame_width()
        )

        frame_height = (
            self.camera_manager.get_frame_height()
        )

        fps = (
            self.camera_manager.get_fps()
        )

        if frame_width <= 0 or frame_height <= 0:
            self.status_panel.set_status(
                "Invalid camera resolution"
            )
            return

        started = self.video_recorder.start(
            width=frame_width,
            height=frame_height,
            fps=fps
        )

        if not started:
            self.status_panel.set_status(
                "Failed to start recording"
            )
            return

        self.status_panel.set_status(
            "Recording..."
        )

        self.control_panel.record_button.configure(
            text="Stop Record"
        )

    def _capture(self) -> None:
        """Capture the current virtual try-on frame."""

        if not self.camera_manager.is_opened():
            self.status_panel.set_status(
                "Camera is not running"
            )
            return

        if self.current_frame is None:
            self.status_panel.set_status(
                "No frame available"
            )
            return

        output_path = self.image_capture.save(
            self.current_frame
        )

        if output_path is None:
            self.status_panel.set_status(
                "Failed to capture image"
            )
            return

        self.status_panel.set_status(
            f"Image saved: {output_path}"
        )

    def destroy(self):
        """Release application resources."""

        if self.video_recorder.is_recording():
            self.video_recorder.stop()

        if self.camera_update_id is not None:
            self.after_cancel(
                self.camera_update_id
            )

            self.camera_update_id = None

        self.camera_manager.release()
        self.face_detector.close()

        super().destroy()

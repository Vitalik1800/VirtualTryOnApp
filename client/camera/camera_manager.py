import cv2

from PIL import Image


class CameraManager:
    """Manages the webcam connection and video frames."""

    def __init__(self, camera_index: int = 0) -> None:
        self.camera_index = camera_index
        self.capture = None

    def open(self) -> bool:
        """Open the webcam."""

        self.release()

        try:
            self.capture = cv2.VideoCapture(
                self.camera_index
            )

            if not self.capture.isOpened():
                self.capture.release()
                self.capture = None
                return False

            return True

        except cv2.error:
            self.release()
            return False

    def read_frame(self):
        """Read a frame from the webcam."""

        if self.capture is None:
            return None

        try:
            success, frame = self.capture.read()

        except cv2.error:
            return None

        if not success or frame is None:
            return None

        return frame

    def prepare_frame(self, frame):
        """Convert OpenCV frame from BGR to PIL Image."""

        if frame is None:
            return None

        try:
            rgb_frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            return Image.fromarray(
                rgb_frame
            )

        except cv2.error:
            return None

    def release(self) -> None:
        """Release the webcam."""

        if self.capture is not None:
            self.capture.release()
            self.capture = None

    def is_opened(self) -> bool:
        """Check whether the webcam is opened."""

        return (
            self.capture is not None
            and self.capture.isOpened()
        )

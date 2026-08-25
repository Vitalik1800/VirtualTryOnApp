from datetime import datetime
from pathlib import Path

import cv2
import numpy as np


class VideoRecorder:
    """Records processed camera frames into a video file."""

    def __init__(
        self,
        output_directory: str = "data/videos",
        fps: float = 30.0
    ) -> None:
        self.output_directory = Path(
            output_directory
        )

        self.fps = fps
        self.writer: cv2.VideoWriter | None = None
        self.output_path: Path | None = None

    def start(
        self,
        width: int,
        height: int,
        fps: float | None = None
    ) -> bool:
        """Start video recording."""

        if width <= 0 or height <= 0:
            return False

        self.stop()

        if fps is not None and fps > 0:
            self.fps = fps

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        self.output_path = (
            self.output_directory
            / f"try_on_{timestamp}.mp4"
        )

        try:
            fourcc = cv2.VideoWriter_fourcc(
                *"mp4v"
            )

            self.writer = cv2.VideoWriter(
                str(self.output_path),
                fourcc,
                self.fps,
                (width, height)
            )

            if not self.writer.isOpened():
                self.writer.release()
                self.writer = None
                self.output_path = None

                return False

            return True

        except (cv2.error, OSError):
            if self.writer is not None:
                self.writer.release()

            self.writer = None
            self.output_path = None

            return False

    def write(
        self,
        frame: np.ndarray
    ) -> bool:
        """Write a frame to the video."""

        if self.writer is None:
            return False

        if frame is None:
            return False

        try:
            self.writer.write(
                frame
            )

            return True

        except cv2.error:
            return False

    def is_recording(self) -> bool:
        """Return whether recording is active."""

        return self.writer is not None

    def stop(self) -> Path | None:
        """Stop recording and release resources."""

        if self.writer is not None:
            self.writer.release()
            self.writer = None

        output_path = self.output_path

        self.output_path = None

        return output_path

    def get_output_path(self) -> Path | None:
        """Return the current output path."""

        return self.output_path

from datetime import datetime
from pathlib import Path

import cv2
import numpy as np


class ImageCapture:
    """Captures processed camera frames as images."""

    def __init__(
        self,
        output_directory: str = "data/captures"
    ) -> None:
        self.output_directory = Path(
            output_directory
        )

    def save(
        self,
        frame: np.ndarray
    ) -> Path | None:
        """Save a camera frame as a PNG image."""

        if frame is None:
            return None

        if not isinstance(frame, np.ndarray):
            return None

        if frame.size == 0:
            return None

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        output_path = (
            self.output_directory
            / f"try_on_{timestamp}.png"
        )

        try:
            success = cv2.imwrite(
                str(output_path),
                frame
            )

        except cv2.error:
            return None

        if not success:
            return None

        return output_path

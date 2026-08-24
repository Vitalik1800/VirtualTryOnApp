import cv2
import numpy as np

from PIL import Image


class AccessoryRenderer:
    """Renders an accessory on a video frame."""

    def render(
            self,
            frame: np.ndarray,
            accessory_image: Image.Image | None,
            center_x: float,
            center_y: float,
            width: float,
            angle: float = 0.0
    ) -> np.ndarray:
        """Render an accessory on a video frame."""

        if accessory_image is None:
            return frame

        if width <= 0:
            return frame

        image = accessory_image.convert(
            "RGBA"
        )

        # Remove transparent borders.
        alpha = image.getchannel("A")
        bbox = alpha.getbbox()

        if bbox is not None:
            image = image.crop(
                bbox
            )

        if image.width <= 0 or image.height <= 0:
            return frame

        # Calculate proportional size.
        scale = width / image.width

        target_width = max(
            1,
            int(width)
        )

        target_height = max(
            1,
            int(image.height * scale)
        )

        image = image.resize(
            (
                target_width,
                target_height
            ),
            Image.Resampling.LANCZOS
        )

        # Rotate the accessory.
        if angle != 0:
            image = image.rotate(
                angle,
                expand=True,
                resample=Image.Resampling.BICUBIC
            )

        overlay = np.array(
            image,
            dtype=np.uint8
        )

        if overlay.ndim != 3:
            return frame

        if overlay.shape[2] != 4:
            return frame

        overlay_height, overlay_width = (
            overlay.shape[:2]
        )

        x = int(
            center_x - overlay_width / 2
        )

        y = int(
            center_y - overlay_height / 2
        )

        self._overlay_image(
            frame,
            overlay,
            x,
            y
        )

        return frame

    def _overlay_image(
        self,
        frame: np.ndarray,
        overlay: np.ndarray,
        x: int,
        y: int
    ) -> None:
        """Overlay an RGBA image onto a BGR frame."""

        frame_height, frame_width = frame.shape[:2]
        overlay_height, overlay_width = overlay.shape[:2]

        x1 = max(0, x)
        y1 = max(0, y)

        x2 = min(
            frame_width,
            x + overlay_width
        )

        y2 = min(
            frame_height,
            y + overlay_height
        )

        if x1 >= x2 or y1 >= y2:
            return

        overlay_x1 = x1 - x
        overlay_y1 = y1 - y

        overlay_x2 = overlay_x1 + (
            x2 - x1
        )

        overlay_y2 = overlay_y1 + (
            y2 - y1
        )

        overlay_crop = overlay[
            overlay_y1:overlay_y2,
            overlay_x1:overlay_x2
        ]

        alpha = (
            overlay_crop[:, :, 3:4].astype(
                np.float32
            ) / 255.0
        )

        overlay_rgb = cv2.cvtColor(
            overlay_crop[:, :, :3],
            cv2.COLOR_RGB2BGR
        ).astype(
            np.float32
        )

        frame_region = frame[
            y1:y2,
            x1:x2
        ].astype(
            np.float32
        )

        result = (
            alpha * overlay_rgb
            + (1.0 - alpha) * frame_region
        )

        frame[
            y1:y2,
            x1:x2
        ] = np.clip(
            result,
            0,
            255
        ).astype(
            np.uint8
        )

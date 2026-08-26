from pathlib import Path

import cv2
import numpy as np

from client.capture.image_capture import ImageCapture


def create_test_frame() -> np.ndarray:
    """Create a test frame representing a processed camera image."""

    frame = np.zeros(
        (480, 640, 3),
        dtype=np.uint8
    )

    cv2.rectangle(
        frame,
        (240, 180),
        (400, 300),
        (255, 255, 255),
        -1
    )

    return frame


def test_full_capture_scenario(
    tmp_path: Path
) -> None:
    """Test the complete image capture scenario."""

    # 1. Create a processed camera frame.
    frame = create_test_frame()

    assert frame is not None
    assert frame.shape == (480, 640, 3)

    # 2. Create the image capture component.
    capture = ImageCapture(
        output_directory=str(tmp_path)
    )

    # 3. Capture the processed frame.
    output_path = capture.save(
        frame
    )

    # 4. Verify that the image was saved.
    assert output_path is not None

    path = Path(output_path)

    assert path.exists()
    assert path.is_file()

    # 5. Verify the file format.
    assert path.suffix.lower() == ".png"

    # 6. Read the captured image.
    captured_image = cv2.imread(
        str(path)
    )

    assert captured_image is not None

    # 7. Verify the captured image dimensions.
    assert captured_image.shape == (
        480,
        640,
        3
    )

    # 8. Verify that the captured image contains data.
    assert np.any(
        captured_image != 0
    )
    
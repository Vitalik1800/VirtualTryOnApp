from pathlib import Path

import cv2
import numpy as np

from client.capture.image_capture import ImageCapture


def test_capture_frame(tmp_path: Path) -> None:
    """Test saving a camera frame."""

    capture = ImageCapture(
        output_directory=str(tmp_path)
    )

    frame = np.zeros(
        (480, 640, 3),
        dtype=np.uint8
    )

    output_path = capture.save(
        frame
    )

    assert output_path is not None
    assert output_path.exists()
    assert output_path.suffix == ".png"
    assert output_path.stat().st_size > 0


def test_capture_creates_directory(
    tmp_path: Path
) -> None:
    """Test automatic creation of output directory."""

    output_directory = (
        tmp_path
        / "captures"
    )

    capture = ImageCapture(
        output_directory=str(output_directory)
    )

    frame = np.zeros(
        (480, 640, 3),
        dtype=np.uint8
    )

    output_path = capture.save(
        frame
    )

    assert output_path is not None
    assert output_directory.exists()
    assert output_path.exists()


def test_capture_none_frame(
    tmp_path: Path
) -> None:
    """Test handling of an invalid frame."""

    capture = ImageCapture(
        output_directory=str(tmp_path)
    )

    output_path = capture.save(
        None
    )

    assert output_path is None


def test_captured_image_can_be_read(
    tmp_path: Path
) -> None:
    """Test that the saved image can be opened."""

    capture = ImageCapture(
        output_directory=str(tmp_path)
    )

    frame = np.zeros(
        (480, 640, 3),
        dtype=np.uint8
    )

    output_path = capture.save(
        frame
    )

    assert output_path is not None

    image = cv2.imread(
        str(output_path)
    )

    assert image is not None
    assert image.shape == (
        480,
        640,
        3
    )

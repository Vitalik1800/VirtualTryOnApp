import numpy as np
from PIL import Image

from client.accessories.accessory import Accessory
from client.accessories.accessory_manager import AccessoryManager
from client.accessories.accessory_renderer import AccessoryRenderer
from client.vision.face_detector import FaceDetector


def create_frame() -> np.ndarray:
    """Create a test camera frame."""

    return np.zeros(
        (480, 640, 3),
        dtype=np.uint8
    )


def create_accessory_image() -> Image.Image:
    """Create a test accessory image."""

    return Image.new(
        "RGBA",
        (120, 60),
        (255, 255, 255, 255)
    )


def create_accessory() -> Accessory:
    """Create a test accessory."""

    return Accessory(
        name="test_glasses",
        category="Glasses",
        file_path="test.png",
        anchor_points=(
            "left_eye",
            "right_eye"
        ),
        scale_factor=1.5,
        rotation_enabled=True
    )


def create_accessory_manager() -> AccessoryManager:
    """Create an accessory manager with a selected accessory."""

    manager = AccessoryManager()

    accessory = create_accessory()

    manager.accessories.append(
        accessory
    )

    manager.selected_accessory = accessory

    return manager


def test_face_landmarks_are_used_for_accessory_position() -> None:
    """Test interaction between FaceDetector and AccessoryManager."""

    face_detector = FaceDetector()
    accessory_manager = create_accessory_manager()

    key_landmarks = {
        "left_eye": (240, 220),
        "right_eye": (400, 220)
    }

    position = accessory_manager.calculate_position(
        key_landmarks
    )

    assert position is not None

    assert position["center_x"] == 320.0
    assert position["center_y"] == 220.0
    assert position["width"] > 0
    assert isinstance(
        position["angle"],
        float
    )

    face_detector.close()


def test_landmarks_position_can_be_rendered() -> None:
    """Test the complete landmarks-to-rendering pipeline."""

    face_detector = FaceDetector()
    accessory_manager = create_accessory_manager()
    renderer = AccessoryRenderer()

    key_landmarks = {
        "left_eye": (240, 220),
        "right_eye": (400, 220)
    }

    position = accessory_manager.calculate_position(
        key_landmarks
    )

    assert position is not None

    frame = create_frame()
    accessory_image = create_accessory_image()

    result = renderer.render(
        frame=frame,
        accessory_image=accessory_image,
        center_x=position["center_x"],
        center_y=position["center_y"],
        width=position["width"],
        angle=position["angle"]
    )

    assert result is not None

    assert result.shape == frame.shape

    assert isinstance(
        result,
        np.ndarray
    )

    face_detector.close()


def test_face_landmarks_control_accessory_rotation() -> None:
    """Test that eye landmarks determine accessory rotation."""

    accessory_manager = create_accessory_manager()

    key_landmarks = {
        "left_eye": (200, 200),
        "right_eye": (300, 250)
    }

    position = accessory_manager.calculate_position(
        key_landmarks
    )

    assert position is not None

    assert position["angle"] != 0.0

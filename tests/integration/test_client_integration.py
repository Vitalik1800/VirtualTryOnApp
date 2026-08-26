import numpy as np

from client.accessories.accessory import Accessory
from client.accessories.accessory_manager import AccessoryManager
from client.accessories.accessory_renderer import AccessoryRenderer
from client.recording.video_recorder import VideoRecorder


def create_frame(
    width: int = 640,
    height: int = 480
) -> np.ndarray:
    """Create a test camera frame."""

    return np.zeros(
        (height, width, 3),
        dtype=np.uint8
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


def test_accessory_manager_and_renderer_integration() -> None:
    """Test accessory selection and rendering."""

    manager = AccessoryManager()
    renderer = AccessoryRenderer()

    accessory = create_accessory()

    manager.accessories.append(
        accessory
    )

    manager.selected_accessory = accessory

    selected = manager.get_selected_accessory()

    assert selected is accessory

    key_landmarks = {
        "left_eye": (250, 220),
        "right_eye": (390, 220)
    }

    position = manager.calculate_position(
        key_landmarks
    )

    assert position is not None
    assert position["center_x"] == 320
    assert position["center_y"] == 220
    assert position["width"] > 0

    frame = create_frame()

    result = renderer.render(
        frame=frame,
        accessory_image=None,
        center_x=position["center_x"],
        center_y=position["center_y"],
        width=position["width"],
        angle=position["angle"]
    )

    assert result is not None
    assert result.shape == frame.shape


def test_accessory_manager_position_is_usable_by_renderer() -> None:
    """Test that calculated position can be passed to renderer."""

    manager = AccessoryManager()

    accessory = create_accessory()

    manager.accessories.append(
        accessory
    )

    manager.selected_accessory = accessory

    key_landmarks = {
        "left_eye": (200, 200),
        "right_eye": (300, 210)
    }

    position = manager.calculate_position(
        key_landmarks
    )

    assert position is not None

    assert isinstance(
        position["center_x"],
        float
    )

    assert isinstance(
        position["center_y"],
        float
    )

    assert isinstance(
        position["width"],
        float
    )

    assert isinstance(
        position["angle"],
        float
    )


def test_video_recorder_integration() -> None:
    """Test starting, writing and stopping recording."""

    recorder = VideoRecorder(
        output_directory="tests/test_output"
    )

    frame = create_frame()

    started = recorder.start(
        width=frame.shape[1],
        height=frame.shape[0]
    )

    assert started is True
    assert recorder.is_recording() is True

    written = recorder.write(
        frame
    )

    assert written is True

    output_path = recorder.stop()

    assert output_path is not None
    assert output_path.exists()

    assert recorder.is_recording() is False

    output_path.unlink()

    output_path.parent.rmdir()
    
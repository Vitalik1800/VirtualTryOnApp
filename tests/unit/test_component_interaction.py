import numpy as np

from client.accessories.accessory import Accessory
from client.accessories.accessory_renderer import AccessoryRenderer
from client.accessories.accessory_manager import AccessoryManager
from client.recording.video_recorder import VideoRecorder
from PIL import Image


def create_frame() -> np.ndarray:
    """Create a test camera frame."""

    return np.zeros(
        (480, 640, 3),
        dtype=np.uint8
    )


def test_accessory_manager_and_renderer_interaction() -> None:
    """Test interaction between AccessoryManager and AccessoryRenderer."""

    manager = AccessoryManager()

    accessory = Accessory(
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

    manager.accessories.append(
        accessory
    )

    manager.selected_accessory = accessory

    key_landmarks = {
        "left_eye": (270, 220),
        "right_eye": (370, 220)
    }

    position = manager.calculate_position(
        key_landmarks
    )

    assert position is not None

    renderer = AccessoryRenderer()

    accessory.image = np_to_pil_image()

    frame = create_frame()

    result = renderer.render(
        frame=frame,
        accessory_image=accessory.image,
        center_x=position["center_x"],
        center_y=position["center_y"],
        width=position["width"],
        angle=position["angle"]
    )

    assert result is not None
    assert result.shape == frame.shape


def test_video_recorder_accepts_processed_frame(
    tmp_path
) -> None:
    """Test interaction between processed frame and VideoRecorder."""

    recorder = VideoRecorder(
        output_directory=str(tmp_path)
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
    assert output_path.stat().st_size > 0


def np_to_pil_image():
    """Create a simple RGBA accessory image."""

    return Image.new(
        "RGBA",
        (100, 50),
        (255, 255, 255, 255)
    )

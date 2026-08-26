from pathlib import Path

import cv2
import numpy as np

from client.recording.video_recorder import VideoRecorder


def create_test_frame() -> np.ndarray:
    """Create a test camera frame."""

    frame = np.zeros(
        (480, 640, 3),
        dtype=np.uint8
    )

    cv2.rectangle(
        frame,
        (200, 150),
        (440, 330),
        (255, 255, 255),
        -1
    )

    return frame


def test_full_record_stop_record_scenario(
    tmp_path: Path
) -> None:
    """Test the complete Record / Stop Record scenario."""

    recorder = VideoRecorder(
        output_directory=str(tmp_path),
        fps=30.0
    )

    frame = create_test_frame()

    # 1. Start recording.
    started = recorder.start(
        width=640,
        height=480
    )

    assert started is True
    assert recorder.is_recording() is True

    # 2. Write camera frames.
    for _ in range(30):
        written = recorder.write(
            frame
        )

        assert written is True

    # 3. Stop recording.
    output_path = recorder.stop()

    assert output_path is not None
    assert recorder.is_recording() is False

    # 4. Verify that the video file exists.
    path = Path(output_path)

    # 5. Verify the video format.
    assert path.suffix.lower() == ".mp4"

    # 6. Open the recorded video.
    capture = cv2.VideoCapture(
        str(path)
    )

    try:
        assert capture.isOpened() is True

        # 7. Check video properties.
        width = int(
            capture.get(
                cv2.CAP_PROP_FRAME_WIDTH
            )
        )

        height = int(
            capture.get(
                cv2.CAP_PROP_FRAME_HEIGHT
            )
        )

        frame_count = int(
            capture.get(
                cv2.CAP_PROP_FRAME_COUNT
            )
        )

        assert width == 640
        assert height == 480
        assert frame_count > 0

        # 8. Read the first recorded frame.
        success, recorded_frame = (
            capture.read()
        )

        assert success is True
        assert recorded_frame is not None

        assert recorded_frame.shape == (
            480,
            640,
            3
        )

    finally:
        capture.release()
        
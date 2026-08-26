from pathlib import Path

import cv2
import numpy as np

from client.recording.video_recorder import VideoRecorder


def test_start_recording(tmp_path: Path) -> None:
    """Test starting video recording."""

    recorder = VideoRecorder(
        output_directory=str(tmp_path)
    )

    result = recorder.start(
        width=640,
        height=480
    )

    assert result is True
    assert recorder.is_recording() is True
    assert recorder.get_output_path() is not None

    recorder.stop()


def test_write_frame(tmp_path: Path) -> None:
    """Test writing a frame to the video."""

    recorder = VideoRecorder(
        output_directory=str(tmp_path)
    )

    recorder.start(
        width=640,
        height=480
    )

    frame = np.zeros(
        (480, 640, 3),
        dtype=np.uint8
    )

    result = recorder.write(
        frame
    )

    assert result is True

    output_path = recorder.get_output_path()

    recorder.stop()

    assert output_path is not None
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_stop_recording(tmp_path: Path) -> None:
    """Test stopping video recording."""

    recorder = VideoRecorder(
        output_directory=str(tmp_path)
    )

    recorder.start(
        width=640,
        height=480
    )

    output_path = recorder.stop()

    assert recorder.is_recording() is False
    assert output_path is not None
    assert output_path.exists()


def test_invalid_resolution(tmp_path: Path) -> None:
    """Test starting recording with invalid resolution."""

    recorder = VideoRecorder(
        output_directory=str(tmp_path)
    )

    result = recorder.start(
        width=0,
        height=480
    )

    assert result is False
    assert recorder.is_recording() is False


def test_write_without_recording(tmp_path: Path) -> None:
    """Test writing a frame when recording is inactive."""

    recorder = VideoRecorder(
        output_directory=str(tmp_path)
    )

    frame = np.zeros(
        (480, 640, 3),
        dtype=np.uint8
    )

    result = recorder.write(
        frame
    )

    assert result is False


def test_write_invalid_frame(tmp_path: Path) -> None:
    """Test writing an invalid frame."""

    recorder = VideoRecorder(
        output_directory=str(tmp_path)
    )

    recorder.start(
        width=640,
        height=480
    )

    result = recorder.write(
        None
    )

    assert result is False

    recorder.stop()

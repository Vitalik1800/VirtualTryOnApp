import numpy as np

from client.camera.camera_manager import CameraManager
from client.vision.face_detector import FaceDetector


def create_test_frame() -> np.ndarray:
    """Create a test frame for camera processing."""

    return np.zeros(
        (480, 640, 3),
        dtype=np.uint8
    )


def test_camera_frame_can_be_processed_by_face_detector() -> None:
    """Test interaction between CameraManager and FaceDetector."""

    camera_manager = CameraManager()
    face_detector = FaceDetector()

    frame = create_test_frame()

    camera_manager.read_frame = lambda: frame

    received_frame = camera_manager.read_frame()

    assert received_frame is not None
    assert received_frame.shape == (
        480,
        640,
        3
    )

    landmarks = face_detector.get_landmarks(
        received_frame
    )

    assert landmarks is None or hasattr(
        landmarks,
        "landmark"
    )

    face_detector.close()


def test_camera_frame_has_correct_format() -> None:
    """Test that a camera frame has a format supported by FaceDetector."""

    camera_manager = CameraManager()
    face_detector = FaceDetector()

    frame = create_test_frame()

    camera_manager.read_frame = lambda: frame

    received_frame = camera_manager.read_frame()

    assert isinstance(
        received_frame,
        np.ndarray
    )

    assert received_frame.dtype == np.uint8

    assert received_frame.ndim == 3

    assert received_frame.shape[2] == 3

    result = face_detector.process_frame(
        received_frame
    )

    assert result is not None

    face_detector.close()


def test_face_detector_handles_frame_without_face() -> None:
    """Test FaceDetector behavior when no face is detected."""

    camera_manager = CameraManager()
    face_detector = FaceDetector()

    frame = create_test_frame()

    camera_manager.read_frame = lambda: frame

    received_frame = camera_manager.read_frame()

    landmarks = face_detector.get_landmarks(
        received_frame
    )

    assert landmarks is None

    face_detector.close()

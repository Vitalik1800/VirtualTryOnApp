import cv2
import numpy as np

from client.vision.face_detector import FaceDetector


def create_frame(
    width: int = 640,
    height: int = 480
) -> np.ndarray:
    """Create a test OpenCV frame."""

    return np.zeros(
        (height, width, 3),
        dtype=np.uint8
    )


def test_prepare_frame() -> None:
    """Test conversion of an OpenCV frame to RGB."""

    detector = FaceDetector()

    frame = create_frame()

    result = detector._prepare_frame(
        frame
    )

    assert result is not None
    assert result.shape == frame.shape
    assert result.dtype == frame.dtype

    detector.close()


def test_prepare_frame_with_none() -> None:
    """Test frame preparation with None."""

    detector = FaceDetector()

    result = detector._prepare_frame(
        None
    )

    assert result is None

    detector.close()


def test_process_frame() -> None:
    """Test MediaPipe frame processing."""

    detector = FaceDetector()

    frame = create_frame()

    result = detector.process_frame(
        frame
    )

    assert result is not None
    assert hasattr(
        result,
        "multi_face_landmarks"
    )

    detector.close()


def test_get_landmarks_without_face() -> None:
    """Test landmark detection when no face is present."""

    detector = FaceDetector()

    frame = create_frame()

    result = detector.get_landmarks(
        frame
    )

    assert result is None

    detector.close()


def test_get_landmark_point_with_none() -> None:
    """Test getting a landmark from missing landmarks."""

    detector = FaceDetector()

    result = detector.get_landmark_point(
        landmarks=None,
        index=0,
        width=640,
        height=480
    )

    assert result is None

    detector.close()


def test_get_landmark_point_with_invalid_index() -> None:
    """Test getting a landmark with an invalid index."""

    detector = FaceDetector()

    class FakeLandmarks:
        landmark = []

    result = detector.get_landmark_point(
        landmarks=FakeLandmarks(),
        index=0,
        width=640,
        height=480
    )

    assert result is None

    detector.close()


def test_get_key_landmarks_without_landmarks() -> None:
    """Test key landmark extraction without landmarks."""

    detector = FaceDetector()

    result = detector.get_key_landmarks(
        landmarks=None,
        width=640,
        height=480
    )

    assert result == {}

    detector.close()


def test_get_landmark_coordinates_without_landmarks() -> None:
    """Test coordinate conversion without landmarks."""

    detector = FaceDetector()

    result = detector.get_landmark_coordinates(
        landmarks=None,
        width=640,
        height=480
    )

    assert result == []

    detector.close()


def test_draw_key_landmarks() -> None:
    """Test drawing key landmarks."""

    detector = FaceDetector()

    frame = create_frame()

    key_landmarks = {
        "left_eye": (200, 200),
        "right_eye": (300, 200),
        "nose": (250, 250)
    }

    result = detector.draw_key_landmarks(
        frame,
        key_landmarks
    )

    assert result is not None
    assert isinstance(
        result,
        np.ndarray
    )

    assert result.shape == frame.shape

    detector.close()


def test_draw_key_landmarks_with_none() -> None:
    """Test drawing landmarks on a missing frame."""

    detector = FaceDetector()

    result = detector.draw_key_landmarks(
        None,
        {}
    )

    assert result is None

    detector.close()


def test_close() -> None:
    """Test releasing MediaPipe resources."""

    detector = FaceDetector()

    detector.close()

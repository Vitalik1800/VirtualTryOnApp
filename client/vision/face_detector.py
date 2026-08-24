import cv2
import mediapipe as mp
import numpy as np


class FaceDetector:
    """Detects facial landmarks using MediaPipe."""

    KEY_LANDMARKS = {
        "left_eye": 33,
        "right_eye": 263,
        "nose": 1,
        "mouth_left": 61,
        "mouth_right": 291,
        "forehead": 10
    }

    def __init__(self) -> None:
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def _prepare_frame(self, frame):
        """Prepare an OpenCV frame for MediaPipe."""

        if frame is None:
            return None

        return cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

    def process_frame(self, frame):
        """Process a video frame using MediaPipe."""

        rgb_frame = self._prepare_frame(
            frame
        )

        if rgb_frame is None:
            return None

        return self.face_mesh.process(
            rgb_frame
        )

    def get_landmarks(self, frame):
        """Return facial landmarks detected on a frame."""

        results = self.process_frame(
            frame
        )

        if results is None:
            return None

        if results.multi_face_landmarks is None:
            return None

        return results.multi_face_landmarks[0]

    def get_landmark_coordinates(
        self,
        landmarks,
        width: int,
        height: int
    ) -> list[tuple[int, int]]:
        """Convert normalized landmarks to pixel coordinates."""

        if landmarks is None:
            return []

        coordinates = []

        for landmark in landmarks.landmark:
            x = int(
                landmark.x * width
            )

            y = int(
                landmark.y * height
            )

            coordinates.append(
                (x, y)
            )

        return coordinates

    def get_landmark_point(
        self,
        landmarks,
        index: int,
        width: int,
        height: int
    ) -> tuple[int, int] | None:
        """Return a facial landmark as pixel coordinates."""

        if landmarks is None:
            return None

        if index < 0 or index >= len(landmarks.landmark):
            return None

        landmark = landmarks.landmark[index]

        x = int(
            landmark.x * width
        )

        y = int(
            landmark.y * height
        )

        return x, y

    def get_key_landmarks(
        self,
        landmarks,
        width: int,
        height: int
    ) -> dict[str, tuple[int, int]]:
        """Return selected facial landmarks."""

        if landmarks is None:
            return {}

        coordinates = {}

        for name, index in self.KEY_LANDMARKS.items():
            point = self.get_landmark_point(
                landmarks,
                index,
                width,
                height
            )

            if point is not None:
                coordinates[name] = point

        return coordinates

    def draw_key_landmarks(
        self,
        frame,
        key_landmarks: dict[str, tuple[int, int]]
    ) -> np.ndarray:
        """Draw selected facial landmarks on a frame."""

        if frame is None:
            return None

        for _, (x, y) in key_landmarks.items():
            cv2.circle(
                frame,
                (x, y),
                5,
                (0, 255, 0),
                -1
            )

        return frame

    def close(self) -> None:
        """Release MediaPipe resources."""

        self.face_mesh.close()

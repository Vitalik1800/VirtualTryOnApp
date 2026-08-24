import numpy as np

from client.vision.face_detector import FaceDetector


def main() -> None:
    detector = FaceDetector()

    frame = np.zeros(
        (480, 640, 3),
        dtype=np.uint8
    )

    landmarks = detector.get_landmarks(
        frame
    )

    print(
        "Landmarks:",
        landmarks
    )

    detector.close()


if __name__ == "__main__":
    main()

import cv2
import numpy as np

from client.accessories.accessory import Accessory
from client.accessories.accessory_manager import AccessoryManager
from client.accessories.accessory_renderer import AccessoryRenderer


def test():
    manager = AccessoryManager()

    glasses = Accessory(
        name="Classic Glasses",
        category="Glasses",
        file_path="assets/accessories/glasses/glasses_01.png",
        anchor_points=(
            "left_eye",
            "right_eye"
        ),
        scale_factor=1.2,
        rotation_enabled=True
    )

    manager.add_accessory(
        glasses
    )

    manager.select_accessory(
        "Classic Glasses"
    )

    accessory = manager.get_selected_accessory()

    if accessory is None:
        print(
            "Accessory not selected"
        )
        return

    key_landmarks = {
        "left_eye": (328, 217),
        "right_eye": (419, 217),
        "nose": (371, 269),
        "mouth_left": (351, 299),
        "mouth_right": (393, 298),
        "forehead": (374, 163)
    }

    position = manager.calculate_position(
        key_landmarks
    )

    print(
        "Position:",
        position
    )

    frame = np.zeros(
        (480, 640, 3),
        dtype=np.uint8
    )

    renderer = AccessoryRenderer()

    result = renderer.render(
        frame=frame,
        accessory_image=accessory.image,
        center_x=position["center_x"],
        center_y=position["center_y"],
        width=position["width"],
        angle=position["angle"]
    )

    success = cv2.imwrite(
        "rendered_test.png",
        result
    )

    print(
        "Rendering completed:",
        success
    )


if __name__ == "__main__":
    test()

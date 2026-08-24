from client.accessories.accessory import Accessory
from client.accessories.accessory_manager import AccessoryManager
from client.accessories.accessory_scaler import AccessoryScaler


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

    added = manager.add_accessory(
        glasses
    )

    print(
        "Added:",
        added
    )

    selected = manager.select_accessory(
        "Classic Glasses"
    )

    print(
        "Selected:",
        selected
    )

    active_accessory = manager.get_selected_accessory()

    if active_accessory is None:
        return

    print(
        "Active accessory:",
        active_accessory.name
    )

    print(
        "Category:",
        active_accessory.category
    )

    print(
        "Image loaded:",
        active_accessory.image is not None
    )

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

    print(
        "Rotation angle:",
        position["angle"]
    )

    scaler = AccessoryScaler()

    scaled_image = scaler.resize(
        active_accessory.image,
        position["width"]
    )

    if scaled_image is not None:
        print(
            "Original size:",
            active_accessory.image.size
        )

        print(
            "Scaled size:",
            scaled_image.size
        )


if __name__ == "__main__":
    test()
import math

from client.accessories.accessory import Accessory
from client.accessories.accessory_loader import AccessoryLoader

from client.api.accessory_api import AccessoryApi
from pathlib import Path


class AccessoryManager:
    """Manages available and selected virtual accessories."""

    def __init__(self) -> None:
        self.accessories: list[Accessory] = []
        self.selected_accessory: Accessory | None = None

        self.loader = AccessoryLoader()
        self.api = AccessoryApi()

    def add_accessory(
        self,
        accessory: Accessory
    ) -> bool:
        """Add an accessory to the collection."""

        image = self.loader.load(
            accessory.file_path
        )

        if image is None:
            return False

        accessory.image = image

        self.accessories.append(
            accessory
        )

        return True

    def load_accessories(
        self,
        base_path: str = "assets/accessories"
    ) -> None:
        """Load all available accessories."""

        base_directory = Path(
            base_path
        )

        print(
            "Accessories directory:",
            base_directory.resolve()
        )

        categories = {
            "Glasses": (
                "glasses",
                (
                    "left_eye",
                    "right_eye"
                ),
                1.5
            ),
            "Hats": (
                "hats",
                (
                    "forehead",
                ),
                2.0
            ),
            "Masks": (
                "masks",
                (
                    "left_eye",
                    "right_eye",
                    "nose"
                ),
                1.8
            )
        }

        for category, (
            directory_name,
            anchor_points,
            scale_factor
        ) in categories.items():

            directory = (
                base_directory
                / directory_name
            )

            if not directory.exists():
                continue

            for file_path in sorted(
                directory.glob("*.png")
            ):
                accessory = Accessory(
                    name=file_path.stem,
                    category=category,
                    file_path=str(file_path),
                    anchor_points=anchor_points,
                    scale_factor=scale_factor,
                    rotation_enabled=True
                )

                self.add_accessory(
                    accessory
                )

        if self.accessories:
            self.selected_accessory = (
                self.accessories[0]
            )

    def select_accessory(
        self,
        name: str
    ) -> bool:
        """Select an accessory by name."""

        for accessory in self.accessories:
            if accessory.name == name:
                self.selected_accessory = accessory
                return True

        return False

    def select_by_category(
        self,
        category: str
    ) -> bool:
        """Select the first accessory from a category."""

        accessories = self.get_by_category(
            category
        )

        if not accessories:
            return False

        self.selected_accessory = accessories[0]

        return True

    def get_selected_accessory(
        self
    ) -> Accessory | None:
        """Return the currently selected accessory."""

        return self.selected_accessory

    def get_by_category(
        self,
        category: str
    ) -> list[Accessory]:
        """Return accessories from a category."""

        return [
            accessory
            for accessory in self.accessories
            if accessory.category == category
        ]

    def calculate_position(
        self,
        key_landmarks: dict[str, tuple[int, int]]
    ) -> dict[str, float] | None:
        """Calculate accessory position from facial landmarks."""

        accessory = self.get_selected_accessory()

        if accessory is None:
            return None

        required_points = accessory.anchor_points

        if not all(
            point in key_landmarks
            for point in required_points
        ):
            return None

        if accessory.category == "Hats":
            forehead_x, forehead_y = key_landmarks[
                "forehead"
            ]

            left_eye = key_landmarks.get(
                "left_eye"
            )

            right_eye = key_landmarks.get(
                "right_eye"
            )

            if left_eye is None or right_eye is None:
                return None

            left_x, left_y = left_eye
            right_x, right_y = right_eye

            distance = math.sqrt(
                (right_x - left_x) ** 2
                + (right_y - left_y) ** 2
            )

            width = (
                    distance * accessory.scale_factor
            )

            angle = self.calculate_rotation_angle(
                key_landmarks
            )

            return {
                "center_x": forehead_x,
                "center_y": forehead_y - width * 0.5,
                "width": width,
                "angle": angle
            }

        left_eye = key_landmarks["left_eye"]
        right_eye = key_landmarks["right_eye"]

        left_x, left_y = left_eye
        right_x, right_y = right_eye

        center_x = (
            left_x + right_x
        ) / 2

        center_y = (
            left_y + right_y
        ) / 2

        distance = math.sqrt(
            (right_x - left_x) ** 2
            + (right_y - left_y) ** 2
        )

        angle = self.calculate_rotation_angle(
            key_landmarks
        )

        return {
            "center_x": center_x,
            "center_y": center_y,
            "width": distance * accessory.scale_factor,
            "angle": angle
        }

    def calculate_rotation_angle(
        self,
        key_landmarks: dict[str, tuple[int, int]]
    ) -> float:
        """Calculate accessory rotation angle from eye landmarks."""

        left_eye = key_landmarks.get(
            "left_eye"
        )

        right_eye = key_landmarks.get(
            "right_eye"
        )

        if left_eye is None or right_eye is None:
            return 0.0

        dx = right_eye[0] - left_eye[0]
        dy = right_eye[1] - left_eye[1]

        if dx == 0 and dy == 0:
            return 0.0

        angle = math.degrees(
            math.atan2(
                dy,
                dx
            )
        )

        return angle

    def select_next_by_category(
        self,
        category: str
    ) -> bool:
        """Select the next accessory from a category."""

        accessories = self.get_by_category(
            category
        )

        if not accessories:
            return False

        if self.selected_accessory not in accessories:
            self.selected_accessory = accessories[0]
            return True

        current_index = accessories.index(
            self.selected_accessory
        )

        next_index = (
            current_index + 1
        ) % len(accessories)

        self.selected_accessory = (
            accessories[next_index]
        )

        return True

    def load_database_ids(self) -> None:
        """Load database IDs for local accessories."""

        accessories = self.api.get_accessories()

        accessory_ids = {
            (
                accessory["category"],
                accessory["name"]
            ): accessory["id"]
            for accessory in accessories
        }

        for accessory in self.accessories:
            key = (
                accessory.category,
                accessory.name
            )

            accessory.id = accessory_ids.get(
                key
            )

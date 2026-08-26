import math

from PIL import Image

from client.accessories.accessory import Accessory
from client.accessories.accessory_manager import AccessoryManager


def create_accessory(
    name: str = "test_glasses",
    category: str = "Glasses"
) -> Accessory:
    """Create a test accessory."""

    return Accessory(
        name=name,
        category=category,
        file_path="test.png",
        anchor_points=(
            "left_eye",
            "right_eye"
        ),
        scale_factor=1.5,
        rotation_enabled=True
    )


def test_add_accessory() -> None:
    """Test adding an accessory."""

    manager = AccessoryManager()

    manager.loader.load = lambda _: Image.new(
        "RGBA",
        (100, 100)
    )

    accessory = create_accessory()

    result = manager.add_accessory(
        accessory
    )

    assert result is True
    assert len(manager.accessories) == 1
    assert manager.accessories[0] is accessory
    assert accessory.image is not None


def test_select_accessory() -> None:
    """Test selecting an accessory by name."""

    manager = AccessoryManager()

    first = create_accessory(
        name="glasses_1"
    )

    second = create_accessory(
        name="glasses_2"
    )

    manager.accessories.extend(
        [first, second]
    )

    result = manager.select_accessory(
        "glasses_2"
    )

    assert result is True
    assert manager.get_selected_accessory() is second


def test_select_unknown_accessory() -> None:
    """Test selecting an unknown accessory."""

    manager = AccessoryManager()

    accessory = create_accessory()

    manager.accessories.append(
        accessory
    )

    result = manager.select_accessory(
        "unknown"
    )

    assert result is False


def test_get_by_category() -> None:
    """Test filtering accessories by category."""

    manager = AccessoryManager()

    glasses = create_accessory(
        name="glasses",
        category="Glasses"
    )

    hat = Accessory(
        name="hat",
        category="Hats",
        file_path="hat.png",
        anchor_points=("forehead",),
        scale_factor=2.0,
        rotation_enabled=True
    )

    manager.accessories.extend(
        [glasses, hat]
    )

    result = manager.get_by_category(
        "Glasses"
    )

    assert len(result) == 1
    assert result[0] is glasses


def test_select_by_category() -> None:
    """Test selecting the first accessory from a category."""

    manager = AccessoryManager()

    glasses = create_accessory(
        name="glasses"
    )

    manager.accessories.append(
        glasses
    )

    result = manager.select_by_category(
        "Glasses"
    )

    assert result is True
    assert manager.get_selected_accessory() is glasses


def test_select_by_empty_category() -> None:
    """Test selecting an empty category."""

    manager = AccessoryManager()

    result = manager.select_by_category(
        "Masks"
    )

    assert result is False


def test_calculate_position() -> None:
    """Test accessory position calculation."""

    manager = AccessoryManager()

    accessory = create_accessory()

    manager.selected_accessory = accessory

    landmarks = {
        "left_eye": (100, 200),
        "right_eye": (200, 200)
    }

    position = manager.calculate_position(
        landmarks
    )

    assert position is not None

    assert position["center_x"] == 150
    assert position["center_y"] == 200
    assert position["width"] == 150
    assert position["angle"] == 0


def test_calculate_position_with_rotation() -> None:
    """Test position calculation for a rotated face."""

    manager = AccessoryManager()

    accessory = create_accessory()

    manager.selected_accessory = accessory

    landmarks = {
        "left_eye": (100, 200),
        "right_eye": (200, 250)
    }

    position = manager.calculate_position(
        landmarks
    )

    assert position is not None

    excepted_angle = math.degrees(
        math.atan2(50, 100)
    )

    assert math.isclose(
        position["angle"],
        excepted_angle
    )


def test_calculate_position_without_landmarks() -> None:
    """Test position calculation without required landmarks."""

    manager = AccessoryManager()

    accessory = create_accessory()

    manager.selected_accessory = accessory

    landmarks = {
        "left_eye": (100, 200)
    }

    position = manager.calculate_position(
        landmarks
    )

    assert position is None

import numpy as np
from PIL import Image

from client.accessories.accessory_renderer import AccessoryRenderer


def create_frame(
    width: int = 640,
    height: int = 480
) -> np.ndarray:
    """Create a test camera frame."""

    return np.zeros(
        (height, width, 3),
        dtype=np.uint8
    )


def create_accessory_image(
    width: int = 100,
    height: int = 50
) -> Image.Image:
    """Create a test accessory image."""

    return Image.new(
        "RGBA",
        (width, height),
        (255, 255, 255, 255)
    )


def test_render_returns_frame() -> None:
    """Test rendering an accessory onto a frame."""

    renderer = AccessoryRenderer()

    frame = create_frame()
    accessory_image = create_accessory_image()

    result = renderer.render(
        frame=frame,
        accessory_image=accessory_image,
        center_x=320,
        center_y=240,
        width=150,
        angle=0.0
    )

    assert result is not None
    assert isinstance(
        result,
        np.ndarray
    )


def test_render_preserves_frame_dimensions() -> None:
    """Test that rendering preserves frame dimensions."""

    renderer = AccessoryRenderer()

    frame = create_frame(
        width=640,
        height=480
    )

    accessory_image = create_accessory_image()

    result = renderer.render(
        frame=frame,
        accessory_image=accessory_image,
        center_x=320,
        center_y=240,
        width=150,
        angle=0.0
    )

    assert result.shape == frame.shape


def test_render_changes_frame() -> None:
    """Test that rendering returns a valid processed frame."""

    renderer = AccessoryRenderer()

    frame = create_frame()
    accessory_image = create_accessory_image()

    result = renderer.render(
        frame=frame,
        accessory_image=accessory_image,
        center_x=320,
        center_y=240,
        width=150,
        angle=0.0
    )

    assert result is not None
    assert isinstance(
        result,
        np.ndarray
    )

    assert result.shape == frame.shape
    assert result.dtype == frame.dtype


def test_render_with_rotation() -> None:
    """Test rendering a rotated accessory."""

    renderer = AccessoryRenderer()

    frame = create_frame()
    accessory_image = create_accessory_image()

    result = renderer.render(
        frame=frame,
        accessory_image=accessory_image,
        center_x=320,
        center_y=240,
        width=150,
        angle=15.0
    )

    assert result is not None
    assert result.shape == frame.shape


def test_render_with_none_image() -> None:
    """Test rendering without an accessory image."""

    renderer = AccessoryRenderer()

    frame = create_frame()

    result = renderer.render(
        frame=frame,
        accessory_image=None,
        center_x=320,
        center_y=240,
        width=150,
        angle=0.0
    )

    assert result is not None
    assert result.shape == frame.shape


def test_render_outside_frame() -> None:
    """Test rendering when the accessory is outside the frame."""

    renderer = AccessoryRenderer()

    frame = create_frame()
    accessory_image = create_accessory_image()

    result = renderer.render(
        frame=frame,
        accessory_image=accessory_image,
        center_x=-100,
        center_y=-100,
        width=150,
        angle=0.0
    )

    assert result is not None
    assert result.shape == frame.shape

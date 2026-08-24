from PIL import Image


class Accessory:
    """Represents a virtual accessory."""

    def __init__(
        self,
        name: str,
        category: str,
        file_path: str,
        anchor_points: tuple[str, ...],
        scale_factor: float,
        rotation_enabled: bool,
        accessory_id: int | None = None
    ) -> None:
        self.id = accessory_id
        self.name = name
        self.category = category
        self.file_path = file_path
        self.anchor_points = anchor_points
        self.scale_factor = scale_factor
        self.rotation_enabled = rotation_enabled
        self.image: Image.Image | None = None

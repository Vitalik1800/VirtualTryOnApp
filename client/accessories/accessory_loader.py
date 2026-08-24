from pathlib import Path

from PIL import Image


class AccessoryLoader:
    """Loads accessory images from files."""

    def __init__(self) -> None:
        self.project_root = Path(__file__).resolve().parents[2]

    def load(
        self,
        file_path: str
    ) -> Image.Image | None:
        """Load an accessory image."""

        path = Path(file_path)

        if not path.is_absolute():
            path = self.project_root / path

        if not path.exists():
            print(
                f"Accessory image not found: {path}"
            )
            return None

        try:
            image = Image.open(path)

            return image.convert("RGBA")

        except (OSError, ValueError) as error:
            print(
                f"Accessory image not found: {error}"
            )
            return None

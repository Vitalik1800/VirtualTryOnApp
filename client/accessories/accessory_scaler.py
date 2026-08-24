from PIL import Image


class AccessoryScaler:
    """Calculates and applies accessory scaling."""

    def calculate_size(
        self,
        image: Image.Image,
        target_width: float
    ) -> tuple[int, int]:
        """Calculate new image size while preserving aspect ratio."""

        if image.width <= 0:
            return 0, 0

        scale = (
            target_width / image.width
        )

        target_height = (
            image.height * scale
        )

        return (
            max(1, int(target_width)),
            max(1, int(target_height))
        )

    def resize(
        self,
        image: Image.Image,
        target_width: float
    ) -> Image.Image | None:
        """Resize an accessory image."""

        if image is None:
            return None

        width, height = self.calculate_size(
            image,
            target_width
        )

        if width <= 0 or height <= 0:
            return None

        return image.resize(
            (width, height),
            Image.Resampling.LANCZOS
        )

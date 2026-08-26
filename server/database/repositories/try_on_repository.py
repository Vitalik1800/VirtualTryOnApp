from sqlalchemy.orm import Session

from server.models.try_on import TryOn


class TryOnRepository:
    """Provides database operations for virtual try-on."""

    def __init__(
        self,
        db: Session
    ) -> None:
        self.db = db

    def save(
        self,
        accessory_name: str,
        category: str,
        center_x: float,
        center_y: float,
        width: float,
        angle: float
    ) -> TryOn:
        """Save a virtual try-on result."""

        try_on = TryOn(
            accessory_name=accessory_name,
            category=category,
            center_x=center_x,
            center_y=center_y,
            width=width,
            angle=angle
        )

        self.db.add(
            try_on
        )

        self.db.commit()

        self.db.refresh(
            try_on
        )

        return try_on

from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from server.database.base import Base


class TryOn(Base):
    """Database model for a virtual try-on."""

    __tablename__ = "try_ons"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    accessory_id: Mapped[int] = mapped_column(
        ForeignKey("accessories.id"),
        nullable=False
    )

    center_x: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    center_y: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    width: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    angle: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

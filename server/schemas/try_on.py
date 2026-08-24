from pydantic import BaseModel


class TryOnCreate(BaseModel):
    """Request schema for creating a try-on record."""

    accessory_id: int
    center_x: float
    center_y: float
    width: float
    angle: float
    
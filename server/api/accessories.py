from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from server.database.connection import get_db
from server.models.accessory import Accessory


router = APIRouter(
    prefix="/accessories",
    tags=["Accessories"]
)


@router.get("/")
def get_accessories(
    db: Session = Depends(get_db)
) -> list[dict]:
    """Return all active accessories."""

    statement = select(Accessory).where(
        Accessory.is_active.is_(True)
    )

    accessories = db.scalars(statement).all()

    return [
        {
            "id": accessory.id,
            "name": accessory.name,
            "category": accessory.category,
            "file_path": accessory.file_path
        }
        for accessory in accessories
    ]

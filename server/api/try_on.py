from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from server.database.connection import get_db
from server.models.accessory import Accessory
from server.models.try_on import TryOn


router = APIRouter(
    prefix="/try-on",
    tags=["Try-On"]
)


@router.post("/")
def save_try_on(
    data: dict,
    db: Session = Depends(get_db)
) -> dict:
    """Save a virtual try-on."""

    accessory_id = data.get("accessory_id")

    accessory = db.get(
        Accessory,
        accessory_id
    )

    if accessory is None:
        raise HTTPException(
            status_code=404,
            detail="Accessory not found"
        )

    try_on = TryOn(
        accessory_id=accessory_id,
        center_x=data["center_x"],
        center_y=data["center_y"],
        width=data["width"],
        angle=data["angle"]
    )

    db.add(try_on)
    db.commit()
    db.refresh(try_on)

    return {
        "id": try_on.id,
        "accessory_id": try_on.accessory_id,
        "center_x": try_on.center_x,
        "center_y": try_on.center_y,
        "width": try_on.width,
        "angle": try_on.angle
    }


@router.get("/")
def get_try_ons(
    db: Session = Depends(get_db)
) -> list[dict]:
    """Return all saved virtual try-ons."""

    statement = (
        select(TryOn, Accessory)
        .join(
            Accessory,
            TryOn.accessory_id == Accessory.id
        )
        .order_by(
            TryOn.id.desc()
        )
    )

    results = db.execute(
        statement
    ).all()

    return [
        {
            "id": try_on.id,
            "accessory_id": try_on.accessory_id,
            "accessory_name": accessory.name,
            "category": accessory.category,
            "center_x": try_on.center_x,
            "center_y": try_on.center_y,
            "width": try_on.width,
            "angle": try_on.angle
        }
        for try_on, accessory in results
    ]

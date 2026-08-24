from sqlalchemy import select

from server.database.connection import SessionLocal
from server.models.accessory import Accessory


INITIAL_ACCESSORIES = [
    {
        "name": "Classic Glasses",
        "category": "Glasses",
        "file_path": "assets/accessories/glasses/glasses_01.png"
    },
    {
        "name": "Modern Glasses",
        "category": "Glasses",
        "file_path": "assets/accessories/glasses/glasses_02.png"
    },
    {
        "name": "Classic Hat",
        "category": "Hats",
        "file_path": "assets/accessories/hats/hat_01.png"
    },
    {
        "name": "Modern Hat",
        "category": "Hats",
        "file_path": "assets/accessories/hats/hat_02.png"
    },
    {
        "name": "Classic Mask",
        "category": "Masks",
        "file_path": "assets/accessories/masks/mask_01.png"
    },
    {
        "name": "Modern Mask",
        "category": "Masks",
        "file_path": "assets/accessories/masks/mask_02.png"
    }
]


def seed_accessories() -> None:
    """Add initial accessories to the database."""

    db = SessionLocal()

    try:
        for data in INITIAL_ACCESSORIES:
            statement = select(Accessory).where(
                Accessory.name == data["name"]
            )

            existing_accessory = db.scalar(statement)

            if existing_accessory is None:
                accessory = Accessory(
                    name=data["name"],
                    category=data["category"],
                    file_path=data["file_path"],
                    is_active=True
                )

                db.add(accessory)

        db.commit()

    finally:
        db.close()


if __name__ == "__main__":
    seed_accessories()
    print("Initial accessories added successfully.")

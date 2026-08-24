from pathlib import Path

from sqlalchemy import select

from server.database.base import Base
from server.database.connection import SessionLocal, engine
from server.models.accessory import Accessory


def seed_accessories() -> None:
    """Populate the accessories table."""

    Base.metadata.create_all(
        bind=engine
    )

    project_root = Path(__file__).resolve().parents[2]

    accessories_directory = (
        project_root
        / "assets"
        / "accessories"
    )

    categories = {
        "Glasses": "glasses",
        "Hats": "hats",
        "Masks": "masks"
    }

    db = SessionLocal()

    try:
        for category, directory_name in categories.items():
            directory = (
                accessories_directory
                / directory_name
            )

            if not directory.exists():
                print(
                    f"Directory not found: {directory}"
                )
                continue

            for file_path in sorted(
                directory.glob("*.png")
            ):
                name = file_path.stem

                existing = db.scalar(
                    select(Accessory).where(
                        Accessory.name == name,
                        Accessory.category == category
                    )
                )

                if existing is not None:
                    continue

                accessory = Accessory(
                    name=name,
                    category=category,
                    file_path=str(
                        file_path.relative_to(
                            project_root
                        )
                    ),
                    is_active=True
                )

                db.add(accessory)

        db.commit()

        print(
            "Accessories seeded successfully."
        )

    finally:
        db.close()


if __name__ == "__main__":
    seed_accessories()

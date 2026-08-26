from fastapi.testclient import TestClient
from sqlalchemy import select

from server.database.base import Base
from server.database.connection import SessionLocal, engine
from server.main import app
from server.models.accessory import Accessory
from server.models.try_on import TryOn


client = TestClient(app)


def setup_database() -> None:
    """Create database tables."""

    Base.metadata.create_all(
        bind=engine
    )


def create_accessory() -> int:
    """Create an accessory for integration testing."""

    db = SessionLocal()

    try:
        accessory = Accessory(
            name="api_sqlite_test_glasses",
            category="Glasses",
            file_path="assets/accessories/glasses/test.png",
            is_active=True
        )

        db.add(accessory)
        db.commit()
        db.refresh(accessory)

        return accessory.id

    finally:
        db.close()


def test_accessories_api_reads_from_sqlite() -> None:
    """Test that the accessories API reads data from SQLite."""

    setup_database()

    accessory_id = create_accessory()

    response = client.get(
        "/accessories/"
    )

    assert response.status_code == 200

    accessories = response.json()

    accessory = next(
        (
            item
            for item in accessories
            if item["id"] == accessory_id
        ),
        None
    )

    assert accessory is not None

    assert accessory["name"] == (
        "api_sqlite_test_glasses"
    )

    assert accessory["category"] == "Glasses"

    assert accessory["file_path"] == (
        "assets/accessories/glasses/test.png"
    )


def test_try_on_api_saves_data_to_sqlite() -> None:
    """Test that the try-on API stores data in SQLite."""

    setup_database()

    accessory_id = create_accessory()

    response = client.post(
        "/try-on/",
        json={
            "accessory_id": accessory_id,
            "center_x": 320.0,
            "center_y": 240.0,
            "width": 180.0,
            "angle": 5.0
        }
    )

    assert response.status_code == 200

    data = response.json()

    try_on_id = data["id"]

    db = SessionLocal()

    try:
        statement = select(TryOn).where(
            TryOn.id == try_on_id
        )

        try_on = db.scalar(
            statement
        )

        assert try_on is not None

        assert try_on.accessory_id == (
            accessory_id
        )

        assert try_on.center_x == 320.0
        assert try_on.center_y == 240.0
        assert try_on.width == 180.0
        assert try_on.angle == 5.0

    finally:
        db.close()


def test_api_and_sqlite_use_same_accessory() -> None:
    """Test consistency between API and SQLite data."""

    setup_database()

    accessory_id = create_accessory()

    response = client.get(
        "/accessories/"
    )

    assert response.status_code == 200

    accessories = response.json()

    api_accessory = next(
        (
            item
            for item in accessories
            if item["id"] == accessory_id
        ),
        None
    )

    assert api_accessory is not None

    db = SessionLocal()

    try:
        statement = select(Accessory).where(
            Accessory.id == accessory_id
        )

        database_accessory = db.scalar(
            statement
        )

        assert database_accessory is not None

        assert api_accessory["id"] == (
            database_accessory.id
        )

        assert api_accessory["name"] == (
            database_accessory.name
        )

        assert api_accessory["category"] == (
            database_accessory.category
        )

        assert api_accessory["file_path"] == (
            database_accessory.file_path
        )

    finally:
        db.close()
        
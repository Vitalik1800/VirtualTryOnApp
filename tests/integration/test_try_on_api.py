from fastapi.testclient import TestClient
from sqlalchemy import select

from server.database.base import Base
from server.database.connection import SessionLocal, engine
from server.main import app
from server.models.accessory import Accessory
from server.models.try_on import TryOn


client = TestClient(app)


def create_accessory() -> int:
    """Create a test accessory in the database."""

    db = SessionLocal()

    try:
        accessory = Accessory(
            name="integration_test_glasses",
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


def test_save_try_on() -> None:
    """Test saving a virtual try-on through the API."""

    Base.metadata.create_all(
        bind=engine
    )

    accessory_id = create_accessory()

    response = client.post(
        "/try-on/",
        json={
            "accessory_id": accessory_id,
            "center_x": 320.0,
            "center_y": 240.0,
            "width": 180.0,
            "angle": 0.0
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert data["accessory_id"] == accessory_id

    db = SessionLocal()

    try:
        statement = select(TryOn).where(
            TryOn.id == data["id"]
        )

        try_on = db.scalar(
            statement
        )

        assert try_on is not None
        assert try_on.accessory_id == accessory_id
        assert try_on.center_x == 320.0
        assert try_on.center_y == 240.0
        assert try_on.width == 180.0
        assert try_on.angle == 0.0

    finally:
        db.close()
        
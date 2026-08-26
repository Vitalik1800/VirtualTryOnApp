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


def create_test_accessory() -> int:
    """Create an accessory for system testing."""

    db = SessionLocal()

    try:
        accessory = Accessory(
            name="system_test_glasses",
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


def test_full_try_on_scenario() -> None:
    """Test the complete virtual try-on scenario."""

    setup_database()

    accessory_id = create_test_accessory()

    # 1. Get available accessories.
    accessories_response = client.get(
        "/accessories/"
    )

    assert accessories_response.status_code == 200

    accessories = accessories_response.json()

    selected_accessory = next(
        (
            accessory
            for accessory in accessories
            if accessory["id"] == accessory_id
        ),
        None
    )

    assert selected_accessory is not None

    assert selected_accessory["category"] == (
        "Glasses"
    )

    # 2. Simulate detected face landmarks.
    left_eye = (240, 220)
    right_eye = (400, 220)

    center_x = (
        left_eye[0] + right_eye[0]
    ) / 2

    center_y = (
        left_eye[1] + right_eye[1]
    ) / 2

    width = (
        (
            (right_eye[0] - left_eye[0]) ** 2
            + (right_eye[1] - left_eye[1]) ** 2
        ) ** 0.5
    ) * 1.5

    angle = 0.0

    # 3. Save the virtual try-on.
    try_on_response = client.post(
        "/try-on/",
        json={
            "accessory_id": accessory_id,
            "center_x": center_x,
            "center_y": center_y,
            "width": width,
            "angle": angle
        }
    )

    assert try_on_response.status_code == 200

    try_on_data = try_on_response.json()

    assert "id" in try_on_data

    assert try_on_data["accessory_id"] == (
        accessory_id
    )

    # 4. Verify the result in SQLite.
    db = SessionLocal()

    try:
        statement = select(TryOn).where(
            TryOn.id == try_on_data["id"]
        )

        try_on = db.scalar(
            statement
        )

        assert try_on is not None

        assert try_on.accessory_id == (
            accessory_id
        )

        assert try_on.center_x == center_x
        assert try_on.center_y == center_y
        assert try_on.width == width
        assert try_on.angle == angle

    finally:
        db.close()

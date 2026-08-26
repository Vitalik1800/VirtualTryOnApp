import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from server.database.base import Base
from server.database.connection import get_db
from server.main import app
from server.models.accessory import Accessory

TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def override_get_db():
    """Provide a test database session."""

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[
    get_db
] = override_get_db

client = TestClient(
    app
)


@pytest.fixture(autouse=True)
def setup_database():
    """Create and clear the test database."""

    Base.metadata.create_all(
        bind=engine
    )

    db = TestingSessionLocal()

    try:
        db.query(Accessory).delete()

        db.add_all(
            [
                Accessory(
                    name="test_glasses",
                    category="Glasses",
                    file_path="assets/accessories/glasses/test_glasses.png",
                    is_active=True
                ),
                Accessory(
                    name="test_hat",
                    category="Hats",
                    file_path="assets/accessories/hats/test_hat.png",
                    is_active=True
                ),
                Accessory(
                    name="inactive_mask",
                    category="Masks",
                    file_path="assets/accessories/masks/inactive_mask.png",
                    is_active=False
                )
            ]
        )

        db.commit()

    finally:
        db.close()

    yield

    Base.metadata.drop_all(
        bind=engine
    )


def test_get_accessories() -> None:
    """Test retrieving active accessories."""

    response = client.get(
        "/accessories/"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(
        data,
        list
    )

    assert len(data) == 2

    names = {
        accessory["name"]
        for accessory in data
    }

    assert names == {
        "test_glasses",
        "test_hat"
    }


def test_get_accessories_contains_required_fields() -> None:
    """Test accessory response fields."""

    response = client.get(
        "/accessories/"
    )

    assert response.status_code == 200

    data = response.json()

    for accessory in data:
        assert "id" in accessory
        assert "name" in accessory
        assert "category" in accessory
        assert "file_path" in accessory


def test_inactive_accessories_are_not_returned() -> None:
    """Test that inactive accessories are excluded."""

    response = client.get(
        "/accessories/"
    )

    assert response.status_code == 200

    data = response.json()

    categories = [
        accessory["category"]
        for accessory in data
    ]

    assert "Masks" not in categories


def test_save_try_on() -> None:
    """Test saving a virtual try-on."""

    response = client.post(
        "/try-on/",
        json={
            "accessory_id": 1,
            "center_x": 320.0,
            "center_y": 240.0,
            "width": 150.0,
            "angle": 0.0
        }
    )

    assert response.status_code in (
        200,
        201
    )

    data = response.json()

    assert "id" in data

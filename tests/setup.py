import pytest
from datetime import datetime
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import Session, sessionmaker
from fastapi.testclient import TestClient
from app.models import Base
from app.models.track import Track
from app.models.meeting import Meeting
from app.models.horse import Horse

from app.main import app
from app.db.session import get_db


@pytest.fixture(scope="module")
def test_db():
    try:
        engine = create_engine("sqlite:///:memory:")
        SessionLocal = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)
        session = SessionLocal()
        yield session
    finally:
        session.close()


@pytest.fixture(scope="session")
def test_client():
    app.dependency_overrides[get_db] = test_db
    client = TestClient(app=app)
    yield client


@pytest.fixture(scope="module")
def track_data(test_db: Session):

    tracks = test_db.execute(
        insert(Track).returning(Track), [
            {"track_id": 100, "name": "Track Name",
                "location": "L", "state": "QLD"}
        ]
    )

    yield tracks.scalars().first()


@pytest.fixture(scope="module")
def meeting_data(test_db: Session, track_data):

    meetings = test_db.execute(
        insert(Meeting).returning(Meeting), [
            {"track_id": track_data.id, "track_surface": "G",
                "date": datetime.strptime("2023-01-01", "%Y-%m-%d")}
        ]
    )

    yield meetings.scalars().first()


@pytest.fixture(scope="module")
def horse_data(test_db: Session):
    horses = test_db.execute(
        insert(Horse).returning(Horse), [
            {"horse_id": "98765", "horse_name": "Silver"}
        ]
    )

    yield horses.scalars().first()

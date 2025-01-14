import pytest
from datetime import datetime
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import Session, sessionmaker
from fastapi.testclient import TestClient
from app.models import Base
from app.models.track import Track
from app.models.meeting import Meeting
from app.models.horse import Horse
from app.models.race import Race
from app.models.horse_race_info import HorseRaceInfo
from app.models.horse_race_stats import HorseRaceStats

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
def race_data(test_db: Session, meeting_data: Meeting):

    races = test_db.execute(
        insert(Race).returning(Race), [
            {
                "race_id": "12345",
                "name": "Race 12345",
                "date_time": datetime.strptime("31/01/2023 12:30pm", "%d/%m/%Y %I:%M%p"),
                "race_number": 1,
                "distance": 1500,
                "meeting_id": meeting_data.id
            }
        ]
    )

    yield races.scalars().first()


@pytest.fixture(scope="module")
def horse_data(test_db: Session):
    horses = test_db.execute(
        insert(Horse).returning(Horse), [
            {"horse_id": "98765", "horse_name": "Silver"}
        ]
    )

    yield horses.scalars().first()


@pytest.fixture(scope="module")
def horse_race_info_data(test_db: Session, horse_data: Horse, race_data: Race):
    infos = test_db.execute(
        insert(HorseRaceInfo).returning(HorseRaceInfo), [
            {
                "race_id": race_data.id,
                "horse_id": horse_data.id,
                "colours": "red",
                "colours_pic": "red.png",
                "trainer": "Trainer Name",
                "jockey": "Jockey Name",
                "barrier": 1,
                "last_starts": "1x1x1"
            }
        ]
    )

    yield infos.scalars().first()


@pytest.fixture(scope="module")
def horse_race_stats_data(test_db: Session, horse_data: Horse, race_data: Race):
    stats = test_db.execute(
        insert(HorseRaceStats).returning(HorseRaceStats), [
            {
                "race_id": race_data.id,
                "horse_id": horse_data.id,
                "stat": "distance",
                "first": 1,
                "second": 0,
                "third": 0,
                "win_ratio": 1
            }
        ]
    )

    yield stats.scalars().first()

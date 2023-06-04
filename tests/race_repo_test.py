from datetime import datetime
from app import repositories as repo
from app.schemas.race import RaceCreate, Race, RaceData
from app import models

from .setup import test_db, track_data, meeting_data, race_data


def test_can_create_race(test_db, meeting_data):
    race = repo.race.create(db=test_db, race_in=RaceCreate(
        race_id="98765",
        name="Race 98765",
        date_time=datetime.strptime("31/12/2023 10:30am", "%d/%m/%Y %I:%M%p"),
        race_number=9,
        distance=900,
        meeting_id=meeting_data.id
    ))

    assert race is not None
    assert isinstance(race, Race)


def test_can_get_race(test_db, race_data: models.Race):
    race = repo.race.get_race(
        db=test_db, race_number=race_data.race_number, meeting_id=race_data.meeting_id)

    assert race is not None
    assert isinstance(race, Race)


def test_can_update_race(test_db, race_data: models.Race):
    updated_race = repo.race.update_race(db=test_db, id=race_data.id, race_data=RaceData(
        race_id=race_data.race_id,
        name="Updated Race",
        date_time=datetime.strptime("01/06/2023 9:30am", "%d/%m/%Y %I:%M%p"),
        race_number=race_data.race_number,
        distance=1000,
        meeting_id=race_data.meeting_id
    ))

    assert updated_race is not None
    assert isinstance(updated_race, Race)
    assert updated_race.name == "Updated Race"
    assert updated_race.date_time.strftime(
        "%d/%m/%Y %I:%M%p") == "01/06/2023 09:30AM"

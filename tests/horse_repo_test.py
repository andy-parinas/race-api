
from app.schemas.horse import HorseData, Horse
from app import repositories as repo
from app import models
from .setup import test_db, horse_data


def test_can_create_horse(test_db):
    horse = repo.horse.create(db=test_db, horse_in=HorseData(
        horse_id="12345",
        horse_name="My Little Pony"
    ))

    assert horse is not None
    assert isinstance(horse, Horse)


def test_can_get_horse(test_db, horse_data):
    horse = repo.horse.get_horse_from_horse_id(
        test_db, horse_id=horse_data.horse_id)

    assert horse is not None
    assert isinstance(horse, Horse)


def test_can_update_horse(test_db, horse_data: models.Horse):
    updated_horse = repo.horse.update_horse(db=test_db, id=horse_data.id, horse_data=HorseData(
        horse_id="54321",
        horse_name="Updated"
    ))

    assert updated_horse is not None
    assert isinstance(updated_horse, Horse)
    assert updated_horse.horse_id == "54321"
    assert updated_horse.horse_name == "Updated"

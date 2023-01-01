from sqlalchemy.orm import Session

from app.models.race import Race
from app.schemas.race import RaceCreate


class RaceRepository:
    def __int__(self):
        self.race = race

    def create(self, db: Session, race_in: RaceCreate) -> Race:
        db_obj = Race(**race_in)
        db.add(db_obj)
        db.commit()
        return db_obj


race = RaceRepository()

from sqlalchemy.orm import Session

from app.models.race import Race
from app.schemas.race import RaceCreate


class RaceRepository:

    def create(self, db: Session, race_in: RaceCreate) -> Race:
        race_obj = race_in.dict()
        db_obj = Race(**race_obj)
        db.add(db_obj)
        db.commit()
        return db_obj


race = RaceRepository()

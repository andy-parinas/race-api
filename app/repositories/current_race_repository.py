from sqlalchemy.orm import Session

from app.schemas.current_race import CurrentRaceCreate
from app.models.current_race import CurrentRace


class CurrentRaceRepository:

    def create(self, db: Session, current_race_in: CurrentRaceCreate):
        db_obj = CurrentRace(**current_race_in)
        db.add(db_obj)
        db.commit()
        return db_obj


current_race = CurrentRaceRepository()

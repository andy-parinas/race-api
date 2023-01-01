from sqlalchemy.orm import Session

from app.models.horse import Horse
from app.schemas.horse import HorseCreate


class HorseRepository:

    def create(self, db: Session, horse_in: HorseCreate):
        db_obj = Horse(**horse_in)
        db.add(db_obj)
        db.commit()
        return db_obj


horse = HorseRepository()

from sqlalchemy.orm import Session

from app.models.horse import Horse
from app.schemas.horse import HorseCreate


class HorseRepository:

    def create(self, db: Session, obj_in: HorseCreate):
        horse_obj = obj_in.dict()
        db_obj = Horse(**horse_obj)
        db.add(db_obj)
        db.commit()
        return db_obj


horse = HorseRepository()

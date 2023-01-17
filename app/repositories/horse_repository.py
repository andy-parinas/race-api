from typing import List
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

    def get_horses_from_ids(self, db: Session, ids: List[int]) ->List[Horse]:
        horses = db.query(Horse).filter(Horse.id.in_(ids)).all()
        return horses


horse = HorseRepository()

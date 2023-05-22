from typing import List
from sqlalchemy.orm import Session, joinedload

from app.models.horse import Horse
from app.models.race import Race
from app.schemas.horse import HorseCreate


class HorseRepository:

    def create(self, db: Session, obj_in: HorseCreate):
        horse_obj = obj_in.dict()
        db_obj = Horse(**horse_obj)
        db.add(db_obj)
        db.commit()
        return db_obj

    def get_horses_from_ids(self, db: Session, ids: List[int]) ->List[Horse]:
        # horses = db.query(Horse).filter(Horse.id.in_(ids)).all()
        horses = db.query(Horse).options(joinedload(Horse.race).joinedload(Race.meeting)).filter(Horse.id.in_(ids)).all()
        return horses

    def get_horse_from_horse_id(self, db: Session, horse_id: str) -> Horse:
        horse = db.query(Horse).filter(Horse.horse_id == horse_id).first()
        return horse

horse = HorseRepository()

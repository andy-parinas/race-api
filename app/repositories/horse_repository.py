from typing import List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, update

from app.models.horse import Horse
from app.models.race import Race
from app.schemas.horse import HorseCreate, HorseData, Horse as HorseSchema


class HorseRepository:

    def create(self, db: Session, horse_in: HorseData):
        horse_obj = horse_in.dict()
        db_obj = Horse(**horse_obj)
        db.add(db_obj)
        db.commit()
        return HorseSchema.from_orm(db_obj)

    def get_horses_from_ids(self, db: Session, ids: List[int]) -> List[Horse]:
        # horses = db.query(Horse).filter(Horse.id.in_(ids)).all()
        horses = db.query(Horse).options(joinedload(Horse.race).joinedload(
            Race.meeting)).filter(Horse.id.in_(ids)).all()
        return horses

    def get_horse_from_horse_id(self, db: Session, horse_id: str) -> Horse:

        stmt = select(Horse).where(Horse.horse_id == horse_id)

        horse = db.scalars(stmt).first()

        if not horse:
            return None

        return HorseSchema.from_orm(horse)

    def update_horse(self, db: Session, id: int, horse_data: HorseData):
        stmt = (update(Horse).returning(Horse)
                .where(Horse.id == id)
                .values(horse_id=horse_data.horse_id, horse_name=horse_data.horse_name)
                )

        horse = db.scalars(stmt).first()

        return HorseSchema.from_orm(horse)


horse = HorseRepository()

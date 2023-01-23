from typing import List
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

    def get_race_list(self, db: Session, *, 
        meeting_ids: List[int]|None = None,
        skip: int = 0,
        limit: int = 0,
    ) -> List[Race]:

        query = db.query(Race)

        if meeting_ids:
            query = query.filter(Race.meeting_id.in_(meeting_ids))

        return query.order_by(Race.race_number).offset(skip).limit(limit).all()

    def get_race_by_id(self, db: Session, *, race_id:int) -> Race:
        return db.query(Race).filter(Race.id == race_id).first()

race = RaceRepository()

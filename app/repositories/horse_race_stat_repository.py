from typing import List
from sqlalchemy.orm import Session, joinedload

from app.models.horse_race_stats import HorseRaceStats
from app.schemas.horse_race_stats import HorseRaceStatsCreate


class HorseRaceStatsRepository:

    """
    Create HorseRaceStat
    """
    def create(self, db: Session, data_in: HorseRaceStatsCreate) -> HorseRaceStats:
        data_obj = data_in.dict()
        db_obj = HorseRaceStats(**data_obj)
        db.add(db_obj)
        db.commit()
        return db_obj
    

    """
    Get HorseRaceInfo list
    """
    def get_list(self, db: Session, *, 
        race_ids: List[int]|None = None,
        horse_ids: List[int]|None = None,
        skip: int = 0,
        limit: int = 0,
    ) -> List[HorseRaceStats]:

        query = db.query(HorseRaceStats)

        if race_ids:
            query = query.filter(HorseRaceStats.race_id.in_(race_ids))

        if horse_ids:
            query = query.filter(HorseRaceStats.horse_id.in_(horse_ids))

        return query.order_by(HorseRaceStats.id).offset(skip).limit(limit).all()


    """
    Get HorseRaceInfo Details
    """
    def get_by_id(self, db: Session, *, info_id:int) -> HorseRaceStats:
        return db.query(HorseRaceStats).filter(HorseRaceStats.id == info_id).first()
    

horse_race_stats = HorseRaceStatsRepository()
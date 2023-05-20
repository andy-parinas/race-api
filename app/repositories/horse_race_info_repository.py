from typing import List
from sqlalchemy.orm import Session, joinedload

from app.models.horse_race_info import HorseRaceInfo
from app.schemas.horse_race_info import HorseRaceInfoCreate


class HorseRaceInfoRepository:
    
    """
    Create HorseRaceInfo
    """
    def create(self, db: Session, data_in: HorseRaceInfoCreate) -> HorseRaceInfo:
        data_obj = data_in.dict()
        db_obj = HorseRaceInfo(**data_obj)
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
    ) -> List[HorseRaceInfo]:

        query = db.query(HorseRaceInfo)

        if race_ids:
            query = query.filter(HorseRaceInfo.race_id.in_(race_ids))

        if horse_ids:
            query = query.filter(HorseRaceInfo.horse_id.in_(horse_ids))

        return query.order_by(HorseRaceInfo.id).offset(skip).limit(limit).all()


    """
    Get HorseRaceInfo Details
    """
    def get_by_id(self, db: Session, *, info_id:int) -> HorseRaceInfo:
        return db.query(HorseRaceInfo).filter(HorseRaceInfo.id == info_id).first()
    

horse_race_info = HorseRaceInfoRepository()
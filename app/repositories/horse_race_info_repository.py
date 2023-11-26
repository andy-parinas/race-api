from typing import List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, update
from app.models.horse_race_info import HorseRaceInfo
from app.models.horse_race_stats import HorseRaceStats
from app.models.horse import Horse
from app.models.race import Race
from app.models.meeting import Meeting
from app.schemas.horse_race_info import HorseRaceInfoCreate, HorseRaceInfoData, HorseRaceInfo as HorseRaceInfoSchema
from app.schemas.race import Race as RaceSchema, RaceWithMeeting
from app.schemas.horse import Horse as HorseSchema, HorseWithStats


class HorseRaceInfoRepository:

    """
    Create HorseRaceInfo
    """

    def create(self, db: Session, data_in: HorseRaceInfoData) -> HorseRaceInfo:
        data_obj = data_in.dict()
        db_obj = HorseRaceInfo(**data_obj)
        db.add(db_obj)
        db.commit()
        return HorseRaceInfoSchema.from_orm(db_obj)

    """
    Get HorseRaceInfo list
    """

    def get_list(self, db: Session, *,
                 race_ids: List[int] | None = None,
                 horse_ids: List[int] | None = None,
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

    def get_by_id(self, db: Session, *, info_id: int) -> HorseRaceInfo:
        return db.query(HorseRaceInfo).filter(HorseRaceInfo.id == info_id).first()

    def get_horse_race_info(self, db: Session, *, race_id: int, horse_id: int):
        stmt = select(HorseRaceInfo).where(HorseRaceInfo.race_id == race_id, HorseRaceInfo.horse_id == horse_id,
                                           HorseRaceInfo.is_scratched == False)

        info = db.scalars(stmt).first()

        if not info:
            return None

        return HorseRaceInfoSchema.from_orm(info)

    def get_horse_race_info_details(self, db: Session, *, race_id: int, horse_id: int):

        stmt = (
            select(HorseRaceInfo, Race, Horse)
            .join(Race).options(joinedload(Race.meeting).joinedload(Meeting.track))
            .join(Horse).options(joinedload(Horse.stats))
            .where(HorseRaceInfo.race_id == race_id, HorseRaceInfo.horse_id == horse_id)
        )

        results = db.execute(stmt).unique().first()

        horse_race_info, race, horse = results

        return {
            "horse_race_info": HorseRaceInfoSchema.from_orm(horse_race_info),
            "race": RaceWithMeeting.from_orm(race),
            "horse": HorseWithStats.from_orm(horse)
        }

    def update_horse_race_info(self, db: Session, id: int, info_data: HorseRaceInfoData):
        stmt = (update(HorseRaceInfo).where(HorseRaceInfo.id == id)
                .values(
                    colours=info_data.colours,
                    colours_pic=info_data.colours_pic,
                    last_starts=info_data.last_starts,
                    jockey=info_data.jockey,
                    trainer=info_data.trainer,
                    barrier=info_data.barrier
        ))

        db.execute(stmt)
        db.commit()

    def scratch(self, db: Session, id: int):
        stmt = update(HorseRaceInfo).where(HorseRaceInfo.id == id).values(
            is_scratched=True
        )

        db.execute(stmt)
        db.commit()

horse_race_info = HorseRaceInfoRepository()

from typing import List
from sqlalchemy.orm import Session, joinedload

from app.models.horse_race_stats import HorseRaceStats
from app.schemas.horse_race_stats import HorseRaceStatsCreate, HorseRaceStat as HorseRaceStatSchema


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

    def get_stats(self, db: Session, *,
                  race_ids: List[int] | None = None,
                  horse_ids: List[int] | None = None,
                  stats: List[str] | None = None) -> List[HorseRaceStatSchema]:

        query = db.query(HorseRaceStats)

        if race_ids:
            query = query.filter(HorseRaceStats.race_id.in_(race_ids))

        if horse_ids:
            query = query.filter(HorseRaceStats.horse_id.in_(horse_ids))

        if stats:
            query = query.filter(HorseRaceStats.stat.in_(stats))

        stats = query.order_by(HorseRaceStats.id).all()

        # return HorseRaceStatSchema.from_orm(stats)
        return [HorseRaceStatSchema.from_orm(stat) for stat in stats]

    """
    Get HorseRaceInfo Details
    """

    def get_by_id(self, db: Session, *, stat_id: int) -> HorseRaceStats:
        return db.query(HorseRaceStats).filter(HorseRaceStats.id == stat_id).first()


horse_race_stats = HorseRaceStatsRepository()

from typing import List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, update

from app.models.horse_race_stats import HorseRaceStats
from app.schemas.horse_race_stats import HorseRaceStatsCreate, HorseRaceStatsData, HorseRaceStat as HorseRaceStatSchema


class HorseRaceStatsRepository:

    def create(self, db: Session, data_in: HorseRaceStatsCreate) -> HorseRaceStats:

        data_in.win_ratio = self.__compute_win_ratio(
            total=data_in.total, first=data_in.first,
            second=data_in.second, third=data_in.third)

        data_obj = data_in.dict()
        print(data_obj)
        db_obj = HorseRaceStats(**data_obj)
        db.add(db_obj)
        db.commit()
        return HorseRaceStatSchema.from_orm(db_obj)

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

    def get_by_id(self, db: Session, *, stat_id: int) -> HorseRaceStats:
        return db.query(HorseRaceStats).filter(HorseRaceStats.id == stat_id).first()

    def get_horse_race_stats(self, db: Session, race_id: int, horse_id: int, stat: str):
        stmt = select(HorseRaceStats).where(HorseRaceStats.race_id ==
                                            race_id, HorseRaceStats.horse_id == horse_id, HorseRaceStats.stat == stat)

        stats = db.scalars(stmt).first()

        if not stats:
            return None

        return HorseRaceStatSchema.from_orm(stats)

    def update_horse_race_stats(self, db: Session, id: int, stats_data: HorseRaceStatsData):

        win_ratio = self.__compute_win_ratio(
            total=stats_data.total, first=stats_data.first,
            second=stats_data.second, third=stats_data.third)

        stmt = update(HorseRaceStats).where(HorseRaceStats.id == id).values(
            stat=stats_data.stat,
            total=stats_data.total,
            first=stats_data.first,
            second=stats_data.second,
            third=stats_data.third,
            win_ratio=win_ratio,
        )

        db.execute(stmt)
        db.commit()

    def __compute_win_ratio(self, *, total, first, second, third):
        win_ratio = 0
        if total > 0:
            win_ratio = (first + second * 0.5 + third * 0.25) / total

        return win_ratio


horse_race_stats = HorseRaceStatsRepository()

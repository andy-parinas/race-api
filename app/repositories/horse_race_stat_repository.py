from typing import List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, update

from app.models.horse_race_stats import HorseRaceStats
from app.schemas.horse_race_stats import (
    HorseRaceStatsCreate,
    HorseRaceStatsData,
    HorseRaceStat as HorseRaceStatSchema
)


class HorseRaceStatsRepository:

    def create(self, db: Session, data_in: HorseRaceStatsCreate, last_starts: str) -> HorseRaceStats:

        data_in.win_ratio = self.__compute_win_ratio(
            total=data_in.total, first=data_in.first,
            second=data_in.second, third=data_in.third, stats=data_in.stat, last_starts=last_starts)

        data_obj = data_in.dict()
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


    def get_all_stats_by_id(self, db: Session, race_id: int, horse_id: int):
        stmt = select(HorseRaceStats).where(HorseRaceStats.race_id == race_id,
                                            HorseRaceStats.horse_id == horse_id, )

        results = db.execute(stmt).unique().all()

        stats_results = []
        for result in results:
            stat, = result
            stat_schema = HorseRaceStatSchema.from_orm(stat)
            stats_results.append(stat_schema)

        return stats_results

    def get_selective_stats(self, db: Session, *,
                            race_ids: List[int] | None = None,
                            horse_ids: List[int] | None = None,
                            stats: List[str] | None = None) -> List[HorseRaceStatSchema]:

        print("Here\n")
        stmt = select(HorseRaceStats).where(HorseRaceStats.is_scratched == False)

        if race_ids:
            stmt = stmt.where(HorseRaceStats.race_id.in_(race_ids))

        if horse_ids:
            stmt = stmt.where(HorseRaceStats.horse_id.in_(horse_ids))

        if stats:
            stmt = stmt.where(HorseRaceStats.stat.in_(stats))

        stmt = stmt.order_by(HorseRaceStats.id)

        results = db.execute(stmt).unique().all()

        stats_results = []
        exclude_horse_id = set()
        for result in results:
            stat, = result

            if stat.stat == "first_up" or stat.stat == "second_up":

                if stat.win_ratio == 0:
                    exclude_horse_id.add(stat.horse_id)

            stat_schema = HorseRaceStatSchema.from_orm(stat)
            stats_results.append(stat_schema)

        if not exclude_horse_id:
            return stats_results

        filtered_result = []
        for stat_result in stats_results:
            if stat_result.horse_id not in exclude_horse_id:
                filtered_result.append(stat_result)

        return filtered_result

    def get_by_id(self, db: Session, *, stat_id: int) -> HorseRaceStats:
        return db.query(HorseRaceStats).filter(HorseRaceStats.id == stat_id).first()

    def get_horse_race_stats(self, db: Session, race_id: int, horse_id: int, stat: str):
        stmt = select(HorseRaceStats).where(HorseRaceStats.race_id ==
                                            race_id, HorseRaceStats.horse_id == horse_id, HorseRaceStats.stat == stat)

        stats = db.scalars(stmt).first()

        if not stats:
            return None

        return HorseRaceStatSchema.from_orm(stats)



    def update_horse_race_stats(self, db: Session, id: int, stats_data: HorseRaceStatsData, last_starts: str):

        win_ratio = self.__compute_win_ratio(
            total=stats_data.total, first=stats_data.first,
            second=stats_data.second, third=stats_data.third, stats=stats_data.stat, last_starts=last_starts)

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

    def scratch(self, db: Session, id: int):
        stmt = update(HorseRaceStats).where(HorseRaceStats.id == id).values(
            is_scratched = True
        )

        db.execute(stmt)
        db.commit()

    def __compute_win_ratio(self, *, total, first, second, third, stats: str, last_starts: str):
        win_ratio = 0

        if total > 0:
            if stats == "first_up":
                if not self.__with_first_up(last_starts):
                    return 0

            if stats == "second_up":
                if not self.__with_second_up(last_starts):
                    return 0

            win_ratio = (first + second * 0.5 + third * 0.25) / total

        return win_ratio

    def __with_first_up(self, last_starts) -> bool:
        if len(last_starts) >= 2 and last_starts[-1] == 'x':
            return True
        else:
            return False

    def __with_second_up(self, last_starts) -> bool:
        if len(last_starts) >= 2 and last_starts[-2] == 'x':
            return True
        else:
            return False


horse_race_stats = HorseRaceStatsRepository()

from typing import List
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, select, update

from app.models.race import Race
from app.models.meeting import Meeting
from app.models.track import Track
from app.models.horse import Horse
from app.models.horse_race_info import HorseRaceInfo
from app.models.horse_race_stats import HorseRaceStats
from app.schemas.race import RaceCreate, RaceData, Race as RaceSchema, RaceWithMeeting, RaceListResults, HorseRaceInfoAndStats, HorseRaceInfoAndStatsList, HorseWithStatsAndInfo, RaceDetailsWithHorseStats
# from app.schemas.horse_race_info import HorseRaceInfo as HorseRaceInfoSchema


class RaceRepository:

    def create(self, db: Session, race_in: RaceCreate) -> RaceSchema:
        race_obj = race_in.dict()
        db_obj = Race(**race_obj)
        db.add(db_obj)
        db.commit()

        return RaceSchema.from_orm(db_obj)

    def get_races(self, db: Session, *, meeting_id: int = None, date_filter: str = None, date_time: str = None,
                  datetime_end: str = None, order_by: str = "date_time",  direction: str = "asc",
                  skip: int = 0, limit: int = 0, ) -> List[Race]:

        stmt = (select(Race, Meeting)
                .join(Meeting)
                .options(joinedload(Meeting.track))
                )

        # query = db.query(Race)

        if meeting_id:
            stmt = stmt.where(Race.meeting_id == meeting_id)
            # query = query.filter(Race.meeting_id == meeting_id)

        if date_time:
            race_datetime = datetime.strptime(date_time, "%Y-%m-%d-%H-%M")
            eq_filter_mapping = ["eq", "gt", "gteq", "lt", "lteq"]
            if date_filter in eq_filter_mapping:
                filter_mapping = {
                    "gt": Race.date_time > race_datetime,
                    "gteq": Race.date_time >= race_datetime,
                    "lt": Race.date_time < race_datetime,
                    "lteq": Race.date_time <= race_datetime,
                    "eq": Race.date_time == race_datetime,
                }
                stmt = stmt.where(filter_mapping[date_filter])
                # query = query.filter(filter_mapping[date_filter])
            elif date_filter == "bet" and datetime_end:
                race_datetime_end = datetime.strptime(
                    datetime_end, "%Y-%m-%d-%H-%M")
                stmt = stmt.where(Race.date_time.between(
                    race_datetime, race_datetime_end))
                # query = query.filter(
                #     Race.date_time.between(race_datetime, race_datetime_end))

        valid_fields = ["id", "race_id",
                        "date_time", "distance", "race_number"]
        valid_directions = ["asc", "desc"]

        if order_by in valid_fields and direction in valid_directions:
            attribute = getattr(Race, order_by)
            ordering = getattr(attribute, direction)()
            stmt = stmt.order_by(ordering)
            # query = query.order_by(ordering)

        stmt = stmt.offset(skip).limit(limit)

        results = db.execute(stmt).unique().all()

        races = []
        for result in results:
            race, meeting = result
            races.append(RaceWithMeeting.from_orm(race))

        return RaceListResults(races=races)

    def get_race_by_id(self, db: Session, *, id: int) -> Race:

        # stmt = (
        #     select(HorseRaceInfo, Race, Horse)
        #     .join(Race)
        #     .join(Horse).options(joinedload(Horse.stats))
        #     .where(HorseRaceInfo.race_id == id)
        # )

        stmt = (
            select(Race)
            .options(
                joinedload(Race.horses).lazyload(Horse.stats.and_(HorseRaceStats.is_scratched == False))
            )
            .options(joinedload(Race.horses).lazyload(Horse.infos.and_(HorseRaceInfo.is_scratched == False)))
            .where(Race.id == id)
        )




        # results = db.execute(stmt).unique().first()
        race = db.scalars(stmt).first()

        # print(race)

        # race, = results

        race_data = RaceDetailsWithHorseStats.from_orm(race)

        return race_data

    def get_race(self, db: Session, *, race_id: int = None, date_time: str = None, race_number: int = None, meeting_id: int = None):

        stmt = select(Race)

        if race_id:
            stmt = stmt.where(Race.race_id == race_id)

        if date_time:
            race_date_time = datetime.strptime(date_time, "%d/%m/%Y %I:%M%p")
            stmt = stmt.where(Race.date_time == race_date_time)

        if race_number:
            stmt = stmt.where(Race.race_number == race_number)

        if meeting_id:
            stmt = stmt.where(Race.meeting_id == meeting_id)

        race = db.scalars(stmt).first()

        if not race:
            return None

        return RaceSchema.from_orm(race)

    def update_race(self, db: Session, id: int, race_data: RaceData) -> RaceSchema:
        stmt = update(Race).where(Race.id == id).returning(Race).values(
            race_id=race_data.race_id,
            name=race_data.name,
            date_time=race_data.date_time,
            distance=race_data.distance
        )

        race = db.scalars(stmt).first()

        return RaceSchema.from_orm(race)


race = RaceRepository()

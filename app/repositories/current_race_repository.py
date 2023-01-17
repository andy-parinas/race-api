import pandas as pd
from pandas import DataFrame
from typing import List
from sqlalchemy import and_
from sqlalchemy.orm import Session


from app.schemas.current_race import CurrentRaceCreate
from app.models.current_race import CurrentRace



def calculate_win_ratio(total, first, second, third):
    if total != 0: 
        value = (((first * 1) + (second * 0.5) + (third * 0.25))/( total))
        return round(value, 2)
    return 0


class CurrentRaceRepository:

    def create(self, db: Session, obj_in: CurrentRaceCreate):
        current_race_obj = obj_in.dict()
        db_obj = CurrentRace(**current_race_obj)
        db_obj.win_ratio = calculate_win_ratio(obj_in.total, obj_in.first, obj_in.second, obj_in.third)
        db.add(db_obj)
        db.commit()
        return db_obj

    def get_races_dataframe(self, db:Session, preference: List[str], race_ids: List[int]):
        statement = db.query(CurrentRace) \
                    .filter(CurrentRace.stat.in_(preference)) \
                    .filter(and_(CurrentRace.race_id.in_(race_ids))).statement

        df = pd.read_sql_query(statement, con=db.connection())

        return df


current_race = CurrentRaceRepository()

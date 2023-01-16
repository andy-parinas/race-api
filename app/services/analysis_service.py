import pandas as pd
import numpy as np
from pandas import DataFrame
from typing import List
from sqlalchemy.orm import Session

from app.schemas.analysis import Preference
from app import repositories as repo

class AnalysisService:

    def compute_pref_multiplier(self, df: DataFrame, 
        conditions: List[bool], pref_weight: List[float]
    ) -> DataFrame:

        df['multiplier'] = np.select(conditions, pref_weight, 0)

        return df 

    def get_condition_weight(self,df: DataFrame, preference: Preference):
        conditions = [
            df['stat'] == preference.first,
            df['stat'] == preference.second,
            df['stat'] == preference.third
        ]

        weights = [0.60, 0.30, 0.10]

        return {
            "conditions": conditions,
            "weights": weights
        }

    def get_top_hoses(self, db: Session, preference: Preference, race_ids: List[int]):
        pref_dict = dict(preference)
        prefs = list(pref_dict.values())

        race_stmt = repo.current_race.get_races_statement(db, prefs, race_ids)
        df = pd.read_sql_query(race_stmt, con=db.connection())

        condition = self.get_condition_weight(df, preference)

        df = self.compute_pref_multiplier(df, conditions=condition['conditions'], pref_weight=condition['weights'])

        df['results'] = (df['win_ratio'] * df['multiplier']) * 100

        df = df.groupby(['horse_id'])['results'].sum().sort_values(ascending=False).nlargest(3)

        print(df)
        return prefs


analysis = AnalysisService()

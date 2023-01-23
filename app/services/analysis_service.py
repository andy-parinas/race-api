import pandas as pd
import numpy as np
from pandas import DataFrame
from typing import List
from sqlalchemy.orm import Session

from app.schemas.analysis import Preference
from app import repositories as repo
from app.schemas.horse import Horse

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

    def analyse_race(self, df: DataFrame, weighted_condition):
        
        df['multiplier'] = np.select(weighted_condition['conditions'], weighted_condition['weights'], 0)
        df['results'] = (df['win_ratio'] * df['multiplier']) * 100
        df = df.groupby(['horse_id'])['results'].sum().sort_values(ascending=False).nlargest(5)

        return df.to_dict()


    def get_top_hoses(self, db: Session, preference: Preference, race_ids: List[int]):
        pref_dict = dict(preference)
        prefs = list(pref_dict.values())

        df = repo.current_race.get_races_dataframe(db, prefs, race_ids)
        weighted_condition = self.get_condition_weight(df, preference)

        analysis = self.analyse_race(df, weighted_condition)
        horses = repo.horse.get_horses_from_ids(db, list(analysis.keys()))


        print(analysis)
        result = []
        for horse in horses:
            # setattr(horse, 'rating', analysis[horse.id])
            """
            Crude way of converting the SQLAlchemy model into
            Dictionary
            """
            result.append({
                "id": horse.id,
                "horse_id": horse.horse_id,
                "horse_name": horse.horse_name,
                "rating": analysis[horse.id],
                "race_id": horse.race_id
            })

        sorted_result = sorted(result, key=lambda d: d['rating'], reverse=True)
        return sorted_result


analysis = AnalysisService()

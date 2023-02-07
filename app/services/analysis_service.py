from typing import List
import pandas as pd
import numpy as np
from pandas import DataFrame
from typing import List
from sqlalchemy.orm import Session

from app.schemas.analysis import Preference
from app import repositories as repo
from app.schemas.horse import Horse
from app.schemas.analysis import PreferenceType

class AnalysisService:

    def __init__(self, df: DataFrame, prefrerences: List[str], preference_type: PreferenceType) -> None:
        self.df = df
        self.preferences = prefrerences
        self.preference_type = preference_type

    def get_preference_weight(self):
        weights = []
        conditions = []
        for pref in self.preferences:
            conditions.append(self.df['stat'] == pref)
            if self.preference_type == PreferenceType.balance:
                weights.append(1/len(self.preferences))
            if self.preference_type == PreferenceType.weighted:
                weights = self.get_weight(len(self.preferences))

        print(self.preference_type)

        return {
            "conditions": conditions,
            "weights": weights
        }

    def get_weight(self, preference_count):
        if preference_count == 1:
            return [1]
        elif preference_count == 2:
            return [0.60, 0.40]
        elif preference_count == 3:
            return [0.55, 0.30, 0.15]
        elif preference_count == 4:
            return [0.50, 0.25, 0.15, 0.10]
        elif preference_count == 5:
            return [0.45, 0.25, 0.15, 0.10, 0.05]
        else:
            return None

    def get_condition_weight(self):

        conditions = [
            self.df['stat'] == self.preference.first,
            self.df['stat'] == self.preference.second,
            self.df['stat'] == self.preference.third
        ]
        
        weights = [0.60, 0.30, 0.10]

        return {
            "conditions": conditions,
            "weights": weights
        }

    def apply_condition(self, weighted_condition):
        
        self.df['multiplier'] = np.select(weighted_condition['conditions'], weighted_condition['weights'], 0)
        self.df['results'] = (self.df['win_ratio'] *self.df['multiplier']) * 100

        
    def get_race_top_results(self):
        self.df = self.df.groupby(['horse_id'])['results'].sum().sort_values(ascending=False).nlargest(5)

        return self.df.to_dict()

    """
    Analyse the Race based on the Given Preferences
    """
    def analyse(self):
        # weighted_condition = self.get_condition_weight(df, preference)
        weighted_condition = self.get_preference_weight()
        self.apply_condition(weighted_condition=weighted_condition)

        results = self.get_race_top_results()

        return results


    # def get_horses_top_results(self,db:Session, results):
    #     horses = repo.horse.get_horses_from_ids(db, list(results.keys()))
    #     result = []
    #     for horse in horses:
    #         # setattr(horse, 'rating', analysis[horse.id])
    #         """
    #         Crude way of converting the SQLAlchemy model into
    #         Dictionary
    #         """
    #         result.append({
    #             "id": horse.id,
    #             "horse_id": horse.horse_id,
    #             "horse_name": horse.horse_name,
    #             "rating": analysis[horse.id],
    #             "race_id": horse.race_id
    #         })

    #     sorted_result = sorted(result, key=lambda d: d['rating'], reverse=True)
    #     return sorted_result

    # def get_top_hoses(self, db: Session, preference: Preference, race_ids: List[int]):
    #     pref_dict = dict(preference)
    #     prefs = list(pref_dict.values())

    #     df = repo.current_race.get_races_dataframe(db, prefs, race_ids)
    #     weighted_condition = self.get_condition_weight(df, preference)

    #     analysis = self.apply_condition(df, weighted_condition)
    #     horses = repo.horse.get_horses_from_ids(db, list(analysis.keys()))

    #     result = []
    #     for horse in horses:
    #         # setattr(horse, 'rating', analysis[horse.id])
    #         """
    #         Crude way of converting the SQLAlchemy model into
    #         Dictionary
    #         """
    #         result.append({
    #             "id": horse.id,
    #             "horse_id": horse.horse_id,
    #             "horse_name": horse.horse_name,
    #             "rating": analysis[horse.id],
    #             "race_id": horse.race_id
    #         })

    #     sorted_result = sorted(result, key=lambda d: d['rating'], reverse=True)
    #     return sorted_result


# analysis = AnalysisService()

from typing import List
import pandas as pd
import numpy as np
from pandas import DataFrame, Series
from typing import List, Tuple
from sqlalchemy.orm import Session

from app.schemas.analysis import Preference
from app import repositories as repo
from app.schemas.horse import Horse
from app.schemas.analysis import PreferenceType


class AnalysisBase:
    def __init__(self, df: DataFrame, prefrerences: Tuple[str], preference_type: PreferenceType) -> None:
        self.df = df
        if "all" not in prefrerences:
            prefrerences.append("all")
        self.preferences = tuple(prefrerences)
        self.preference_type = preference_type
        self.preferences_count = len(self.preferences)

    def get_weighted_value(self):

        if self.preferences_count == 1:
            return (1)
        elif self.preferences_count == 2:
            return (0.60, 0.40)
        elif self.preferences_count == 3:
            return (0.55, 0.30, 0.15)
        elif self.preferences_count == 4:
            return (0.50, 0.25, 0.15, 0.10)
        elif self.preferences_count == 5:
            return (0.45, 0.25, 0.15, 0.10, 0.05)
        else:
            return None
    
    def get_preference_weight(self):
        weights = self.get_weighted_value()
        result = []
        for i, pref in  enumerate(self.preferences):
            if self.preference_type == PreferenceType.balance:
                result.append((pref, 1/self.preferences_count))
            if self.preference_type == PreferenceType.weighted:
                result.append((pref, weights[i]))


        return tuple(result)


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



class BayseAnalysis(AnalysisBase):
    def __init__(self, df: DataFrame, prefrerences: List[str], preference_type: PreferenceType) -> None:
        super().__init__(df, prefrerences, preference_type)

    def get_likelihood(self, data: DataFrame):
        likelihood = pd.Series(dtype=float)
        preferences = self.get_preference_weight()

        for pref in preferences:
            s = data[pref[0]] * pref[1]
            likelihood = likelihood.add(s, fill_value=0) 
        
        return likelihood

    def transform_dataframe(self):
        data = self.df.pivot_table(index='horse_id', columns='stat', values='win_ratio')
        return data

    def get_probability(self, data: DataFrame, likelihood: Series):
        data = data.merge(pd.DataFrame(likelihood.rename('likelihood')), left_index=True, right_index=True)

        data['prior'] = data['all']
        data["unnormalized_posterior"] =  data['prior'] * data['likelihood']
        normalization_factor = data["unnormalized_posterior"].sum()
        
        if normalization_factor == 0:
            return None
        
        data["posterior_probability"] = round(data["unnormalized_posterior"] / normalization_factor, 2)

        data = data.sort_values(['posterior_probability'], ascending= [False])

        return data.head(5)['posterior_probability'].to_dict()

    

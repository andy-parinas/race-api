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
        self.preferences = tuple(prefrerences)
        self.preference_type = preference_type
        self.preferences_count = len(self.preferences)

    
    def get_preference_weight(self):
        if self.preference_type == PreferenceType.balance:
            return self.compute_balance_value(self.preferences)
        if self.preference_type == PreferenceType.weighted:
            return self.compute_weighted_value(self.preferences)

    
    def compute_weighted_value(self, preferences):
        print(preferences)
        count = len(preferences)
        weight_rating = list(range(count, 0, -1))
        sum_of_weight = sum(weight_rating)

        result = []
        for pref, weight in zip(preferences, weight_rating):
            result.append((pref, weight/sum_of_weight))

        return result
        

    def compute_balance_value(self, preferences):
        result = []
        for pref in preferences:
            result.append((pref, 1/len(preferences)))

        return result



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
        if (data['prior'] == 0).all():
            data['unnormalized_posterior'] = data['likelihood']
        else:
            data["unnormalized_posterior"] =  data['prior'] * data['likelihood']

        normalization_factor = data["unnormalized_posterior"].sum()
        
        if normalization_factor == 0:
            data["posterior_probability"] = 0
        else:
            data["posterior_probability"] = round(data["unnormalized_posterior"] / normalization_factor, 2)

        data = data.sort_values(['posterior_probability'], ascending= [False])

        return data.head(5)['posterior_probability'].to_dict()

    

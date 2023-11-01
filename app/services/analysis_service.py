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
        self.preferences = prefrerences
        self.preference_type = preference_type
        self.preferences_count = len(self.preferences)

    def get_preference_weight(self):
        if self.preference_type == PreferenceType.balance:
            return self.compute_balance_value(self.preferences)
        if self.preference_type == PreferenceType.weighted:
            return self.compute_weighted_value(self.preferences)

    def compute_weighted_value(self, preferences):
        # print(preferences)
        count = len(preferences)
        weight_rating = list(range(count, 0, -1))
        sum_of_weight = sum(weight_rating)

        result = []
        for pref, weight in zip(preferences, weight_rating):
            result.append((pref, weight/sum_of_weight))

        return result

    def compute_balance_value(self, preferences):
        result = []
        # print(preferences)
        for pref in preferences:
            result.append((pref, 1/len(preferences)))

        return result


class ExponentialAnalysis(AnalysisBase):
    def __init__(self, df: DataFrame, prefrerences: List[str], preference_type: PreferenceType) -> None:
        super().__init__(df, prefrerences, preference_type)

    def get_preference_total_sum(self):
        preferences_sum = {}
        for pref in self.preferences:
            preferences_sum[pref] = self.df[self.df['stat'] == pref]['total'].sum()

        return preferences_sum

    def compute_extra_data(self):
        preferences_sum = self.get_preference_total_sum()

        self.df['modified_weight'] = self.df.apply(
            lambda row: row['win_ratio'] * 0.6 + (row['total'] / preferences_sum[row['stat']]) * 0.4, axis=1)
        self.df['exponential_weight'] = self.df.apply(lambda row: 2.718281828459045 ** row['modified_weight'], axis=1)

    def get_total_exponential(self):

        self.compute_extra_data()

        exponential_sum = {}
        for pref in self.preferences:
            exponential_sum[pref] = self.df[self.df['stat'] == pref]['exponential_weight'].sum()

        return exponential_sum



    def compute_rating(self):

        preferences = self.get_preference_weight()

        preference_weight = {key: int(value * 100) for key, value in preferences}

        exponential_sums = self.get_total_exponential()
        self.df['normalized_exponential'] = self.df.apply(
            lambda row: row['exponential_weight'] / exponential_sums[row['stat']], axis=1)

        self.df['rating'] = self.df.apply(lambda row: row['normalized_exponential'] * preference_weight[row['stat']],
                                            axis=1)

        return self.df

    def transform_dataframe(self):
        self.compute_rating()

        data = self.df.pivot_table(
            index='horse_id', columns='stat', values='rating')

        return data

    def sum_rating(self, row, *column_names):
        values = [row[col] for col in column_names if row[col] > 0]
        num_columns = len(values)

        if num_columns == 0:
            return 0.0
        elif num_columns == 1:
            return round(values[0]) / 100
        else:
            return round(sum(values)) / 100

    def get_final_rating(self):
        data = self.transform_dataframe()

        data['rating_summation'] = data.apply(lambda row: self.sum_rating(row, *self.preferences), axis=1)

        final_data = data.sort_values('rating_summation', ascending=[False])

        return final_data['rating_summation'].head(4).to_dict()

class BasicAnalysis(AnalysisBase):
    def __init__(self, df: DataFrame, prefrerences: List[str], preference_type: PreferenceType) -> None:
        super().__init__(df, prefrerences, preference_type)

    def transform_dataframe(self):
        data = self.df.pivot_table(
            index='horse_id', columns='stat', values='win_ratio')

        return data

    def get_likelihood(self, data: DataFrame):
        likelihood = pd.Series(dtype=float)
        preferences = self.get_preference_weight()
        print(preferences)
        for pref in preferences:
            s = data[pref[0]] * pref[1]
            likelihood = likelihood.add(s, fill_value=0)

        return likelihood

    def get_probability(self, likelihood: Series):

        data = likelihood.sort_values(ascending=[False])

        return data.head(4).to_dict()


class BayseAnalysis(AnalysisBase):
    def __init__(self, df: DataFrame, prefrerences: List[str], preference_type: PreferenceType) -> None:
        super().__init__(df, prefrerences, preference_type)

    def get_likelihood(self, data: DataFrame):
        likelihood = pd.Series(dtype=float)
        preferences = self.get_preference_weight()
        # print("##### PREFERENCES #####")
        for pref in preferences:
            s = data[pref[0]] * pref[1]
            likelihood = likelihood.add(s, fill_value=0)

        return likelihood

    def transform_dataframe(self):
        data = self.df.pivot_table(
            index='horse_id', columns='stat', values='win_ratio')

        return data

    def get_probability(self, data: DataFrame, likelihood: Series):
        data = data.merge(pd.DataFrame(likelihood.rename(
            'likelihood')), left_index=True, right_index=True)

        data['prior'] = data['all']
        # print(data['prior'])
        if (data['prior'] == 0).all():
            data['unnormalized_posterior'] = data['likelihood']
        else:
            data["unnormalized_posterior"] = data['prior'] * data['likelihood']

        # print(data['likelihood'])

        # print(data["unnormalized_posterior"])

        normalization_factor = data["unnormalized_posterior"].sum()

        if normalization_factor == 0:
            data["posterior_probability"] = 0
        else:
            data["posterior_probability"] = round(
                data["unnormalized_posterior"] / normalization_factor, 2)

        data = data.sort_values(['posterior_probability'], ascending=[False])

        return data.head(5)['posterior_probability'].to_dict()

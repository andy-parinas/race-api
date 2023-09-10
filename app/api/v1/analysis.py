from typing import List, Dict
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from pandas import DataFrame, concat

from app import repositories as repo
from app.schemas.analysis import AnalsyisInput
from app.schemas.horse import HorseListResult
from app.db.session import get_db
from app.services.analysis_service import BasicAnalysis, Preference, BayseAnalysis

router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK)
def analyse_race_advance(analysis_in: AnalsyisInput,  db: Session = Depends(get_db)):

    preferences = analysis_in.preferences
    # preferences.append("all")

    results, race_horses = __analyze_multiple_race(
        db, analysis_in.race_ids, preferences, analysis_in.preference_type)

    results = __get_analysis_results_values(db, results, race_horses)

    return results


def __analyze_multiple_race(db, race_ids, preferences, preference_type):

    final_df = DataFrame()
    race_horses = []

    for race_id in race_ids:
        single_race_result, horse_ids = __analyze_single_race(
            db, race_id, preferences, preference_type)

        race_horses.append(horse_ids)

        if not single_race_result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="No results found. Statistics does not have enough information.")

        """
        Convert the analysis_result into a dataframe. 
        """
        analysis_df = DataFrame.from_dict(
            single_race_result, orient='index', columns=['rating'])
        analysis_df.index.name = 'horse_id'

        """
        For multiple races, gather all the analysis_result into the final_df
        """
        final_df = concat([final_df, analysis_df], ignore_index=False)

    """
    Sort the values from highes to lowest rating
    """
    final_df = final_df.sort_values(['rating'], ascending=[False])

    """
    Return only the top 5 results and the race_horses which contains list of race_id and horses in that race
    """
    return final_df.head(5).to_dict(), race_horses


"""
This function will get and format the results of the analysis and get the values for output for the response.
"""


def __get_analysis_results_values(db, results, race_horses: List[Dict[int, List[int]]]):

    horse_rating = results['rating']

    output = []

    for horse_id, rating in sorted(horse_rating.items(), key=lambda x: x[1], reverse=True):
        for race in race_horses:
            for race_id, horse_ids in race.items():
                if horse_id in horse_ids:
                    horse_race_info = repo.horse_race_info.get_horse_race_info_details(
                        db, race_id=race_id, horse_id=horse_id)
                    if horse_race_info:
                        output.append({
                            "rating": rating,
                            "details": horse_race_info
                        })

                    break

    return output


def __analyze_single_race(db, race_id, preferences, preference_type):

    race_query_results = repo.horse_race_stats.get_selective_stats(
        db, race_ids=[race_id], stats=preferences)


    if not race_query_results or len(race_query_results) == 0:
        return None

    stat_df = __convert_stat_to_df(race_query_results)

    single_race_result = __get_basic_result(
        stat_df, preferences, preference_type)

    return single_race_result, {race_id: list(single_race_result.keys())}


def __convert_stat_to_df(stat_query_results):
    race_stat_data = [race_stat.dict() for race_stat in stat_query_results]
    return DataFrame(race_stat_data)


def __get_basic_result(df: DataFrame, selected_preferences: List[str], preference_type):

    stat_preferences = selected_preferences.copy()

    if "all" in stat_preferences:
        stat_preferences.remove("all")

    basic = BasicAnalysis(df=df, prefrerences=stat_preferences,
                          preference_type=preference_type)

    data = basic.transform_dataframe()

    likelihood = basic.get_likelihood(data)

    return basic.get_probability(likelihood=likelihood)


def __get_bayes_results(df: DataFrame, selected_preferences: List[str], preference_type):

    # print(df)

    stat_preferences = selected_preferences.copy()

    if "all" in stat_preferences:
        stat_preferences.remove("all")

    bayes = BayseAnalysis(df=df, prefrerences=stat_preferences,
                          preference_type=preference_type)

    data = bayes.transform_dataframe()

    # print(data)

    likelihood = bayes.get_likelihood(data)

    # print(likelihood)

    # return likelihood
    return bayes.get_probability(data, likelihood)

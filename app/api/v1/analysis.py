from typing import List, Dict
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from pandas import DataFrame, concat

from app import repositories as repo
from app.schemas.analysis import AnalsyisInput
from app.schemas.horse import HorseListResult
from app.db.session import get_db
from app.services.analysis_service import Preference, BayseAnalysis

router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK)
def analyse_race_advance(analysis_in: AnalsyisInput,  db: Session = Depends(get_db)):

    preferences = analysis_in.preferences
    preferences.append("all")

    results, race_horses = __analyze_multiple_race(
        db, analysis_in.race_ids, preferences, analysis_in.preference_type)

    __get_analysis_results_values(db, results, race_horses)
    # print(results)

    return "results"


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

    for horse_id, rating in sorted(horse_rating.items(), key=lambda x: x[1], reverse=True):
        for race in race_horses:
            for race_id, horse_ids in race.items():
                if horse_id in horse_ids:
                    # horse_race_info

                    race_name = f"Race {race_id}"
                    print(
                        f"Horse {horse_id} belongs to {race_name} with a rating of {rating}")
                    break

    # result_ratings = results['rating']
    # for race in race_horses:
    #     for race_id, horse_ids in race.items():
    #         for horse_id in horse_ids:

    #             if horse_id in result_ratings:
    #                 race_number = f"Race {race_id}"
    #                 horse_rating_value = result_ratings[horse_id]
    #                 print(
    #                     f"Horse {horse_id} belongs to {race_number} with a rating of {horse_rating_value}")


def __analyze_single_race(db, race_id, preferences, preference_type):

    race_query_results = repo.horse_race_stats.get_stats(
        db, race_ids=[race_id], stats=preferences)

    if not race_query_results or len(race_query_results) == 0:
        return None

    stat_df = __convert_stat_to_df(race_query_results)

    single_race_result = __get_bayes_results(
        stat_df, preferences, preference_type)

    return single_race_result, {race_id: list(single_race_result.keys())}


def __convert_stat_to_df(stat_query_results):
    race_stat_data = [race_stat.dict() for race_stat in stat_query_results]
    return DataFrame(race_stat_data)


def _get_analysis_from_races(db: Session, races_ids, preferences: List[str], preference_type):
    final_df = DataFrame()

    preferences_with_all = preferences.copy()
    preferences_with_all.append("all")

    for race_id in races_ids:

        df = repo.current_race.get_race_dataframe(
            db, preferences_with_all, race_id)
        if df.empty:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Races not found")

        analysis_results = _get_bayes_results(df, preferences, preference_type)

        if not analysis_results:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="No results found. Statistics does not have enough information.")

        analysis_df = DataFrame.from_dict(
            analysis_results, orient='index', columns=['rating'])
        analysis_df.index.name = 'horse_id'

        final_df = concat([final_df, analysis_df], ignore_index=False)

    final_df = final_df.sort_values(['rating'], ascending=[False])
    top_horses = final_df.head(5).to_dict()
    return __get_horses_from_analysis(db, top_horses['rating'])


def __get_bayes_results(df: DataFrame, selected_preferences: List[str], preference_type):

    bayes = BayseAnalysis(df=df, prefrerences=selected_preferences,
                          preference_type=preference_type)

    data = bayes.transform_dataframe()
    likelihood = bayes.get_likelihood(data)

    # return likelihood
    return bayes.get_probability(data, likelihood)


# def __get_horses_from_analysis(db: Session, horses_dict):
#     horse_ids = list(horses_dict.keys())
#     horses = repo.horse.get_horses_from_ids(db, ids=horse_ids)
#     horse_array = []
#     for horse in horses:
#         horse_array.append({
#             "id": horse.id,
#             "horse_id": horse.horse_id,
#             "horse_name": horse.horse_name,
#             "rating": horses_dict[horse.id],
#             "race_id": horse.race_id,
#             "race_number": horse.race.race_number,
#             "meeting": horse.race.meeting.track_name,
#             "date": horse.race.meeting.meeting_date,
#             "state": horse.race.meeting.state
#         })

#     return sorted(horse_array, key=lambda d: d['rating'], reverse=True)

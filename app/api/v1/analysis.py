import pprint
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app import repositories as repo
from app.schemas.analysis import AnalsyisInput
from app.schemas.horse import HorseListResult
from app.db.session import get_db
from app.services.analysis_service import analysis, Preference

router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK)
def analyse_race(analysis_in: AnalsyisInput,  db:Session = Depends(get_db)):

    """
    Extract the Preferences into a list
    """
    prefs = __get_preferences(analysis_in.preference)
    df = repo.current_race.get_races_dataframe(db, prefs, analysis_in.race_ids)
    analysis_results = analysis.analyse(analysis_in.preference, analysis_in.race_ids, df)

    final_result = __get_horses_from_analysis(db, analysis_results)


    # return list(result)
    return {"results": final_result}


@router.post("/advance", status_code=status.HTTP_200_OK)
def analyse_race_advance(analysis_in: AnalsyisInput,  db:Session = Depends(get_db)):
    """
    Extract the Preferences into a list
    """
    # pref_dict = dict(analysis_in.preference)
    prefs = __get_preferences(analysis_in.preference)

    """
    Get the Dataframes from the database
    """
    df = repo.current_race.get_races_dataframe(db, prefs, analysis_in.race_ids)
    analysis_results = analysis.analyse(analysis_in.preference, analysis_in.race_ids, df)

    final_results = __get_final_results(db, analysis_results)

    return {"results": final_results}


def __get_preferences(preferences: Preference):
    pref_dict = dict(preferences)
    return list(pref_dict.values())


def __get_final_results(db: Session, analysis_results):
    final_result = []
    for result_key in analysis_results:
        
        race = __get_races_from_analysis(db, result_key)
        horses = __get_horses_from_analysis(db, analysis_results[result_key])
        
        race["horses"] = horses
        final_result.append(race)

    return final_result


def __get_races_from_analysis(db: Session, race_id):
    race = repo.race.get_race_by_id(db, race_id=race_id)
    return {
        "race_number": race.race_number,
        "date": race.race_date,
        "meeting_id": race.meeting_id
    }

def __get_horses_from_analysis(db: Session, horses_dict):
    horse_ids = list(horses_dict.keys())
    horses = repo.horse.get_horses_from_ids(db, ids=horse_ids)
    horse_array = []
    for horse in horses:
        print(horse.race.meeting.track_name)
        horse_array.append({
            "id": horse.id,
            "horse_id": horse.horse_id,
            "horse_name": horse.horse_name,
            "rating": horses_dict[horse.id],
            "race_id": horse.race_id,
            "race_number": horse.race.race_number,
            "meeting": horse.race.meeting.track_name,
            "date": horse.race.meeting.meeting_date,
            "state": horse.race.meeting.state
        })

    return sorted(horse_array, key=lambda d: d['rating'], reverse=True)
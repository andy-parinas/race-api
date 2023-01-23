from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app import repositories as repo
from app.schemas.analysis import AnalsyisInput
from app.schemas.horse import HorseListResult
from app.db.session import get_db
from app.services.analysis_service import analysis

router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK, response_model=HorseListResult)
def analyse_race(analysis_in: AnalsyisInput,  db:Session = Depends(get_db)):
    result = analysis.get_top_hoses(db, analysis_in.preference, analysis_in.race_ids)


    # return list(result)
    return {"results": result}


@router.post("/advance", status_code=status.HTTP_200_OK)
def analyse_race_advance(analysis_in: AnalsyisInput,  db:Session = Depends(get_db)):
    """
    Extract the Preferences into a list
    """
    pref_dict = dict(analysis_in.preference)
    prefs = list(pref_dict.values())

    """
    Get the Dataframes from the database
    """
    df = repo.current_race.get_races_dataframe(db, prefs, analysis_in.race_ids)

    analysis_results = analysis.analyse(analysis_in.preference, analysis_in.race_ids, df)

    final_result = []
    for result in analysis_results:
        race = repo.race.get_race_by_id(db, race_id=result)
        race_dict = {
            "race_number": race.race_number,
            "date": race.race_date,
            "meeting_id": race.meeting_id
        }
        horse_results = analysis_results[result]
        horse_ids = list(horse_results.keys())
        horses = repo.horse.get_horses_from_ids(db, ids=horse_ids)
        horse_array = []
        for horse in horses:
            horse_array.append({
                "id": horse.id,
                "horse_id": horse.horse_id,
                "horse_name": horse.horse_name,
                "rating": horse_results[horse.id],
                "race_id": horse.race_id
            })

        sorted_horses = sorted(horse_array, key=lambda d: d['rating'], reverse=True)
        race_dict["horses"] = sorted_horses
        final_result.append(race_dict)

    return final_result
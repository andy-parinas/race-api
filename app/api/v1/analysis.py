from typing import List
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from pandas import DataFrame, concat

from app import repositories as repo
from app.schemas.analysis import AnalsyisInput
from app.schemas.horse import HorseListResult
from app.db.session import get_db
from app.services.analysis_service import AnalysisService, Preference, BayseAnalysis

router = APIRouter()



@router.post("/", status_code=status.HTTP_200_OK)
def analyse_race_advance(analysis_in: AnalsyisInput,  db:Session = Depends(get_db)):

    results = _get_analysis_from_races(db, analysis_in.race_ids, analysis_in.preferences, analysis_in.preference_type)

    return {
        "results": results
    }




def _get_analysis_from_races(db: Session, races_ids, preferences: List[str], preference_type):
    final_df = DataFrame()

    if "all" not in preferences:
        preferences.append("all")

    for race_id in races_ids:
   
        df = repo.current_race.get_race_dataframe(db, preferences ,race_id)
        if df.empty:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Races not found")

        analysis_results = _get_bayes_results(df, preferences, preference_type )

        if not analysis_results:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No results found. Statistics does not have enough information.")

        analysis_df = DataFrame.from_dict(analysis_results, orient='index', columns=['rating'])
        analysis_df.index.name = 'horse_id'

        final_df = concat([final_df,analysis_df], ignore_index=False)
    
    final_df = final_df.sort_values(['rating'], ascending= [False])
    top_horses = final_df.head(5).to_dict()
    return __get_horses_from_analysis(db, top_horses['rating'])


def _get_bayes_results(df: DataFrame, preferences, preference_type):

    bayes = BayseAnalysis(df=df, prefrerences=preferences, 
                        preference_type=preference_type)


    data = bayes.transform_dataframe()
    likelihood = bayes.get_likelihood(data)

    return bayes.get_probability(data, likelihood)



def __get_horses_from_analysis(db: Session, horses_dict):
    horse_ids = list(horses_dict.keys())
    horses = repo.horse.get_horses_from_ids(db, ids=horse_ids)
    horse_array = []
    for horse in horses:
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
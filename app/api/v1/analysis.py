from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

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
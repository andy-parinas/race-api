from typing import Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app import repositories as repo
from app.schemas.meeting import MeetingData

router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK)
def get_races(
    meeting_data: MeetingData,
    page: int = 1,
    max_results: int = 100,
    db: Session = Depends(get_db)
):
    skip = (page -1) * max_results

    if meeting_data is not None:
        results = repo.race.get_race_list(db, skip=skip, limit=max_results, meeting_ids=meeting_data.meeting_ids)
    else:
        results = repo.race.get_race_list(db, skip=skip, limit=max_results)

    return {
        "results": results
    }
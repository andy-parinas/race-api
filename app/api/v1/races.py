from typing import Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app import repositories as repo

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def get_races(
    meeting_id: int|None = None,
    page: int = 1,
    max_results: int = 10,
    db: Session = Depends(get_db)
):
    skip = (page -1) * max_results

    return repo.race.get_race_list(db, skip=skip, limit=max_results, meeting_id=meeting_id)
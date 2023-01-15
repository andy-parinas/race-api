from typing import Optional
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.schemas.meeting import MeetingListResults
from app import repositories as repo
from app.db.session import get_db


router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=MeetingListResults)
def get_meetings(
    page: Optional[int] = 1,
    max_results: Optional[int] = 10,
    db:Session = Depends(get_db)
):
    offset = (page - 1) * max_results
    results = repo.meeting.get_many(db, skip=offset, limit=max_results)

    return {"results": list(results)}
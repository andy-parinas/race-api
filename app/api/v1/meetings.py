from typing import Optional
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.schemas.meeting import MeetingListResults, MeetingQuery
from app import repositories as repo
from app.db.session import get_db


router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def get_meetings(
    state: Optional[str] = None,
    date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    meetings = repo.meeting.get_meetings(db, date=date, state=state, limit=10)
    return meetings


# @router.post("/", status_code=status.HTTP_200_OK, response_model=MeetingListResults)
# @router.post("/", status_code=status.HTTP_200_OK)
# def get_meetings(
#     query_in: MeetingQuery,
#     db:Session = Depends(get_db)
# ):
#     offset = (query_in.page - 1) * query_in.max_results
#     results = repo.meeting.get_many(db, skip=offset, limit=query_in.max_results, state=query_in.state)

#     return {"results": list(results)}

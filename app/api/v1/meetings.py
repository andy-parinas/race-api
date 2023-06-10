from typing import Optional, Annotated
from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.orm import Session

from app.schemas.meeting import MeetingQuery
from app.schemas.race import MeetingListResults
from app import repositories as repo
from app.db.session import get_db


router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=MeetingListResults)
def get_meetings(
    state: Annotated[str | None, Query(
        description="State where meeting is held")] = None,
    date: Annotated[str | None, Query(
        description="Meeting Date. example: 2023-12-31")] = None,
    page: Annotated[int | None, Query(
        description="Page number")] = 1,
    max_results: Annotated[int | None, Query(
        description="Max number of results")] = 10,
    db: Session = Depends(get_db)
):

    skip = (page - 1) * max_results

    meetings = repo.meeting.get_meetings(
        db, date=date, state=state, limit=max_results, skip=skip)
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

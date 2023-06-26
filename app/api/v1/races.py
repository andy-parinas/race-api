import re
from typing import Optional, Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Query, Path
from sqlalchemy.orm import Session

from app.db.session import get_db
from app import repositories as repo
from app.schemas.meeting import MeetingData
from app.schemas.race import RaceListResults

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=RaceListResults)
def get_races(
    meeting_id: Annotated[int | None, Query(
        description="The Meeting ID")] = None,
    datetime: Annotated[str | None, Query(
        description="Date and Time of the Race. ex: 2023-12-31-16-30")] = None,
    datetime_end: Annotated[str | None, Query(
        description="Date and Time of the Race when using between")] = None,
    date_filter: Annotated[str | None, Query(
        description="Filter use when working with dates (eq, gt, lt, gte, lte, bet)")] = None,
    order_by: Annotated[str | None, Query(
        description="Property to order")] = "date_time",
    direction: Annotated[str | None, Query(
        description="Direction of ordering")] = "asc",
    page: Annotated[int | None, Query(
        description="Page number")] = 1,
    max_results: Annotated[int | None, Query(
        description="Max number of results")] = 10,
    db: Session = Depends(get_db)
):
    skip = (page - 1) * max_results

    """
    validate the query parameters
    """
    datetime = validate_datetime_param(datetime) if datetime else None

    datetime_end = validate_datetime_param(
        datetime_end) if datetime_end else None

    order_by = validate_order_by(order_by) if order_by else None

    direction = validate_direction(direction) if direction else None

    date_filter = validate_date_filter(date_filter) if date_filter else None

    races = repo.race.get_races(db, meeting_id=meeting_id, date_time=datetime, datetime_end=datetime_end,
                                date_filter=date_filter, order_by=order_by, direction=direction, skip=skip, limit=max_results)

    return races


@router.get("/{race_id}", status_code=status.HTTP_200_OK)
def get_race(
    race_id: Annotated[int, Path(description="The Id of the Race to get")],
    horse_id: Annotated[int | None, Query(description="Horse Id")] = None,
    db: Session = Depends(get_db)
):
    if not horse_id:
        race = repo.race.get_race_by_id(db, id=race_id)
    else:
        race = repo.horse_race_info.get_horse_race_info(
            db, race_id=race_id, horse_id=horse_id)

    if not race:
        raise HTTPException(status_code=404, detail="Not found.")

    return race


def validate_datetime_param(datetime_param: str) -> str:

    datetime_regex = r"\d{4}-\d{2}-\d{2}-\d{2}-\d{2}"
    if not re.match(datetime_regex, datetime_param):
        raise HTTPException(
            status_code=400, detail="Invalid datetime format. Expected format: YYYY-MM-DD-HH-MM")

    return datetime_param


def validate_order_by(order_by: str) -> str:
    valid_fields = ["id", "race_id", "date_time", "distance", "race_number"]
    if order_by not in valid_fields:
        raise HTTPException(status_code=400, detail="Invalid order_by field.")
    return order_by


def validate_direction(direction: str) -> str:
    valid_directions = ["asc", "desc"]
    if direction not in valid_directions:
        raise HTTPException(status_code=400, detail="Invalid direction value.")
    return direction


def validate_date_filter(date_filter: str) -> str:
    valid_filter = ["eq", "gt", "gteq", "lt", "lteq", "bet"]
    if date_filter not in valid_filter:
        raise HTTPException(
            status_code=400, detail="Invalid date_filter value.")

    return date_filter

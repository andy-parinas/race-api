import re
from typing import Optional
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app import repositories as repo
from app.schemas.meeting import MeetingData

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def get_races(
    meeting_id: Optional[int] = None,
    datetime: Optional[str] = None,
    datetime_end: Optional[str] = None,
    date_filter: Optional[str] = None,
    order_by: Optional[str] = "date_time",
    direction: Optional[str] = "asc",
    page: int = 1,
    max_results: int = 10,
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


def validate_datetime_param(datetime_param: str) -> str:

    datetime_regex = r"\d{4}-\d{2}-\d{2}-\d{2}_\d{2}_\d{2}"
    if not re.match(datetime_regex, datetime_param):
        raise HTTPException(
            status_code=400, detail="Invalid datetime format. Expected format: YYYY-MM-DD-HH_MM_SS")

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

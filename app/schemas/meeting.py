from typing import Sequence, List, Optional
from datetime import date
from pydantic import BaseModel


class MeetingBase(BaseModel):
    track_name: str
    track_id: str
    track_surface: str
    location: str
    state: str
    date: date


class MeetingQuery(BaseModel):
    state: Optional[str]
    page: int = 1
    max_results: int = 10

class MeetingCreate(MeetingBase):
    ...


class MeetingInDbBase(MeetingBase):
    id: int

    class Config:
        orm_mode = True


class Meeting(MeetingInDbBase):
    ...

class MeetingListResults(BaseModel):
    results: Sequence[Meeting]


class MeetingData(BaseModel):
    meeting_ids: List[int]
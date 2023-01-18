from typing import Sequence, List
from datetime import date
from pydantic import BaseModel


class MeetingBase(BaseModel):
    track_name: str
    track_id: str
    track_surface: str
    location: str
    state: str
    meeting_date: date


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
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


from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from app.schemas.meeting import Meeting


class RaceBase(BaseModel):
    race_id: str
    name: str
    date_time: Optional[datetime]
    race_number: int
    distance: int


class RaceCreate(RaceBase):
    meeting_id: int


class RaceInDb(RaceBase):
    id: int
    # created_at: datetime
    # updated_at: datetime

    class Config:
        orm_mode = True


class Race(RaceInDb):
    ...


class RaceWithMeeting(Race):
    meeting: Meeting

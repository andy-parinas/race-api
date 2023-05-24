from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


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

    class Config:
        orm_mode = True

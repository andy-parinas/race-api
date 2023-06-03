from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class TrackBase(BaseModel):
    track_id: Optional[int]
    name: Optional[str]
    location: Optional[str]
    state: Optional[str]


class TrackData(TrackBase):
    ...


class TrackCreate(TrackData):
    track_id: int
    name: str
    location: str
    state: str


class TrackUpdate(TrackData):
    ...


class TrackInDb(TrackBase):
    id: int
    # created_at: datetime
    # updated_at: datetime

    class Config:
        orm_mode = True


class Track(TrackInDb):
    ...

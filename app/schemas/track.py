from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class TrackBase(BaseModel):
    track_id: str
    name: str
    location: str
    state: str


class TrackCreate(TrackBase):
    ...


class TrackUpdate(TrackBase):
    ...


class TrackData(TrackBase):
    ...


class TrackInDb(TrackBase):
    id: int
    # created_at: datetime
    # updated_at: datetime

    class Config:
        orm_mode = True


class Track(TrackInDb):
    ...

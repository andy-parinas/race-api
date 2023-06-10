from enum import Enum
from typing import Sequence, List, Optional
from datetime import date
from pydantic import BaseModel

from app.schemas.track import Track
# from app.schemas.race import Race


class TrackSurface(str, Enum):
    D = "Dirt"
    G = "Grass"
    S = "Sand"
    Y = "Synthetic"
    W = "Wood Chip"
    A = "Grass Hidirt"
    B = "Grass Hisand"
    C = "Grass Hiwood Chip"


class MeetingBase(BaseModel):
    track_id: int
    track_surface: Optional[str]
    date: date


class MeetingQuery(BaseModel):
    state: Optional[str]
    page: int = 1
    max_results: int = 10


class MeetingCreate(MeetingBase):
    ...


class MeetingUpdate(MeetingBase):
    ...


class MeetingData(MeetingBase):
    ...


class MeetingInDbBase(MeetingBase):
    id: int
    # created_at: date
    # updated_at: date

    class Config:
        orm_mode = True


class Meeting(MeetingInDbBase):
    track: Track


# class MeetingData(BaseModel):
#     meeting_ids: List[int]

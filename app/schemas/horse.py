from datetime import datetime
from typing import Sequence, List
from pydantic import BaseModel

from app.schemas.horse_race_stats import HorseRaceStat


class HorseBase(BaseModel):
    horse_name: str
    horse_id: str
    # race_id: int


class HorseCreate(HorseBase):
    ...


class HorseData(HorseBase):
    ...


class HorseInDbBase(HorseBase):
    id: int
    # created_at: datetime
    # updated_at: datetime

    class Config:
        orm_mode = True


class Horse(HorseInDbBase):
    ...


class HorseWithStats(Horse):
    stats: List[HorseRaceStat]


class HorseResult(HorseInDbBase):
    rating: float


class HorseListResult(BaseModel):
    results: Sequence[HorseResult]

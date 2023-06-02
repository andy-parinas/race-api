from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class HorseRaceStatsBase(BaseModel):
    stat: Optional[str]
    total: Optional[int]
    first: Optional[int]
    second: Optional[int]
    third: Optional[int]
    win_ratio: Optional[float]
    horse_id: Optional[int]
    race_id: Optional[int]


class HorseRaceStatsData(HorseRaceStatsBase):
    stat: str
    total: int
    first: int
    second: int
    third: int
    win_ratio: Optional[float]


class HorseRaceStatsCreate(HorseRaceStatsData):
    horse_id: int
    race_id: int


class HorseRaceStatsInDb(HorseRaceStatsBase):
    id: int
    # created_at: datetime
    # updated_at: datetime

    class Config:
        orm_mode = True


class HorseRaceStat(HorseRaceStatsInDb):
    ...


class HorseRaceStatsList(BaseModel):
    ...

from datetime import datetime
from pydantic import BaseModel


class HorseRaceStatsBase(BaseModel):
    stat: str
    total: int
    first: int
    second: int
    third: int
    win_ratio: float
    horse_id: int
    race_id: int

class HorseRaceStatsCreate(HorseRaceStatsBase):
    ...

class HorseRaceStatsInDb(HorseRaceStatsBase):
    id: int

    class Config:
        orm_mode = True

class HorseRaceStat(HorseRaceStatsInDb):
    ...

    

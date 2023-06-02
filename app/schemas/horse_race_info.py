from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from app.schemas.race import Race
from app.schemas.horse import Horse, HorseWithStats
from app.schemas.horse_race_stats import HorseRaceStat


class HorseRaceInfoBase(BaseModel):
    colours: str
    colours_pic: str
    last_starts: str
    jockey: str
    trainer: str
    barrier: Optional[int]
    horse_id: int
    race_id: int


class HorseRaceInfoCreate(HorseRaceInfoBase):
    ...


class HorseRaceInfoData(HorseRaceInfoBase):
    ...


class HorseRaceInfoInDb(HorseRaceInfoBase):
    id: int
    # created_at: datetime
    # updated_at: datetime

    class Config:
        orm_mode = True


class HorseRaceInfo(HorseRaceInfoInDb):
    ...


class HorseRaceInfoDetails(BaseModel):
    id: int
    race_id: int
    date_time: datetime

    class Config:
        orm_mode = True

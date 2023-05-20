from datetime import datetime
from pydantic import BaseModel


class HorseRaceInfoBase(BaseModel):
    colours: str
    colours_pic: str
    last_starts: str
    jockey: str
    trainer: str
    barrier: int
    horse_id: int
    race_id: int

class HorseRaceInfoCreate(HorseRaceInfoBase):
    ...

class HorseRaceInfoInDb(HorseRaceInfoBase):
    id: int

    class Config:
        orm_mode = True

class HorseRaceInfo(HorseRaceInfoInDb):
    ...
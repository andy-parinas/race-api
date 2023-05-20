from typing import Sequence
from pydantic import BaseModel


class HorseBase(BaseModel):
    horse_name: str
    horse_id: str


class HorseCreate(HorseBase):
    ...

class HorseInDbBase(HorseBase):
    id: int
    race_id: int

    class Config:
        orm_mode = True

class Horse(HorseInDbBase):
    ...

class HorseResult(HorseInDbBase):
    rating: float

class HorseListResult(BaseModel):
    results: Sequence[HorseResult]
from datetime import datetime
from pydantic import BaseModel


class RaceBase(BaseModel):
    race_id: str
    race_date: datetime


class RaceCreate(RaceBase):
    ...


class RaceInDb(RaceBase):
    id: int

    class Config:
        orm_mode = True


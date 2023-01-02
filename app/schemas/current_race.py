from pydantic import BaseModel


class CurrentRaceBase(BaseModel):
    stat: str
    total: int
    first: int
    second: int
    third: int
    horse_id: int
    race_id: int


class CurrentRaceCreate(CurrentRaceBase):
    ...



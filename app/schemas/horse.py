from pydantic import BaseModel


class HorseBase(BaseModel):
    horse_name: str
    horse_id: str


class HorseCreate(HorseBase):
    race_id: int

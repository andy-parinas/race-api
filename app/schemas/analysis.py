from typing import List
from pydantic import BaseModel


class Preference(BaseModel):
    first: str
    second: str
    third: str


class AnalsyisInput(BaseModel):
    race_ids: List[int]
    preference: Preference
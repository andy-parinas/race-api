from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class PreferenceType(str, Enum):
    balance = "balance"
    weighted = "weighted"

class Preference(BaseModel):
    first: str
    second: str
    third: str


class AnalsyisInput(BaseModel):
    race_ids: List[int]
    preference: Optional[Preference]
    preferences: Optional[List[str]]
    preference_type: PreferenceType

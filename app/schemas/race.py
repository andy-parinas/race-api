from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from app.schemas.meeting import Meeting
from app.schemas.horse_race_info import HorseRaceInfo
from app.schemas.horse import HorseWithStats, HorseWithStatsAndInfo


class RaceBase(BaseModel):
    race_id: str
    name: str
    date_time: Optional[datetime]
    race_number: int
    distance: int
    meeting_id: int


class RaceData(RaceBase):
    ...


class RaceCreate(RaceBase):
    ...


class RaceInDb(RaceBase):
    id: int
    # created_at: datetime
    # updated_at: datetime

    class Config:
        orm_mode = True


class Race(RaceInDb):
    ...


class RaceWithMeeting(Race):
    meeting: Meeting


class RaceDetailsWithHorseStats(Race):
    horses: List[HorseWithStatsAndInfo]


class RaceListResults(BaseModel):
    races: List[RaceWithMeeting]


class MeetingWithRaces(Meeting):
    races: List[Race]


class MeetingListResults(BaseModel):
    meetings: List[MeetingWithRaces]


class HorseRaceInfoAndStats(BaseModel):
    race: Race
    info: HorseRaceInfo
    horse: HorseWithStats


class HorseRaceInfoAndStatsList(BaseModel):
    results: List[HorseRaceInfoAndStats]

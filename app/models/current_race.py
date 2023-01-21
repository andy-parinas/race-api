from sqlalchemy import Column, String, ForeignKey, Integer, Float
from .base_class import Base


class CurrentRace(Base):
    id = Column(Integer, primary_key=True, index=True)
    stat = Column(String, nullable=False)
    total = Column(Integer)
    first = Column(Integer)
    second = Column(Integer)
    third = Column(Integer)
    horse_id = Column(Integer, ForeignKey('horse.id', name="current_race_horse_fk"), nullable=False)
    race_id = Column(Integer, ForeignKey('race.id', name="current_race_race_fk"), nullable=False)
    meeting_id = Column(Integer, ForeignKey('meeting.id', name="current_race_meeting_fk"), nullable=False)
    win_ratio = Column(Float, default=0)

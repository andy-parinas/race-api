from sqlalchemy import Column, String, ForeignKey, Integer
from .base_class import Base


class CurrentRace(Base):
    id = Column(Integer, primary_key=True, index=True)
    stat = Column(String, nullable=False)
    total = Column(Integer)
    first = Column(Integer)
    second = Column(Integer)
    third = Column(Integer)
    horse_id = Column(Integer, ForeignKey('horse.id'), nullable=False)
    race_id = Column(Integer, ForeignKey('race.id'), nullable=False)
    meeting_id = Column(Integer, ForeignKey('meeting.id'), nullable=False)

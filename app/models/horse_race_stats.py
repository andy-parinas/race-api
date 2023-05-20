from sqlalchemy import Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from .base_class import Base
from .race import Race
from .horse import Horse

class HorseRaceStats(Base):
    id = Column(Integer, primary_key=True, index=True)
    race_id = Column(Integer, ForeignKey("race.id", name="stats_race_fk"))
    horse_id = Column(Integer, ForeignKey("horse.id", name="stats_horse_fk"))
    stat = Column(String)
    total = Column(Integer)
    first = Column(Integer)
    second = Column(Integer)
    third = Column(Integer)
    win_ratio = Column(Float, default=0)
    race: Race = relationship("Races", back_populates="stats")
    horse: Horse = relationship("Horse", back_populates="stats")
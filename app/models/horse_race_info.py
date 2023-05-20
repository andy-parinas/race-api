from sqlalchemy import Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from .base_class import Base
from .race import Race
from .horse import Horse


class HorseRaceInfo(Base):
    id = Column(Integer, primary_key=True, index=True)
    race_id = Column(Integer, ForeignKey("race.id", name="info_race_fk"))
    horse_id = Column(Integer, ForeignKey("horse.id", name="info_horse_fk"))
    colours = Column(String)
    colours_pic = Column(String, nullable=True)
    trainer = Column(String)
    jockey = Column(String)
    barrier = Column(Integer, nullable=True)
    last_starts = Column(String)
    race: Race = relationship("Races", back_populates="infos")
    horse: Horse = relationship("Horse", back_populates="infos")
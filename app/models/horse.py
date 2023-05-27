from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base_class import Base


class Horse(Base):
    id = Column(Integer, primary_key=True, index=True)
    horse_name = Column(String)
    horse_id = Column(String)
    infos = relationship("HorseRaceInfo", back_populates="horse")
    stats = relationship("HorseRaceStats", back_populates="horse")

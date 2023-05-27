from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from .base_class import Base


class Horse(Base):

    __tablename__ = "horse"

    id = Column(Integer, primary_key=True, index=True)
    horse_name = mapped_column(String)
    horse_id = mapped_column(String)
    created_at = mapped_column(
        DateTime, default=datetime.now)
    updated_at = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now)
    infos = relationship("HorseRaceInfo", back_populates="horse")
    stats = relationship("HorseRaceStats", back_populates="horse")

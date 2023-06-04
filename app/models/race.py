from typing import List
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from .base_class import Base
from .meeting import Meeting


class Race(Base):

    __tablename__ = "race"

    id = mapped_column(Integer, primary_key=True, index=True)
    race_id = mapped_column(String)
    name = mapped_column(String)
    date_time = mapped_column(DateTime, nullable=True)
    race_number = mapped_column(Integer)
    distance = mapped_column(Integer)
    meeting_id = mapped_column(Integer, ForeignKey(
        "meeting.id", name="race_meeting_fk"), nullable=False)
    created_at = mapped_column(
        DateTime, default=datetime.now)
    updated_at = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now)
    meeting = relationship("Meeting", back_populates="races")
    infos: Mapped[List["HorseRaceInfo"]] = relationship(
        back_populates="race", overlaps="races")
    # stats = relationship("HorseRaceStats", back_populates="race")
    horses: Mapped[List["Horse"]] = relationship(
        secondary="horseraceinfo", back_populates="races", overlaps="infos")

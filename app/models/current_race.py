from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, Integer, Float, DateTime
from sqlalchemy.orm import relationship, mapped_column
from .base_class import Base


class CurrentRace(Base):

    __tablename__ = "current_race"

    id = mapped_column(Integer, primary_key=True, index=True)
    stat = mapped_column(String, nullable=False)
    total = mapped_column(Integer)
    first = mapped_column(Integer)
    second = mapped_column(Integer)
    third = mapped_column(Integer)
    horse_id = mapped_column(Integer, ForeignKey(
        'horse.id', name="current_race_horse_fk"), nullable=False)
    race_id = mapped_column(Integer, ForeignKey(
        'race.id', name="current_race_race_fk"), nullable=False)
    meeting_id = mapped_column(Integer, ForeignKey(
        'meeting.id', name="current_race_meeting_fk"), nullable=False)
    win_ratio = mapped_column(Float, default=0)
    created_at = mapped_column(
        DateTime, default=datetime.now)
    updated_at = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now)

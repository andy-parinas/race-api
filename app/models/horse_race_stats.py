from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, Integer, Float, DateTime
from sqlalchemy.orm import relationship, mapped_column


from .base_class import Base
from .race import Race
from .horse import Horse


class HorseRaceStats(Base):

    __tablename__ = "horseracestats"

    id = mapped_column(Integer, primary_key=True, index=True)
    race_id = mapped_column(Integer, ForeignKey(
        "race.id", name="stats_race_fk"))
    horse_id = mapped_column(Integer, ForeignKey(
        "horse.id", name="stats_horse_fk"))
    stat = mapped_column(String)
    total = mapped_column(Integer)
    first = mapped_column(Integer)
    second = mapped_column(Integer)
    third = mapped_column(Integer)
    win_ratio = mapped_column(Float, default=0)
    # race = relationship("Race", back_populates="stats")
    horse = relationship("Horse", back_populates="stats")
    created_at = mapped_column(
        DateTime, default=datetime.now)
    updated_at = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now)

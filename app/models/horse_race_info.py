from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import relationship, mapped_column
from .base_class import Base


class HorseRaceInfo(Base):

    __tablename__ = "horseraceinfo"

    id = mapped_column(Integer, primary_key=True, index=True)
    race_id = mapped_column(Integer, ForeignKey(
        "race.id", name="info_race_fk"))
    horse_id = mapped_column(Integer, ForeignKey(
        "horse.id", name="info_horse_fk"))
    colours = mapped_column(String)
    colours_pic = mapped_column(String, nullable=True)
    trainer = mapped_column(String)
    jockey = mapped_column(String)
    barrier = mapped_column(Integer, nullable=True)
    last_starts = mapped_column(String)
    race = relationship("Race", back_populates="infos")
    horse = relationship("Horse", back_populates="infos")
    created_at = mapped_column(
        DateTime, default=datetime.now)
    updated_at = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now)

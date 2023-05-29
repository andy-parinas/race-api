from typing import List
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
    infos: Mapped[List["HorseRaceInfo"]] = relationship(back_populates="horse",
                                                        primaryjoin="and_(HorseRaceInfo.horse_id == Horse.id, Race.id == HorseRaceInfo.race_id )")
    stats: Mapped[List["HorseRaceStats"]] = relationship(back_populates="horse",
                                                         primaryjoin="and_(HorseRaceStats.horse_id == Horse.id, Race.id == HorseRaceStats.race_id )")
    races: Mapped[List["Race"]] = relationship(
        secondary="horseraceinfo", back_populates="horses", overlaps="infos")

    #  infos: Mapped[List["HorseRaceInfo"]] = relationship(back_populates="horse",
    #                                                     primaryjoin="and_(HorseRaceInfo.horse_id == Horse.id, Race.id == HorseRaceInfo.race_id )")
    # stats: Mapped[List["HorseRaceStats"]] = relationship(back_populates="horse",
    #                                                      primaryjoin="and_(HorseRaceStats.horse_id == Horse.id, Race.id == HorseRaceStats.race_id )")

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base_class import Base
from .meting import Meeting


class Race(Base):
    id = Column(Integer, primary_key=True, index=True)
    race_id = Column(String)
    name = Column(String)
    date_time = Column(DateTime, nullable=True)
    race_number = Column(Integer)
    distance = Column(Integer)
    meeting_id = Column(Integer, ForeignKey(
        "meeting.id", name="race_meeting_fk"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    meeting: Meeting = relationship("Meeting", back_populates="races")
    # horses = relationship("Horse", back_populates="race")
    infos = relationship("HorseRaceInfo", back_populates="race")
    stats = relationship("HorseRaceStats", back_populates="race")

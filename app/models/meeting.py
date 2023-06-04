from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from .base_class import Base


class Meeting(Base):

    __tablename__ = "meeting"

    id = mapped_column(Integer, primary_key=True, index=True)
    track_surface = mapped_column(String)
    date = mapped_column(Date)
    track_id: Mapped[int] = mapped_column(ForeignKey(
        "track.id", name="meeting_track_fk"))
    created_at = mapped_column(
        DateTime, default=datetime.now)
    updated_at = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now)
    races = relationship("Race", back_populates="meeting")
    track = relationship("Track", back_populates="meetings")

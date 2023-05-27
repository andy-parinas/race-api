from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, mapped_column

from .base_class import Base


class Track(Base):

    __tablename__ = "track"

    id = mapped_column(Integer, primary_key=True, index=True)
    track_id = mapped_column(Integer)
    name = mapped_column(String)
    location = mapped_column(String)
    state = mapped_column(String)
    created_at = mapped_column(
        DateTime, default=datetime.now)
    updated_at = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now)
    meetings = relationship("Meeting", back_populates="track")

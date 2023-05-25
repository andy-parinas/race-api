from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base_class import Base


class Meeting(Base):
    id = Column(Integer, primary_key=True, index=True)
    track_surface = Column(String)
    date = Column(Date)
    track_id = Column(Integer, ForeignKey("track.id", name="meeting_track_fk"))
    races = relationship("Race", back_populates="meeting")
    track = relationship("Track", back_populates="meetings")

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .base_class import Base


class Track(Base):
    id = Column(Integer, primary_key=True, index=True)
    track_id = Column(Integer)
    name = Column(String)
    location = Column(String)
    state = Column(String)
    meetings = relationship("Meeting", back_populates="track")

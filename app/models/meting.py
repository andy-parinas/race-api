from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from .base_class import Base


class Meeting(Base):
    id = Column(Integer, primary_key=True, index=True)
    track_name = Column(String, index=True)
    track_id = Column(String)
    track_surface = Column(String)
    location = Column(String)
    state = Column(String)
    date = Column(Date)
    races = relationship("Race", back_populates="meeting")
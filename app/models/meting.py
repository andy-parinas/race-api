from sqlalchemy import Column, Integer, String, Date
from .base_class import Base


class Meeting(Base):
    id = Column(Integer, primary_key=True, index=True)
    track_name = Column(String, index=True)
    track_id = Column(String)
    track_surface = Column(String)
    location = Column(String)
    state = Column(String)
    meeting_date = Column(Date)
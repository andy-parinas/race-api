from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base_class import Base
from .meting import Meeting

class Race(Base):
    id = Column(Integer, primary_key=True, index=True)
    race_id = Column(String)
    race_date = Column(DateTime)
    race_number = Column(Integer)
    distance = Column(Integer)
    meeting_id = Column(Integer, ForeignKey("meeting.id", name="race_meeting_fk"), nullable=False)
    meeting: Meeting = relationship("Meeting", back_populates="races")
    horses = relationship("Horse", back_populates="race")

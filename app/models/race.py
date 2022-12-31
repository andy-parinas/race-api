from sqlalchemy import Column, Integer, String, DateTime

from .base_class import Base


class Race(Base):
    id = Column(Integer, primary_key=True, index=True)
    race_id = Column(String)
    race_date = Column(DateTime)
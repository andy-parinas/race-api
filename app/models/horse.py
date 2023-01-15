from sqlalchemy import Column, Integer, String, ForeignKey
from .base_class import Base


class Horse(Base):
    id = Column(Integer, primary_key=True, index=True)
    horse_name = Column(String)
    horse_id = Column(String)
    race_id = Column(Integer, ForeignKey("race.id"))

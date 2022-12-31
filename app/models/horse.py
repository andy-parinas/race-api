from sqlalchemy import Column, Integer, String
from .base_class import Base


class Horse(Base):
    id = Column(Integer, primary_key=True, index=True)
    horse_name = Column(String)
    horse_id = Column(String)

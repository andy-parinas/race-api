from sqlalchemy import Column, String, ForeignKey, Integer, Float, Boolean
from .base_class import Base


class FormFiles(Base):
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    is_processed = Column(Boolean, default=0)
    is_uploaded = Column(Boolean, default=0)
    timestamp = Column(Integer, nullable=False)

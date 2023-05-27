from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Boolean, DateTime
from sqlalchemy.orm import mapped_column
from .base_class import Base


class FormFiles(Base):

    __tablename__ = "formfiles"

    id = mapped_column(Integer, primary_key=True, index=True)
    file_name = mapped_column(String, nullable=False)
    is_processed = mapped_column(Boolean, default=0)
    is_uploaded = mapped_column(Boolean, default=0)
    timestamp = mapped_column(Integer, nullable=False)
    created_at = mapped_column(
        DateTime, default=datetime.now)
    updated_at = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now)

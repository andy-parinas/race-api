from typing import List
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, mapped_column, Mapped
from .base_class import Base
from .meeting import Meeting


class ScratchFiles(Base):
    __tablename__ = "scratch_files"

    id = mapped_column(Integer, primary_key=True, index=True)
    file_name = mapped_column(String, nullable=False)
    is_processed = mapped_column(Boolean, default=0)
    is_uploaded = mapped_column(Boolean, default=0)
    timestamp = mapped_column(Integer, nullable=False)
    created_at = mapped_column(
        DateTime, default=datetime.now)
    updated_at = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now)
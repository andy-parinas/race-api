import typing as t
from datetime import datetime
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class_registry: t.Dict = {}


@as_declarative(class_registry=class_registry)
class Base:
    id: t.Any
    __name__: str
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

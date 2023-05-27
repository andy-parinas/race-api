import typing as t
from datetime import datetime
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column

class_registry: t.Dict = {}


class Base(DeclarativeBase):
    ...
    # created_at: Mapped[datetime] = mapped_column(
    #     DateTime, default=datetime.now)
    # updated_at: Mapped[datetime] = mapped_column(
    #     DateTime, default=datetime.now, onupdate=datetime.now)

    # def __tablename__(cls) -> str:
    #     return cls.__name__.lower()

    # __table_args__ = {'extend_existing': True}


# @as_declarative(class_registry=class_registry)
# class Base:
#     id: t.Any
#     __name__: str
#     created_at = Column(DateTime, default=datetime.now)
#     updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

#     @declared_attr
#     def __tablename__(cls) -> str:
#         return cls.__name__.lower()

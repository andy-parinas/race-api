from typing import List
from sqlalchemy.orm import Session

from app.models.meting import Meeting
from app.schemas.meeting import MeetingCreate


class MeetingRepository:

    def create(self, db: Session, meeting_in: MeetingCreate) -> Meeting:
        meeting_obj = meeting_in.dict()
        db_obj = Meeting(**meeting_obj)

        db.add(db_obj)
        db.commit()
        return db_obj

    def get_many(self, db: Session, *, skip:int = 0, limit:int = 0) -> List[Meeting]:
        return db.query(Meeting).offset(skip).limit(limit).all()


meeting = MeetingRepository()

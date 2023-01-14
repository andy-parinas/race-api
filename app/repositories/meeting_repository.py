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


meeting = MeetingRepository()

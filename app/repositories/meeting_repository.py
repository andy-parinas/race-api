from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session, joinedload

from app.models.meting import Meeting
from app.models.track import Track
from app.schemas.meeting import MeetingCreate


class MeetingRepository:

    def create(self, db: Session, meeting_in: MeetingCreate) -> Meeting:
        meeting_obj = meeting_in.dict()
        db_obj = Meeting(**meeting_obj)

        db.add(db_obj)
        db.commit()
        return db_obj

    def get_meetings(self, db: Session, *,  skip: int = 0, limit: int = 0,
                     state: Optional[str] = None, date: Optional[str] = None) -> List[Meeting]:

        query = db.query(Meeting).options(joinedload(
            Meeting.track)).options(joinedload(Meeting.races))

        if state is not None:
            query = query.filter(Meeting.track.has(state=state))

        if date is not None:
            query_date = datetime.strptime(date, '%Y-%m-%d').date()
            query = query.filter(Meeting.date == query_date)

        return query.offset(skip).limit(limit).all()

    def get_meeting_by_track_id_and_date(self, db: Session, track_id: int, date: str) -> Optional[Meeting]:
        query = db.query(Meeting).options(joinedload(Meeting.track)).filter(
            Meeting.track.id == track_id, Meeting.date == date)
        return query.first()


meeting = MeetingRepository()

from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, update

from app.models.meting import Meeting
from app.models.track import Track
from app.schemas.meeting import MeetingCreate, MeetingData, Meeting as MeetingSchema


class MeetingRepository:

    def create(self, db: Session, meeting_in: MeetingData) -> MeetingSchema:
        meeting_obj = meeting_in.dict()
        db_obj = Meeting(**meeting_obj)

        db.add(db_obj)
        db.commit()
        return MeetingSchema.from_orm(db_obj)

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

    def get_meeting(self, db: Session, track_id, date: datetime):
        stmt = select(Meeting).where(Meeting.track_id ==
                                     track_id, Meeting.date == date)

        meeting = db.scalars(stmt).first()

        if not meeting:
            return None

        return MeetingSchema.from_orm(meeting)

    def update_meeting(self, db: Session, id: int, meeting_data: MeetingData):
        stmt = (update(Meeting)
                .where(Meeting.id == id)
                .values(track_id=meeting_data.track_id, track_surface=meeting_data.track_surface, date=meeting_data.date)
                )

        db.execute(stmt)
        db.commit()


meeting = MeetingRepository()

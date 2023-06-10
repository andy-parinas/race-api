from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, update

from app.models.meeting import Meeting
from app.models.track import Track
from app.models.race import Race
from app.schemas.meeting import MeetingCreate, MeetingData, Meeting as MeetingSchema
from app.schemas.race import MeetingWithRaces, MeetingListResults


class MeetingRepository:

    def create(self, db: Session, meeting_in: MeetingData) -> MeetingSchema:
        meeting_obj = meeting_in.dict()
        db_obj = Meeting(**meeting_obj)

        db.add(db_obj)
        db.commit()
        return MeetingSchema.from_orm(db_obj)

    def get_meetings(self, db: Session, *,  skip: int = 0, limit: int = 0,
                     state: Optional[str] = None, date: Optional[str] = None) -> List[Meeting]:

        stmt = select(Meeting, Track).join(
            Track).options(joinedload(Meeting.races))

        if state is not None:
            stmt = stmt.where(Meeting.track.has(state=state))

        if date is not None:
            query_date = datetime.strptime(date, '%Y-%m-%d').date()
            stmt = stmt.where(Meeting.date == query_date)

        stmt = stmt.offset(skip).limit(limit)

        results = db.execute(stmt).unique().all()

        meetings = []
        for result in results:
            meeting, track = result
            meetings.append(MeetingWithRaces.from_orm(meeting))

        return MeetingListResults(meetings=meetings)

    def get_meeting_by_track_id_and_date(self, db: Session, track_id: int, date: str) -> Optional[Meeting]:
        query = db.query(Meeting).options(joinedload(Meeting.track)).filter(
            Meeting.track.id == track_id, Meeting.date == date)
        return query.first()

    def get_meeting(self, db: Session, track_id, date: str):
        stmt = select(Meeting).where(Meeting.track_id ==
                                     track_id).where(Meeting.date == date)

        meeting = db.scalars(stmt).first()

        if not meeting:
            return None

        return MeetingSchema.from_orm(meeting)

    def update_meeting(self, db: Session, id: int, meeting_data: MeetingData):
        stmt = (update(Meeting).returning(Meeting)
                .where(Meeting.id == id)
                .values(track_id=meeting_data.track_id, track_surface=meeting_data.track_surface, date=meeting_data.date)
                )

        meeting = db.scalars(stmt).first()

        return MeetingSchema.from_orm(meeting)


meeting = MeetingRepository()

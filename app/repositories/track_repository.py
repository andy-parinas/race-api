from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select, update

from app.schemas.track import TrackCreate, TrackData, Track as TrackSchema
from app.models.track import Track


class TrackRepository:

    def create(self, db: Session, track_in: TrackData) -> TrackSchema:
        track_obj = track_in.dict()
        db_obj = Track(**track_obj)

        db.add(db_obj)
        db.commit()
        return TrackSchema.from_orm(db_obj)

    def get_track(self, db: Session, track_id: int, track_name: str = None):
        stmt = select(Track).where(Track.track_id == track_id)

        if track_name:
            stmt = stmt.where(Track.name == track_name)

        track = db.scalars(stmt).first()

        if not track:
            return None

        return TrackSchema.from_orm(track)

    def update_track(self, db: Session, id: int, track_data: TrackData):
        stmt = (update(Track)
                .where(Track.id == id)
                .values(track_id=track_data.track_id,
                        name=track_data.name,
                        location=track_data.location,
                        state=track_data.state)
                )

        db.execute(stmt)
        db.commit()


track = TrackRepository()

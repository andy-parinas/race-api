from typing import List
from sqlalchemy.orm import Session

from app.schemas.track import TrackCreate, Track as TrackSchema
from app.models.track import Track


class TrackRepository:

    def create(self, db: Session, track_in: TrackCreate) -> TrackSchema:
        track_obj = track_in.dict()
        db_obj = Track(**track_obj)

        db.add(db_obj)
        db.commit()
        return TrackSchema.from_orm(db_obj)


track = TrackRepository()

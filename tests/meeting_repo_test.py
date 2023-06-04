from datetime import datetime
from app.schemas.track import TrackData
from sqlalchemy.orm import Session
from app import repositories as repo
from app.schemas.meeting import MeetingData, Meeting

from .setup import test_db, track_data, meeting_data


def test_can_create_meeting(test_db, track_data):

    meeting_data = MeetingData(
        track_id=track_data.id,
        track_surface="G",
        date=datetime.strptime("2023-01-01", "%Y-%m-%d")
    )

    meeting = repo.meeting.create(db=test_db, meeting_in=meeting_data)

    assert meeting is not None
    assert isinstance(meeting, Meeting)


def test_can_get_meeting(test_db, meeting_data):

    meeting = repo.meeting.get_meeting(
        db=test_db, track_id=meeting_data.track_id, date="2023-01-01")

    assert meeting is not None
    assert isinstance(meeting, Meeting)


def test_can_update_meeting():
    pass

from datetime import datetime
from app.schemas.track import TrackData
from sqlalchemy.orm import Session
from app import repositories as repo
from app.schemas.meeting import MeetingData, Meeting
from app.schemas.race import MeetingWithRaces

from app import models

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


def test_can_get_meeting_by_id(test_db, meeting_data: models.Meeting):
    meeting = repo.meeting.get_mmeting_by_id(db=test_db, id=meeting_data.id)

    assert meeting is not None
    assert isinstance(meeting, MeetingWithRaces)


def test_can_update_meeting(test_db, meeting_data: models.Meeting):

    updated_meeting = repo.meeting.update_meeting(db=test_db, id=meeting_data.id, meeting_data=MeetingData(
        track_id=meeting_data.track_id,
        track_surface="U",
        date=datetime.strptime("2023-12-31", "%Y-%m-%d")
    ))

    assert updated_meeting is not None
    assert isinstance(updated_meeting, Meeting)
    assert updated_meeting.track_surface == "U"
    assert updated_meeting.date.strftime("%Y-%m-%d") == "2023-12-31"

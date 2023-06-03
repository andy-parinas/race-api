from app.schemas.track import TrackData
from sqlalchemy.orm import Session
from app import repositories as repo
from app.schemas.track import Track

from .setup import test_db


def test_can_create_track(test_db):
    track_data = TrackData(
        track_id=100,
        name="Track Name",
        location="L",
        state="QLD"
    )

    track = repo.track.create(db=test_db, track_in=track_data)

    assert track is not None
    assert isinstance(track, Track)


def test_can_get_track(test_db):
    track = repo.track.get_track(
        db=test_db, track_id=100, track_name="Track Name")

    assert track is not None
    assert isinstance(track, Track)


def test_can_update_track(test_db):
    track = repo.track.get_track(
        db=test_db, track_id=100, track_name="Track Name")

    updeated_track = repo.track.update_track(db=test_db, id=track.id, track_data=TrackData(
        track_id=200,
        name="Updated Name",
        location="U",
        state="NSW"
    ))

    assert updeated_track.track_id == 200
    assert updeated_track.name == "Updated Name"
    assert updeated_track.location == "U"
    assert updeated_track.state == "NSW"

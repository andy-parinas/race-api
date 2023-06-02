from typing import Optional
from datetime import datetime, date
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app import repositories as repo
from .xml_parser import XmlParser
from .image_download import image_download
from .s3_client import S3Client

from app.schemas.meeting import MeetingCreate, MeetingData
from app.schemas.race import RaceCreate, RaceData
from app.schemas.horse import HorseCreate, HorseData
from app.schemas.horse_race_info import HorseRaceInfoCreate, HorseRaceInfoData
from app.schemas.horse_race_stats import HorseRaceStatsCreate, HorseRaceStatsData
from app.schemas.track import TrackCreate, TrackUpdate, TrackData
from app.settings import settings


def load_db(file, update=False):
    print("Loading file to DB...")
    allowed_stat = ['all', 'track', 'distance', 'distance_track',
                    'firm', 'good', 'soft', 'heavy', 'synthetic',
                    'first_up', 'second_up', 'current_jockey'
                    ]

    s3_client = S3Client(settings.S3_REGION, settings.IMAGE_BUCKET)

    xml_file = file
    parser = XmlParser(xml_file)
    db: Session = SessionLocal()

    meeting_date = parser.get_meeting_date()
    meeting_xml_data = parser.get_meeting_data()

    track_data = TrackData(
        name=meeting_xml_data['track_name'],
        track_id=meeting_xml_data['track_id'],
        location=meeting_xml_data['location'],
        state=meeting_xml_data['state'],
    )

    track = process_track_data(db, track_data)

    meeting = process_meeting_data(db, MeetingData(
        track_id=track.id,
        track_surface=meeting_xml_data['track_surface'],
        date=datetime.strptime(meeting_xml_data['meeting_date'], "%d/%m/%Y")
    ))

    races = parser.get_races()
    for race in races:
        start_time = parser.get_race_start_time(race)

        race_db = process_race_data(db, RaceData(
            race_id=race['id'],
            race_number=int(race['number']),
            name=race['name'],
            meeting_id=meeting.id,
            date_time=datetime.strptime(
                f"{meeting_date} {start_time}", "%d/%m/%Y %I:%M%p") if start_time is not None else None,
            distance=parser.get_race_distance(race),
        ))

        horses = parser.get_race_horses(race)
        for horse in horses:

            horse_db = process_horse_data(db, HorseData(
                horse_id=horse['id'],
                horse_name=horse['name'],
                race_id=race_db.id
            ))

            process_horse_race_info_data(db, HorseRaceInfoData(
                horse_id=horse_db.id,
                race_id=race_db.id,
                jockey=parser.get_horse_jockey(horse),
                trainer=parser.get_horse_trainer(horse),
                last_starts=parser.get_last_starts(horse),
                colours=parser.get_horse_colours(horse),
                colours_pic=upload_horse_colours(
                    s3_client, parser.get_horse_colours_image(horse)),
                barrier=parser.get_horse_barrier(horse)
            ))

            statistics = parser.get_horse_stats(horse)
            for stat in statistics:
                if stat['type'] in allowed_stat:
                    process_horse_race_stats_data(db, HorseRaceStatsData(
                        stat=stat['type'],
                        total=int(stat['total']),
                        first=int(stat['firsts']),
                        second=int(stat['seconds']),
                        third=int(stat['thirds']),
                        horse_id=horse_db.id,
                        race_id=race_db.id,
                    ))

    print("File Loaded to DB Successfully.")


def process_track_data(db: Session, track_data: TrackData):

    track = repo.track.get_track(
        db, track_id=track_data.track_id, track_name=track_data.name)

    if track:
        repo.track.update_track(db, track.id, track_data=track_data)

    else:
        track = repo.track.create(db, track_in=track_data)

    return track


def process_meeting_data(db: Session, meeting_data: MeetingData):
    meeting = repo.meeting.get_meeting(
        db, track_id=meeting_data.track_id, date=meeting_data.date)

    if meeting:
        repo.meeting.update_meeting(
            db, meeting.id, meeting_data=meeting_data)

    elif not meeting:
        meeting = repo.meeting.create(db, meeting_in=meeting_data)

    return meeting


def process_race_data(db: Session, race_data: RaceData):
    race_db = repo.race.get_race(
        db, race_id=race_data.race_id, meeting_id=race_data.meeting_id)

    if race_db:
        repo.race.update_race(db, id=race_db.id, race_data=race_data)

    else:
        race_db = repo.race.create(db, race_in=race_data)

    return race_db


def process_horse_data(db: Session, horse_data: HorseData):

    horse_db = repo.horse.get_horse_from_horse_id(db, horse_data.horse_id)

    if horse_db is None:
        horse_db = repo.horse.create(db, horse_in=horse_data)

    return horse_db


def process_horse_race_info_data(db: Session, info_data: HorseRaceInfoData):

    info = repo.horse_race_info.get_horse_race_info(
        db, race_id=info_data.race_id, horse_id=info_data.horse_id)

    if info:
        repo.horse_race_info.update_horse_race_info(db, info.id, info_data)

    else:
        info = repo.horse_race_info.create(db, info_data)

    return info


def process_horse_race_stats_data(db: Session, stats_data: HorseRaceStatsData):

    stats = repo.horse_race_stats.get_horse_race_stats(
        db, stats_data.race_id, stats_data.horse_id, stats_data.stat)

    if stats:
        repo.horse_race_stats.update_horse_race_stats(db, stats.id, stats_data)
    else:
        stats = repo.horse_race_stats.create(db,  stats_data)

    return stats


def upload_horse_colours(s3_client, colours_data):
    image_data, filename = image_download(colours_data)

    colours_image = ""
    if image_data and filename:
        uploaded = s3_client.upload_image(
            image_data, settings.IMAGE_FOLDER, filename)
        if uploaded:
            s3_client.make_object_public(
                settings.IMAGE_FOLDER, filename)
            colours_image = f"{settings.IMAGE_URL}/{filename}"

    return colours_image


# def test_data(file):
#     xml_file = file
#     parser = XmlParser(xml_file)
#     races = parser.get_races()
#     for race in races:
#         horses = parser.get_race_horses(race)
#         for horse in horses:

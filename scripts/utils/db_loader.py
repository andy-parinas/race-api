from datetime import datetime, date
from app.db.session import SessionLocal
from app import repositories as repo
from .xml_parser import XmlParser

from app.schemas.meeting import MeetingCreate
from app.schemas.race import RaceCreate
from app.schemas.horse import HorseCreate
from app.schemas.horse_race_info import HorseRaceInfoCreate
from app.schemas.horse_race_stats import HorseRaceStatsCreate


def load_db(file, update=False):
    print("Loading file to DB...")
    allowed_stat = ['all', 'track', 'distance', 'distance_track',
                    'firm', 'good', 'soft', 'heavy', 'synthetic',
                    'first_up', 'second_up', 'current_jockey'
                    ]

    xml_file = file
    parser = XmlParser(xml_file)
    races = parser.get_races()
    db = SessionLocal()
    meeting_date = parser.get_meeting_date()
    meeting_data = parser.get_meeting_data()

    meeting = repo.meeting.create(db, meeting_in=MeetingCreate(
        track_name=meeting_data['track_name'],
        track_id=meeting_data['track_id'],
        track_surface=meeting_data['track_surface'],
        location=meeting_data['location'],
        state=meeting_data['state'],
        date=datetime.strptime(meeting_data['meeting_date'], "%d/%m/%Y")
    ))

    for race in races:
        start_time = parser.get_race_start_time(race)
        race_db = repo.race.create(
            db,
            RaceCreate(
                race_id=race['id'],
                race_number=int(race['number']),
                name=race['name'],
                meeting_id=meeting.id,
                date_time=datetime.strptime(
                    f"{meeting_date} {start_time}", "%d/%m/%Y %I:%M%p") if start_time is not None else None,
                distance=parser.get_race_distance(race),
            )
        )

        horses = parser.get_race_horses(race)
        for horse in horses:

            horse_db = repo.horse.get_horse_from_horse_id(db, horse['id'])

            if horse_db is None:

                horse_db = repo.horse.create(
                    db,
                    HorseCreate(
                        horse_id=horse['id'],
                        horse_name=horse['name'],
                        race_id=race_db.id
                    )
                )

            horse_jockey = parser.get_horse_jockey(horse)
            horse_trainer = parser.get_horse_trainer(horse)
            last_starts = parser.get_last_starts(horse)
            colours = parser.get_horse_colours(horse)
            colours_image = parser.get_horse_colours_image(horse)
            barrier = parser.get_horse_barrier(horse)

            repo.horse_race_info.create(db, HorseRaceInfoCreate(
                horse_id=horse_db.id,
                race_id=race_db.id,
                jockey=horse_jockey,
                trainer=horse_trainer,
                last_starts=last_starts,
                colours=colours,
                colours_pic=colours_image,
                barrier=barrier if barrier is not None else None
            ))

            statistics = parser.get_horse_stats(horse)
            for stat in statistics:
                if stat['type'] in allowed_stat:

                    total = int(stat['total'])
                    first = int(stat['firsts'])
                    second = int(stat['seconds'])
                    third = int(stat['thirds'])

                    win_ratio = 0
                    if total > 0:
                        win_ratio = (first + second * 0.5 +
                                     third * 0.25) / total

                    horse_race_stats = repo.horse_race_stats.create(
                        db, HorseRaceStatsCreate(
                            stat=stat['type'],
                            total=total,
                            first=first,
                            second=second,
                            third=third,
                            win_ratio=win_ratio,
                            horse_id=horse_db.id,
                            race_id=race_db.id,
                        )
                    )

    print("File Loaded to DB Successfully.")
# def test_data(file):
#     xml_file = file
#     parser = XmlParser(xml_file)
#     races = parser.get_races()
#     for race in races:
#         horses = parser.get_race_horses(race)
#         for horse in horses:

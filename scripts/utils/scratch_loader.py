from datetime import datetime
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from .scratch_parser import ScratchParser
from app import repositories as repo

def load_scratch(file):
    print("Loading Scratch to DB...")

    xml_file = file
    parser = ScratchParser(xml_file)
    db: Session = SessionLocal()

    meeting_data = parser.get_meeting_data()

    track = repo.track.get_track(db,  meeting_data['track_id'], meeting_data['track_name'])

    meeting_date = datetime.strptime(meeting_data['meeting_date'], "%d/%m/%Y")
    if track is not None:
        meeting_in_db = repo.meeting.get_meeting(db, track.id, meeting_date.strftime("%Y-%m-%d"))
        if meeting_in_db is not None:
            race_data = parser.get_races()
            for race in race_data:
                race_in_db = repo.race.get_race(db, race_id=race['id'], meeting_id=meeting_in_db.id)
                if race_in_db is not None:
                    horses = parser.get_scratch_horses(race)
                    for horse in horses:
                        horse_in_db = repo.horse.get_horse_from_horse_id(db, horse['id'])
                        if horse_in_db is not None:
                            stats = repo.horse_race_stats.get_all_stats_by_id(db, race_id=race_in_db.id,
                                                                              horse_id=horse_in_db.id)
                            for stat in stats:
                                repo.horse_race_stats.scratch(db, stat.id)
                                print(f"Scratched HorseRaceStat {stat.id}")

                            horse_race_info = repo.horse_race_info.get_horse_race_info(db,
                                               race_id=race_in_db.id, horse_id=horse_in_db.id)
                            if horse_race_info is not None:
                                repo.horse_race_info.scratch(db, horse_race_info.id)
                                print(f"Scratched HorseRaceStat {horse_race_info.id}")


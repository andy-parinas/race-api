from datetime import datetime
from app.db.session import SessionLocal
from app import repositories as repo
from .xml_parser import XmlParser


def load_db(file):
    allowed_stat = ['track', 'distance', 'distance_track',
                    'firm', 'good', 'soft', 'heavy', 'synthetic',
                    'first_up', 'second_up', 'current_jockey'
                    ]
    xml_file = file
    parser = XmlParser(xml_file)
    races = parser.get_races()
    db = SessionLocal()
    meeting_date = parser.get_meeting_date()
    for race in races:
        start_time = parser.get_race_start_time(race)
        date_time = f"{meeting_date} {start_time}"
        race_db = repo.race.create(
            db,
            {
                "race_id": race['id'],
                "race_date": datetime.strptime(date_time, "%d/%m/%Y %I:%M%p")
            }
        )
        horses = parser.get_race_horses(race)
        for horse in horses:
            horse_db = repo.horse.create(
                db,
                {
                    "horse_id":  horse['id'],
                    "horse_name": horse['name']
                }
            )
            statistics = parser.get_horse_stats(horse)
            for stat in statistics:
                if stat['type'] in allowed_stat:
                    current_race = repo.current_race.create(
                            db,
                            {
                                "stat": stat['type'],
                                "total": int(stat['total']),
                                "first": int(stat['firsts']),
                                "second": int(stat['seconds']),
                                "third": int(stat['thirds']),
                                "horse_id": horse_db.id,
                                "race_id": race_db.id
                            }
                        )
                    print(f"{current_race.id}")

from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag

class ScratchParser:
    def __init__(self, xml_file):
        with open(xml_file, 'r') as file:
            xml = file.read()

        self.soup = BeautifulSoup(xml, features='xml')

    def get_meeting_data(self):
        meeting = self.soup.find('meeting', recursive=False)
        meeting_track = meeting.find('track', recursive=False)
        meeting_date = meeting.find('date', recursive=False)
        return {
            "track_name": meeting_track['name'],
            "track_id": meeting_track['id'],
            "state": meeting_track['state'],
            "meeting_date": meeting_date.text
        }

    def get_races(self):
        race_data = self.soup.races
        return race_data.find_all('race', recursive=False)


    def get_scratch_horses(self, race: Tag) -> ResultSet:
        horses_data = race.find('scratched_horses', recursive=False)
        return horses_data.find_all('horse', recursive=False)


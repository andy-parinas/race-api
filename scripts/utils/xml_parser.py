from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag


class XmlParser:
    def __init__(self, xml_file):
        with open(xml_file, 'r') as file:
            xml = file.read()

        self.soup = BeautifulSoup(xml, features='xml')

    def get_meeting_date(self):
        meeting = self.soup.find('meeting', recursive=False)
        meeting_date = meeting.find('date', recursive=False)
        return meeting_date.text

    def get_meeting_data(self):
        meeting = self.soup.find('meeting', recursive=False)
        meeting_track = meeting.find('track', recursive=False)
        meeting_date = meeting.find('date', recursive=False)
        return {
            "track_name": meeting_track['name'],
            "track_id": meeting_track['id'],
            "track_surface": meeting_track['track_surface'],
            "location": meeting_track['location'],
            "state": meeting_track['state'],
            "meeting_date": meeting_date.text
        }

    def get_races(self):
        race_data = self.soup.races
        return race_data.find_all('race', recursive=False)

    def get_race_start_time(self, race):
        start_time = race.find('start_time', recursive=False )
        return start_time.text

    def get_race_horses(self, race: Tag) -> ResultSet:
        horses_data = race.find('horses', recursive=False)
        return horses_data.find_all('horse', recursive=False)

    def get_horse_stats(self, horse: Tag):
        statistics_data = horse.find('statistics', recursive=False)
        return statistics_data.find_all('statistic', recursive=False)


# def get_xml_soup(xml_file):
#     with open(xml_file, 'r') as file:
#         xml = file.read()
#
#     soup = BeautifulSoup(xml, features='xml')
#     return soup
#
#
# def get_races_from_xml(xml_file) -> ResultSet:
#     race_data = soup.races
#     return race_data.find_all('race', recursive=False)
#
#
# def get_horses_from_race(race: Tag) -> ResultSet:
#     horses_data = race.find('horses', recursive=False)
#     return horses_data.find_all('horse', recursive=False)
#
#
# def get_statistics_from_horse(horse: Tag) -> ResultSet:
#     statistics_data = horse.find('statistics', recursive=False)
#     return statistics_data.find_all('statistic', recursive=False)

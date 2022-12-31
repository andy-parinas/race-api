from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag

def get_races_from_xml(xml_file) -> ResultSet:
    with open(xml_file, 'r')as file:
        xml = file.read()

    soup = BeautifulSoup(xml, features='xml')
    race_data = soup.races
    return race_data.find_all('race', recursive=False)


def get_horses_from_race(race: Tag) -> ResultSet:
    horses_data = race.find('horses', recursive=False)
    return horses_data.find_all('horse', recursive=False)


def get_statistics_from_horse(horse: Tag) -> ResultSet:
    statistics_data = horse.find('statistics', recursive=False)
    return statistics_data.find_all('statistic', recursive=False)

if __name__ == "__main__":
    xml_file = '../storage/20221119_GOS_FORM_XML_A.xml'
    races = get_races_from_xml(xml_file)
    for race in races:
        horses = get_horses_from_race(race)
        for horse in horses:
            statistics = get_statistics_from_horse(horse)
            for stat in statistics:
                print(f"{race['id']} {horse['name']} Stat Type: {stat['type']}")
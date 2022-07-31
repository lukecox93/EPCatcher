from fractions import Fraction

class Horse(object):
    def __init__(self, name, number, bookie, odds):
        self.name = name
        self.number = number
        self.odds = {bookie: odds}
        self.place_terms = 1/5

    def get_name(self):
        return self.name

    def get_odds(self):
        return self.odds

    def get_number(self):
        return self.number

    def update_odds(self, bookie, odds):
        self.odds[bookie] = odds

    def update_multiple_odds(self, dictionary: dict):
        self.odds.update(dictionary)

    def give_highest_odds(self):
        return max(self.odds.items(), key=lambda k: k[1])

    def to_string(self):
        return f'{self.name}: {self.odds}'

    def get_place_terms(self):
        return self.place_terms

    def get_place_terms_as_string(self):
        return Fraction(self.place_terms).limit_denominator()


class HorseRace(object):
    def __init__(self, location, time):
        self.name = f'{location} - {time}'
        self.location = location
        self.time = time
        self.horses = {}
        self.bookies = []
        self.urls = {}
        self.runners = int
        self.standard_places = 3

    def __lt__(self, other):
        return self.time < other.time

    def get_name(self):
        return self.name

    def get_location(self):
        return self.location

    def get_time(self):
        return self.time

    def get_horse(self, name: str):
        return self.horses.get(name)

    def get_horses(self):
        return self.horses

    def get_runners(self):
        return self.runners

    def get_bookies(self):
        return self.bookies

    def get_url(self, bookie: str):
        return self.urls.get(bookie)

    def get_places(self):
        return self.standard_places

    def get_urls(self):
        return self.urls if self.urls else None

    def add_horses(self, *kwargs: Horse):
        for arg in kwargs:
            self.horses[arg.get_name()] = arg
        return 1

    def remove_horses(self, *kwargs: str):
        for arg in kwargs:
            del self.horses[arg]
        return 1

    def add_bookie(self, bookie, url):
        self.bookies.append(bookie)
        self.urls[bookie] = url

    def get_odds(self):
        return [{horse.get_name(): horse.get_odds()} for horse in self.get_horses().values()]

    def to_string(self):
        new_line = '\n'
        return f'{new_line}{self.name}{new_line}{new_line}{new_line.join((horse.to_string() for horse in self.get_horses().values()))}'


class HorseRaces(object):
    def __init__(self):
        self.races = {}

    def sort_by_date(self):
        self.races = {k: v for k, v in sorted(self.races.items(), key=lambda item: item[1])}

    def add_race(self, competition: HorseRace):
        self.races[competition.get_name()] = competition

    def get_races(self):
        return self.races if self.races else {}

    def get_race(self, race_title):
        return self.races.get(race_title)

    def get_odds(self):
        return [race.get_odds() for race in self.get_races().values()]

    def get_horse(self, race_name: str, name: str):
        return self.get_race(race_name).get_horse(name)

    def to_string(self):
        new_line = '\n'
        return f'{new_line.join(race.to_string() for race in self.get_races().values())}'









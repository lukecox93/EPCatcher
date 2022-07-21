

class Horse:
    def __init__(self, name, number, bookie, odds):
        self.name = name
        self.number = number
        self.odds = {bookie: odds}

    def get_name(self):
        return self.name

    def get_odds(self):
        return self.odds

    def get_number(self):
        return self.number

    def update_odds(self, bookie, odds):
        self.odds[bookie] = odds
        return 1

    def update_multiple_odds(self, dictionary: dict):
        self.odds.update(dictionary)
        return 1


class HorseRace:
    def __init__(self, location, time):
        self.name = f'{location}, {time}'
        self.location = location
        self.time = time
        self.horses = {}
        self.bookies = []
        self.urls = {}

    def get_name(self):
        return self.name

    def get_location(self):
        return self.location

    def get_time(self):
        return self.time

    def get_horse(self, name: str):
        return self.horses[name] if name in self.horses else None

    def get_horses(self):
        return self.horses

    def get_runners(self):
        return self.runners

    def get_bookies(self):
        return self.bookies

    def get_url(self, bookie: str):
        return self.urls[bookie] if bookie in self.urls else None

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


class HorseRaces:
    def __init__(self):
        self.races = {}

    def add_race(self, competition: HorseRace):
        self.races[competition.get_name()] = competition

    def get_races(self):
        return self.races if self.races else None

    def get_race(self, race_title):
        try:
            return self.races[race_title]
        except KeyError:
            return False


one = Horse('one', 1, 'William Hill', 2.0)
two = Horse('two', 1, 'William Hill', 2.0)
three = Horse('three', 1, 'William Hill', 2.0)

kmpton = HorseRace('Kempton', '17:00')
kempton = HorseRace('Kempton', '17:01')

kempton.add_horses(one, two, three)

today = HorseRaces()
today.add_race(kempton)
today.add_race(kmpton)

one.update_odds('Betfred', 3)
one.update_odds('Betfred', 4)

today.get_race('Kempton, 17:01').get_horse('one').update_odds('Betfred', 1)






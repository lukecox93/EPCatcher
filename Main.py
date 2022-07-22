from Bookmaker import Betfred
from Objects import Horse, HorseRace, HorseRaces
import time

def main():
    today = HorseRaces()
    betfred = Betfred(today)
    betfred.get_races_data()
    betfred.get_race_urls()
    betfred.get_indiv_race_data('new')
    print(today.to_string())
    time.sleep(30)
    betfred.get_indiv_race_data('update')


if __name__ == '__main__':
    main()

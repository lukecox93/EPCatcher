from Bookmaker import Betfred, WilliamHill, PaddyPower
from Objects import Horse, HorseRace, HorseRaces
import time

def main():
    start_time = time.time()
    today = HorseRaces()
    paddypower = PaddyPower(today)
    paddypower.get_races_data()
    paddypower.get_race_urls()
    paddypower.get_indiv_race_data('new')
    williamhill = WilliamHill(today)
    williamhill.get_races_data()
    williamhill.get_race_urls()
    williamhill.get_indiv_race_data('new')
    betfred = Betfred(today)
    betfred.get_races_data()
    betfred.get_race_urls()
    betfred.get_indiv_race_data('new')
    print(today.to_string())
    print(time.time() - start_time)








if __name__ == '__main__':
    main()

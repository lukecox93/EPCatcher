import Bookmaker
from Objects import Horse, HorseRace, HorseRaces
import time
import concurrent.futures
from datetime import datetime

def start_day(bookie):
    bookie.get_races_data()
    bookie.get_race_urls()
    bookie.get_indiv_race_data('new')

def update(bookie):
    bookie.get_indiv_race_data('update')

def main():
    today = HorseRaces()
    bookies = []
    bookies.append(Bookmaker.PaddyPower(today))
    bookies.append(Bookmaker.WilliamHill(today))
    bookies.append(Bookmaker.Betfred(today))
    bookies.append(Bookmaker.BetVictor(today))
    bookies.append(Bookmaker.Parimatch(today))
    bookies.append(Bookmaker.ThirtyTwoRed(today))
    bookies.append(Bookmaker.Grosvenor(today))
    bookies.append(Bookmaker.Casumo(today))
    bookies.append(Bookmaker.LeoVegas(today))
    bookies.append(Bookmaker.MrGreen(today))
    bookies.append(Bookmaker.LiveScoreBet(today))
    bookies.append(Bookmaker.VirginBet(today))
    bookies.append(Bookmaker.PokerStars(today))

    new_time = time.time()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(start_day, bookies)

    #for bookie in bookies:
     #   start_day(bookie)

    today.sort_by_date()

    print(time.time() - new_time)

    update_time = time.time()
    #with concurrent.futures.ThreadPoolExecutor() as executor:
        #executor.map(update, bookies)
    print(time.time() - update_time)

    return today

if __name__ == '__main__':
    main()

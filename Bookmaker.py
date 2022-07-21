import WebBrowsing
import requests
import functions
from Objects import Horse, HorseRace, HorseRaces


class Bookmaker:
    def __init__(self, name, all_race_url: str, all_race_query_string, headers, race_url: str):
        self.name = name
        self.all_race_url = all_race_url
        self.all_race_query_string = all_race_query_string
        self.all_race_json_data = {}
        self.race_extensions = []
        self.headers = headers
        self.race_url = race_url
        self.races = []

    def get_races_data(self):
        with requests.Session() as session:
            self.all_race_json_data = WebBrowsing.UrlOpener(session).open_url(self.all_race_url,
                                                                              self.all_race_query_string, self.headers)
            return 1

    def add_new_horse_race(self, races_for_the_day: HorseRaces, location, time):
        races_for_the_day.add_race(HorseRace(location, time))

    def add_new_horse(self, race_name, name, number, odds):
        today.get_race(race_name).add_horses(Horse(name, number, self.name, odds))

    def update_horse_odds(self, race_name, name, odds):
        today.get_race(race_name).get_horse(name).update_odds(self.name, odds)


class Betfred(Bookmaker):
    def __init__(self, name, all_race_url: str, all_race_query_string, headers, race_url: str):
        super().__init__(name, all_race_url, all_race_query_string, headers, race_url)

    def get_race_urls(self):
        for race in self.all_race_json_data['Bonavigationnode']['marketgroups']:
            self.races.append(race['idfwmarketgroup'])

    def get_indiv_race_data(self):
        with requests.Session() as session:
            for extension in self.races:
                query_string = {"language": "uk", "type": "marketgroup", "idfwmarketgroup": extension,
                                "dataflags": "12",
                                "datasize": "8", "cachebust": "1658160890508"}
                json_data = WebBrowsing.UrlOpener(session).open_url(self.race_url, query_string, self.headers)
                title = self.get_race_title(json_data)
                self.get_indiv_horse_data(json_data, title)

    def get_race_title(self, json_race_data):
        return ', '.join(json_race_data['Marketgroup']['name'].split(' ')[::-1])

    def get_indiv_horse_data(self, json_race_data, race_title):
        print(race_title)
        for horse in json_race_data['Marketgroup']['markets'][0]['selections']:
            if horse['is1stfavourite'] != 'true' and horse['is2ndfavourite'] != 'true' and horse[
                'idfobolifestate'] != 'NR':
                name = horse['name']
                number = horse['competitornumber']
                odds = functions.convert_to_decimal(horse['currentpriceup'], horse['currentpricedown'])
                if not today.get_race(race_title):
                    self.add_new_horse_race(today, race_title.split(', ')[0], race_title.split(', ')[1])
                if not today.get_race(race_title).get_horse(name):
                    self.add_new_horse(race_title, name, number, odds)
                else:
                    self.update_horse_odds(race_title, name, odds)
        for horse in today.get_race(race_title).get_horses().values():
            print(f'{horse.get_name()}, {horse.get_odds()}')

    def update_data(self, json_race_data, race_title):
        for horse in json_race_data['Marketgroup']['markets'][0]['selections']:
            if horse['is1stfavourite'] != 'true' and horse['is2ndfavourite'] != 'true' and horse[
                'idfobolifestate'] != 'NR':
                name = horse['name']
                odds = functions.convert_to_decimal(horse['currentpriceup'], horse['currentpricedown'])
                self.update_horse_odds(race_title, name, odds)

# TODO - add functionality for super extra place races


kmpton = HorseRace('Yarmouth', '16:52')
today = HorseRaces()
today.add_race(kmpton)

betfred = Betfred('Betfred', "https://www.betfred.com/services/SportsBook/navigationlist",
                  {"region": "440", "language": "uk", "type": "bonavigationlist", "id": "254374.2", "dataflags": "12",
                   "datasize": "8", "cachebust": "1658160592143"}, {
                      "cookie": "visid_incap_2254385=ARD5TOf1RwK55Av/63oP/pQTjmIAAAAAQUIPAAAAAABnulSVh/H/pDSAYlgbp/7c; "
                                "_gcl_au=1.1.1299117066.1653478296; "
                                "__adal_ca=so^%^3Ddirect^%^26me^%^3Dnone^%^26ca^%^3Ddirect^%^26co^%^3D^%^28not^%^2520set^%^29^%^26ke"
                                "^%^3D^%^28not^%^2520set^%^29; _tgci=0997f865-aaf3-5213-92b0-6520d39a7ea6; "
                                "_tgpc=77aaac86-472c-52cb-998f-9e04ae2dde93; "
                                "cd_user_id=180fafc8bf5f09-0cc5c73a3aa09a-26021851-1fa400-180fafc8bf6ea8; "
                                "_hjSessionUser_688760"
                                "=eyJpZCI6ImQwNmNlOWY0LTMwNzYtNTFjNi05ZDI0LTc3NjJlYzUzNDRhMyIsImNyZWF0ZWQiOjE2NTM0NzgyOTY3NDYsImV4aXN0aW5nIjp0cnVlfQ==; IA_AffiliateTracking=AffiliateID=10006&BTAG=a_107470b_c_Betfred-e-590045377658d_323778697; IA_AffiliateTracking_BTAG=a_107470b_c_Betfred-e-590045377658d_323778697; IA_AffiliateTracking_AffID=10006; BF_AffiliateTracking=AffiliateID=10006&trackingSystem=RV&trackingString=a_107470b_c_Betfred-e-590045377658d_323778697; BF_AffiliateTracking_BTAG=a_107470b_c_Betfred-e-590045377658d_323778697; BF_AffiliateTracking_ClickData=^{^\^click_id^^:323778697,^\^click_date^^:^\^2022-07-13",
                      "authority": "www.betfred.com",
                      "accept": "*/*",
                      "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
                      "content-type": "application/json",
                      "referer": "https://www.betfred.com/sports/market-group/20121636.2",
                      "sec-ch-ua": "^\^.Not/A",
                      "sec-ch-ua-mobile": "?0",
                      "sec-ch-ua-platform": "^\^Windows^^",
                      "sec-fetch-dest": "empty",
                      "sec-fetch-mode": "cors",
                      "sec-fetch-site": "same-origin",
                      "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
                      "x-betfred": "Betfred Website (Desktop)",
                      "x-instana-l": "1,correlationType=web;correlationId=81a6ec0ac4254ffe",
                      "x-instana-s": "81a6ec0ac4254ffe",
                      "x-instana-t": "81a6ec0ac4254ffe"
                  }, "https://www.betfred.com/services/SportsBook/marketgroup")

betfred.get_races_data()
betfred.get_race_urls()
betfred.get_indiv_race_data()



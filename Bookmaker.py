import WebBrowsing
import requests
import functions
from Objects import Horse, HorseRace, HorseRaces
from dateutil import parser
import pytz
from pytz import timezone
import time


class Bookmaker(object):
    def __init__(self, today):
        self.name = str
        self.all_race_url = str
        self.all_race_query_string = []
        self.all_race_json_data = []
        self.race_extensions = []
        self.headers = None
        self.race_url = None
        self.races = []
        self.today = today

    def get_races_data(self):
        with requests.Session() as session:
            for query_string in self.all_race_query_string:
                self.all_race_json_data.append(WebBrowsing.UrlOpener(session).open_url(self.all_race_url,
                                                                              query_string, self.headers))
            return 1

    def add_new_horse_race(self, races_for_the_day: HorseRaces, location, time):
        races_for_the_day.add_race(HorseRace(location, time))

    def add_new_horse(self, race_name, name, number, odds):
        self.today.get_race(race_name).add_horses(Horse(name, number, self.name, odds))

    def update_horse_odds(self, race_name, name, odds):
        self.today.get_horse(race_name, name).update_odds(self.name, odds)


class Betfred(Bookmaker):
    def __init__(self, today):
        super().__init__(today)
        self.name = 'Betfred'
        self.all_race_url = "https://www.betfred.com/services/SportsBook/navigationlist"
        self.all_race_query_string = [{"region": "440", "language": "uk", "type": "bonavigationlist", "id": "254374.2", "dataflags": "12",
                   "datasize": "8", "cachebust": "1658160592143"}, {"region": "440", "language": "uk", "type": "bonavigationlist", "id": "250364.2", "dataflags": "12",
                   "datasize": "8", "cachebust": "1658160592143"}]
        self.headers = {
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
                  }
        self.race_url = "https://www.betfred.com/services/SportsBook/marketgroup"

    def get_race_urls(self):
        self.races = [race['idfwmarketgroup'] for data in self.all_race_json_data for race in data['Bonavigationnode']['marketgroups']]

    def get_indiv_race_data(self, new_or_update: str):
        with requests.Session() as session:
            for extension in self.races:
                query_string = {"language": "uk", "type": "marketgroup", "idfwmarketgroup": extension,
                                "dataflags": "12",
                                "datasize": "8", "cachebust": "1658160890508"}
                json_data = WebBrowsing.UrlOpener(session).open_url(self.race_url, query_string, self.headers)
                title = self.get_race_title(json_data)
                self.get_indiv_horse_data(json_data, title) if new_or_update == 'new' else self.update_data(json_data, title)

    def get_race_title(self, json_race_data):
        location = json_race_data['Marketgroup']['markets'][0]['venue']
        time = json_race_data['Marketgroup']['name'][:5]
        return f'{location}, {time}'

    def get_indiv_horse_data(self, json_race_data, race_title):
        for horse in json_race_data['Marketgroup']['markets'][0]['selections']:
            if horse['is1stfavourite'] != 'true' and horse['is2ndfavourite'] != 'true' and horse[
                'idfobolifestate'] != 'NR':
                name = horse['name']
                number = horse['competitornumber']
                try:
                    odds = functions.convert_to_decimal(horse['currentpriceup'], horse['currentpricedown'])
                except KeyError:
                    odds = '-'
                if not self.today.get_race(race_title):
                    self.add_new_horse_race(self.today, race_title.split(', ')[0], race_title.split(', ')[1])
                if not self.today.get_race(race_title).get_horse(name):
                    self.add_new_horse(race_title, name, number, odds)
                else:
                    self.update_horse_odds(race_title, name, odds)

    def update_data(self, json_race_data, race_title):
        for horse in json_race_data['Marketgroup']['markets'][0]['selections']:
            if horse['is1stfavourite'] != 'true' and horse['is2ndfavourite'] != 'true' and horse[
                'idfobolifestate'] != 'NR':
                name = horse['name']
                try:
                    odds = functions.convert_to_decimal(horse['currentpriceup'], horse['currentpricedown'])
                except KeyError:
                    odds = '-'
                self.update_horse_odds(race_title, name, odds)


class WilliamHill(Bookmaker):
    def __init__(self, today):
        super().__init__(today)
        self.name = 'William Hill'
        self.all_race_url = "https://sports.williamhill.com/data/rmp01/api/desktop/horse-racing/en-gb/meetings/extra-places/today"
        self.all_race_tomorrow_url = "https://sports.williamhill.com/data/rmp01/api/desktop/horse-racing/en-gb/meetings/extra-places" \
                   "/tomorrow "
        self.all_race_query_string = ['']
        self.headers = {
        "cookie": "vid=edcd8a38-46b2-45e6-bef6-a3e243800c3d; storageSSC=lsSSC^%^3D1; _gcl_au=1.1.130733483.1653407172; "
                  "OptanonAlertBoxClosed=2022-05-24T15:46:13.598Z; _scid=eb7325b4-8201-45d8-9a85-259f4e2e7eb9; "
                  "QuantumMetricUserID=0a020ac0e9a395844e11b9d2bfc2d5fc; uge=y; bfsd=ts=1653407175711^|st=reg; "
                  "language=en_GB; bid_pPBFRdxAR61DXgGaYvvIPWQ7pAaq8QQJ=90913374-ab03-4446-a72a-d0b6aa85d8d8; "
                  "userhistory=725650521656072408928^|1^|N^|240622^|240622^|home^|N; bucket=3~53~test_search_fbs; "
                  "bftim=1656072408928; bfj=GB; betexPtk=betexCurrency^%^3DGBP^%^7EbetexLocale^%^3Den^%^7EbetexRegion"
                  "^%^3DGBR; LPVID=ZmYWY0N2UzMDczMTY3MWFk; rfr=5300708; PI=5300708; "
                  "TrackingTags=rfr=5300708&prod_vertical=SPORTSBOOK; StickyTags=rfr=5300708&prod_vertical=SPORTSBOOK; "
                  "_gcl_dc=GCL.1656766983.CjwKCAjw2f-VBhAsEiwAO4lNeI2BFOPLEOybUgTWKSdt4v56dw"
                  "-2gv96OTQI5oxKWFNkjHAhbOwtoxoCrvQQAvD_BwE; "
                  "_gcl_aw=GCL.1656766983.CjwKCAjw2f-VBhAsEiwAO4lNeI2BFOPLEOybUgTWKSdt4v56dw"
                  "-2gv96OTQI5oxKWFNkjHAhbOwtoxoCrvQQAvD_BwE; "
                  "_gac_UA-63107437-17=1.1656766983.CjwKCAjw2f-VBhAsEiwAO4lNeI2BFOPLEOybUgTWKSdt4v56dw"
                  "-2gv96OTQI5oxKWFNkjHAhbOwtoxoCrvQQAvD_BwE; ccawa=6346129162088072573367057810712168089409; "
                  "gtmfl=/4Hr2; __cf_bm=dA_E5uRoXdbsJ9JgTBMWKTPBdJbmRMvGbG15z6L4GUM-1657881511-0-Ab2Bhgzd8zMSX4H1d5Ji"
                  "+h8rRUQGxA1wZZbpfuST+Q0hRxliE48V2z7n4WcxMzDXAzOeF5d0QKlrwSgmJrLnx4E=; "
                  "bx_guest_ref=a43834d3-4475-4c41-b8a2-128b04af2355; bx_bucket_number=77; "
                  "_gid=GA1.2.1185969717.1657881516; _gat=1; _uetsid=48262cd0042a11ed8f9e0b75e2c6026c; "
                  "_uetvid=a4242a00db7811ec96368df59a5e70eb; Qualtrics_Cookie=; "
                  "QuantumMetricSessionID=216886d8e2376f2faaa9ff878b66520b; _ga=GA1.2.1233677491.1653407174; "
                  "OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jul+15+2022+11^%^3A38^%^3A40+GMT^%^2B0100+("
                  "British+Summer+Time)&version=6.18.0&isIABGlobal=false&hosts=&consentId=68089409&interactionCount=1"
                  "&landingPath=NotLandingPage&groups=C0001^%^3A1^%^2CC0003^%^3A1^%^2CC0002^%^3A1^%^2CC0004^%^3A1"
                  "&geolocation=^%^3B&AwaitingReconsent=false; _ga_DC69KVTC2E=GS1.1.1657881516.22.1.1657881528.48",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/103.0.0.0 "
                      "Safari/537.36 "
    }

    def get_race_urls(self):
        self.races = [f'{race["id"]}/{race["slug"]}' for data in self.all_race_json_data[0]['data']['regionCompetitions'][0]['competitions'] for race in data['events']]

    def get_indiv_race_data(self, new_or_update):
        with requests.Session() as session:
            for extension in self.races:
                url = f'https://sports.williamhill.com/data/rmp01/api/desktop/horse-racing/en-gb/racecard/{extension}'
                json_data = WebBrowsing.UrlOpener(session).open_url(url, '', self.headers)
                title = self.get_race_title(json_data)
                self.get_indiv_horse_data(json_data, title) if new_or_update == 'new' else self.update_data(json_data,
                                                                                                            title)

    def get_indiv_horse_data(self, json_race_data, race_title):
        print(race_title)
        if json_race_data['data']['raceCardData']['event']['isInPlay']:
            return
        horse_ids = [[horse['title'], horse['runnerNum'], horse['selections'][0]] for horse in
                     json_race_data['data']['raceCardData']['marketCollections'][0]['raceCardTables'][0]['raceCardRows']]
        for horse in horse_ids:
            runner = (json_race_data['data']['raceCardData']['selections'][horse[2]])
            if runner['priceNum'] != None:
                name = horse[0]
                number = horse[1]
                odds = functions.convert_to_decimal(runner['priceNum'], runner['priceDen'])
                if not self.today.get_race(race_title):
                    self.add_new_horse_race(self.today, race_title.split(', ')[0], race_title.split(', ')[1])
                if not self.today.get_race(race_title).get_horse(name):
                    self.add_new_horse(race_title, name, number, odds)
                else:
                    self.update_horse_odds(race_title, name, odds)

    def update_data(self, json_race_data, race_title):
        horse_ids = [[horse['title'], horse['runnerNum'], horse['selections'][0]] for horse in
                     json_race_data['data']['raceCardData']['marketCollections'][0]['raceCardTables'][0][
                         'raceCardRows']]
        for horse in horse_ids:
            runner = (json_race_data['data']['raceCardData']['selections'][horse[2]])
            if runner['priceNum'] != None:
                name = horse[0]
                number = horse[1]
                odds = functions.convert_to_decimal(runner['priceNum'], runner['priceDen'])
                self.update_horse_odds(race_title, name, odds)

    def get_race_title(self, json_race_data):
        slug = json_race_data['data']['raceCardData']['event']['slug']
        location = ' '.join([word.capitalize() for word in slug[5:].split('-')])
        time = f'{slug[:2]}:{slug[2:4]}'
        return f'{location}, {time}'


class PaddyPower(Bookmaker):
    def __init__(self, today):
        super().__init__(today)
        self.name = 'Paddy Power'
        self.all_race_url = "https://apisds.paddypower.com/sdspp/content-managed-page/v7"
        self.all_race_query_string = [{"_ak": "vsd0Rm5ph2sS2uaK", "betexRegion": "GBR", "capiJurisdiction": "intl",
                  "cardsToFetch": ["18888", "SEO_CONTENT_SUMMARY"], "countryCode": "GB", "currencyCode": "GBP",
                  "eventTypeId": "7", "exchangeLocale": "en_GB", "includeEuromillionsWithoutLogin": "false",
                  "includeMarketBlurbs": "true", "includePrices": "true", "includeRaceCards": "true",
                  "language": "en", "layoutFetchedCardsOnly": "true", "loggedIn": "false",
                  "nextRacesMarketsLimit": "3", "page": "SPORT", "priceHistory": "3", "regionCode": "UK",
                  "requestCountryCode": "GB", "staticCardsIncluded": "SEO_CONTENT_SUMMARY",
                  "timezone": "Europe^%^2FLondon"}]
        self.headers = {
"authority": "apisds.paddypower.com",
"accept": "application/json, text/plain, */*",
"accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
"cookie": "vid=edcd8a38-46b2-45e6-bef6-a3e243800c3d; storageSSC=lsSSC^%^3D1; _gcl_au=1.1.130733483.1653407172; "
          "OptanonAlertBoxClosed=2022-05-24T15:46:13.598Z; _scid=eb7325b4-8201-45d8-9a85-259f4e2e7eb9; "
          "QuantumMetricUserID=0a020ac0e9a395844e11b9d2bfc2d5fc; uge=y; bfsd=ts=1653407175711^|st=reg; "
          "language=en_GB; bid_pPBFRdxAR61DXgGaYvvIPWQ7pAaq8QQJ=90913374-ab03-4446-a72a-d0b6aa85d8d8; "
          "userhistory=725650521656072408928^|1^|N^|240622^|240622^|home^|N; bucket=3~53~test_search_fbs; "
          "bftim=1656072408928; bfj=GB; betexPtk=betexCurrency^%^3DGBP^%^7EbetexLocale^%^3Den^%^7EbetexRegion^%^3DGBR"
          "; LPVID=ZmYWY0N2UzMDczMTY3MWFk; rfr=5300708; PI=5300708; "
          "TrackingTags=rfr=5300708&prod_vertical=SPORTSBOOK; StickyTags=rfr=5300708&prod_vertical=SPORTSBOOK; "
          "_gcl_aw=GCL.1656766983.CjwKCAjw2f-VBhAsEiwAO4lNeI2BFOPLEOybUgTWKSdt4v56dw"
          "-2gv96OTQI5oxKWFNkjHAhbOwtoxoCrvQQAvD_BwE; "
          "_gcl_dc=GCL.1656766983.CjwKCAjw2f-VBhAsEiwAO4lNeI2BFOPLEOybUgTWKSdt4v56dw"
          "-2gv96OTQI5oxKWFNkjHAhbOwtoxoCrvQQAvD_BwE; "
          "_gac_UA-63107437-17=1.1656766983.CjwKCAjw2f-VBhAsEiwAO4lNeI2BFOPLEOybUgTWKSdt4v56dw"
          "-2gv96OTQI5oxKWFNkjHAhbOwtoxoCrvQQAvD_BwE; ccawa=6346129162088072573367057810712168089409; gtmfl=/4Hr2; "
          "bx_guest_ref=a43834d3-4475-4c41-b8a2-128b04af2355; bx_bucket_number=77; _gid=GA1.2.1185969717.1657881516; "
          "Qualtrics_Cookie=; _mibhv=anon-1657887989967-6710669666_6418; "
          "QSI_HistorySession=https^%^3A^%^2F^%^2Fapisds.paddypower.com^%^2Fbet~1657887990815; "
          "__cf_bm=Gtz3Q_33UoQUN78sX5wKjxjuFFQVsN0B8jJ3gCC8gas-1657893233-0-AcerZMETz8nSUT4wmBCyOmwwxWUbKHsawR"
          "+SbDX4BGY9lg7pPun746BKuzKxCTgYm3y4TIh54J4w0ltqwWBn94I=; "
          "QuantumMetricSessionID=03ee347a15d46b2c351125308def061b; _ga=GA1.1.1233677491.1653407174; "
          "_uetsid=48262cd0042a11ed8f9e0b75e2c6026c; _uetvid=a4242a00db7811ec96368df59a5e70eb; "
          "OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jul+15+2022+15^%^3A02^%^3A23+GMT^%^2B0100+("
          "British+Summer+Time)&version=6.18.0&isIABGlobal=false&hosts=&consentId=68089409&interactionCount=1"
          "&landingPath=NotLandingPage&groups=C0001^%^3A1^%^2CC0003^%^3A1^%^2CC0002^%^3A1^%^2CC0004^%^3A1&geolocation"
          "=^%^3B&AwaitingReconsent=false; _ga_DC69KVTC2E=GS1.1.1657892031.25.1.1657893808.60",
"origin": "https://www.paddypower.com",
"referer": "https://www.paddypower.com/",
"sec-ch-ua": "^\^.Not/A",
"sec-ch-ua-mobile": "?0",
"sec-ch-ua-platform": "^\^Windows^^",
"sec-fetch-dest": "empty",
"sec-fetch-mode": "cors",
"sec-fetch-site": "same-site",
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}
        self.race_url = "https://apisds.paddypower.com/sdspp/racing-page/v7"

    def get_race_urls(self):
        self.races = [self.all_race_json_data[0]['attachments']['races'][race]['raceId'] for race in
                      self.all_race_json_data[0]['attachments']['races']]

    def get_indiv_race_data(self, new_or_update):
        with requests.Session() as session:
            for extension in self.races:
                query_string = {"_ak": "vsd0Rm5ph2sS2uaK", "betexRegion": "GBR", "capiJurisdiction": "intl", "currencyCode": "GBP",
                   "eventTypeId": "7", "exchangeLocale": "en_GB", "includePrices": "true",
                   "includeRaceTimeform": "true",
                   "includeResults": "true", "language": "en", "priceHistory": "3", "raceId": extension,
                   "regionCode": "UK"}
                json_data = WebBrowsing.UrlOpener(session).open_url(self.race_url, query_string, self.headers)
                print(json_data)
                title = self.get_race_title(json_data)

    def get_race_title(self, json_data):
        pass



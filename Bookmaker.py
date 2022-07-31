import WebBrowsing
import requests
import functions
from Objects import Horse, HorseRace, HorseRaces
from dateutil import parser
import pytz
from pytz import timezone
import time
import string
from datetime import datetime
from datetime import timedelta
import re


def format_horse_name(name):
    return name.translate(str.maketrans('', '', string.punctuation)).title()


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

    def add_new_horse_race(self, json_race_data, extension=None):
        self.today.add_race(HorseRace(self.formatted_location(json_race_data, extension),
                                             self.get_start_time(json_race_data, extension)))

    def formatted_location(self, json_race_data, extension=None):
        location = self.get_race_location(json_race_data, extension)
        return 'Epsom' if location == 'Epsom Downs' else location

    def add_horse(self, race_title, name, odds, number, json_race_data, extension=None):
        if not self.today.get_race(race_title):
            self.add_new_horse_race(json_race_data, extension)
            self.add_new_horse(race_title, name, number, odds)
        elif not self.today.get_race(race_title).get_horse(name):
            self.add_new_horse(race_title, name, number, odds)
        else:
            self.update_horse_odds(race_title, name, odds)

    def add_new_horse(self, race_name, name, number, odds):
        self.today.get_race(race_name).add_horses(Horse(name, number, self.name, odds))

    def update_horse_odds(self, race_name, name, odds):
        self.today.get_horse(race_name, name).update_odds(self.name, odds)

    def get_race_urls(self):
        pass

    def get_indiv_race_data(self, new_or_update: str):
        pass

    def get_indiv_horse_data(self, json_race_data, race_title, extension=None):
        pass

    def update_data(self, json_race_data, race_title, extension=None):
        pass

    def get_race_title(self, json_race_data, extension=None):
        return f'{self.formatted_location(json_race_data, extension)} - {self.get_start_time(json_race_data, extension)}'

    def get_race_location(self, json_race_data, extension=None):
        return ''

    def get_start_time(self, json_race_data, extension=None):
        return ''

    def check_if_race_started(self, json_race_data, extension=None):
        return self.get_start_time(json_race_data, extension) > time.strftime("%A %d %B, %H:%M", time.localtime())


class Betfred(Bookmaker):
    def __init__(self, today):
        super().__init__(today)
        self.name = 'Betfred'
        self.all_race_url = "https://www.betfred.com/services/SportsBook/navigationlist"
        self.all_race_query_string = [
            {"region": "440", "language": "uk", "type": "bonavigationlist", "id": "254374.2", "dataflags": "12",
             "datasize": "8", "cachebust": "1658160592143"},
            {"region": "440", "language": "uk", "type": "bonavigationlist", "id": "250364.2", "dataflags": "12",
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
        self.races = [race['idfwmarketgroup'] for data in self.all_race_json_data for race in
                      data['Bonavigationnode']['marketgroups']]

    def get_indiv_race_data(self, new_or_update: str):
        with requests.Session() as session:
            for extension in self.races:
                query_string = {"language": "uk", "type": "marketgroup", "idfwmarketgroup": extension,
                                "dataflags": "12",
                                "datasize": "8", "cachebust": "1658160890508"}
                json_data = WebBrowsing.UrlOpener(session).open_url(self.race_url, query_string, self.headers)
                if self.check_if_race_started(json_data, extension=None):
                    title = self.get_race_title(json_data)
                    self.get_indiv_horse_data(json_data, title) if new_or_update == 'new' else self.update_data(
                        json_data, title)

    def get_start_time(self, json_race_data, extension=None):
        start_time = parser.isoparse(json_race_data['Marketgroup']['markets'][0]['tsstartiso'])
        return start_time.strftime("%A %d %B, %H:%M")

    def get_race_location(self, json_race_data, extension=None):
        return json_race_data['Marketgroup']['markets'][0]['venue']

    def get_indiv_horse_data(self, json_race_data, race_title, extension=None):
        for horse in json_race_data['Marketgroup']['markets'][0]['selections']:
            if horse['is1stfavourite'] != 'true' and horse['is2ndfavourite'] != 'true' and horse[
                'idfobolifestate'] != 'NR':
                name = format_horse_name(horse['name'])
                number = horse['competitornumber']
                try:
                    odds = functions.convert_to_decimal(horse['currentpriceup'], horse['currentpricedown'])
                except KeyError:
                    odds = '-'
                self.add_horse(race_title, name, odds, number, json_race_data)

    def update_data(self, json_race_data, race_title):
        for horse in json_race_data['Marketgroup']['markets'][0]['selections']:
            if horse['is1stfavourite'] != 'true' and horse['is2ndfavourite'] != 'true' and horse[
                'idfobolifestate'] != 'NR':
                name = format_horse_name(horse['name'])
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
        self.races = [f'{race["id"]}/{race["slug"]}' for data in
                      self.all_race_json_data[0]['data']['regionCompetitions'][0]['competitions'] for race in
                      data['events']]

    def get_indiv_race_data(self, new_or_update):
        with requests.Session() as session:
            for extension in self.races:
                url = f'https://sports.williamhill.com/data/rmp01/api/desktop/horse-racing/en-gb/racecard/{extension}'
                json_data = WebBrowsing.UrlOpener(session).open_url(url, '', self.headers)
                if self.check_if_race_started(json_data, extension=None):
                    title = self.get_race_title(json_data)
                    self.get_indiv_horse_data(json_data, title) if new_or_update == 'new' else self.update_data(
                        json_data,
                        title)

    def get_indiv_horse_data(self, json_race_data, race_title, extension=None):
        horse_ids = [[horse['title'], horse['runnerNum'], horse['selections'][0]] for horse in
                     json_race_data['data']['raceCardData']['marketCollections'][0]['raceCardTables'][0][
                         'raceCardRows']]
        for horse in horse_ids:
            runner = (json_race_data['data']['raceCardData']['selections'][horse[2]])
            if runner['priceNum'] != None and runner['status'] == 'A':
                name = format_horse_name(horse[0])
                number = horse[1]
                odds = functions.convert_to_decimal(runner['priceNum'], runner['priceDen'])
                self.add_horse(race_title, name, odds, number, json_race_data)

    def update_data(self, json_race_data, race_title):
        horse_ids = [[horse['title'], horse['runnerNum'], horse['selections'][0]] for horse in
                     json_race_data['data']['raceCardData']['marketCollections'][0]['raceCardTables'][0][
                         'raceCardRows']]

        for horse in horse_ids:
            runner = (json_race_data['data']['raceCardData']['selections'][horse[2]])
            if runner['priceNum'] != None and runner['status'] == 'A':
                name = format_horse_name(horse[0])
                odds = functions.convert_to_decimal(runner['priceNum'], runner['priceDen'])
                self.update_horse_odds(race_title, name, odds)

    def get_start_time(self, json_race_data, extension=None):
        time = parser.isoparse(json_race_data['data']['raceCardData']['event']['startDateTime']).astimezone(
            timezone('Europe/London'))
        return time.strftime("%A %d %B, %H:%M")

    def get_race_location(self, json_race_data, extension=None):
        return json_race_data['data']['raceCardData']['event']['eventName'][6:]


class PaddyPower(Bookmaker):
    def __init__(self, today):
        super().__init__(today)
        self.name = 'Paddy Power'
        self.all_race_url = "https://apisds.paddypower.com/sdspp/content-managed-page/v7"
        self.all_race_query_string = [{"_ak": "vsd0Rm5ph2sS2uaK", "betexRegion": "GBR", "capiJurisdiction": "intl",
                                       "cardsToFetch": ["18888", "SEO_CONTENT_SUMMARY"], "countryCode": "GB",
                                       "currencyCode": "GBP",
                                       "eventTypeId": "7", "exchangeLocale": "en_GB",
                                       "includeEuromillionsWithoutLogin": "false",
                                       "includeMarketBlurbs": "true", "includePrices": "true",
                                       "includeRaceCards": "true",
                                       "language": "en", "layoutFetchedCardsOnly": "true", "loggedIn": "false",
                                       "nextRacesMarketsLimit": "3", "page": "SPORT", "priceHistory": "3",
                                       "regionCode": "UK",
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
                query_string = {"_ak": "vsd0Rm5ph2sS2uaK", "betexRegion": "GBR", "capiJurisdiction": "intl",
                                "currencyCode": "GBP",
                                "eventTypeId": "7", "exchangeLocale": "en_GB", "includePrices": "true",
                                "includeRaceTimeform": "true",
                                "includeResults": "true", "language": "en", "priceHistory": "3", "raceId": extension,
                                "regionCode": "UK"}
                json_data = WebBrowsing.UrlOpener(session).open_url(self.race_url, query_string, self.headers)
                if self.check_if_race_started(json_data, extension):
                    title = self.get_race_title(json_data, extension)
                    self.get_indiv_horse_data(json_data, title,
                                              extension) if new_or_update == 'new' else self.update_data(json_data,
                                                                                                         title)

    def get_indiv_horse_data(self, json_race_data, race_title, extension):
        for race in (json_race_data['markets']):
            if json_race_data['markets'][race]['marketType'] == 'WIN':
                for runner in json_race_data['markets'][race]['runners']:
                    if runner['runnerStatus'] == 'ACTIVE' and 'Unnamed' and 'Favourite' not in runner['runnerName']:
                        number = runner['sortPriority']
                        name = format_horse_name(runner['runnerName'])
                        try:
                            odds = round(float(runner['winRunnerOdds']['trueOdds']['decimalOdds']['decimalOdds']), 2)
                        except:
                            odds = '-'
                        self.add_horse(race_title, name, odds, number, json_race_data, extension)

    def update_data(self, json_race_data, title):
        for race in (json_race_data['markets']):
            if json_race_data['markets'][race]['marketType'] == 'WIN':
                for runner in json_race_data['markets'][race]['runners']:
                    if runner['runnerStatus'] == 'ACTIVE' and 'Unnamed' and 'Favourite' not in runner['runnerName']:
                        name = format_horse_name(runner['runnerName'])
                        try:
                            odds = round(float(runner['winRunnerOdds']['trueOdds']['decimalOdds']['decimalOdds']), 2)
                        except:
                            odds = '-'
                        self.update_horse_odds(title, name, odds)

    def get_race_title(self, json_race_data, extension):
        return f"{self.get_race_location(json_race_data, extension)} - {self.get_start_time(json_race_data, extension)}"

    def get_race_location(self, json_race_data, extension):
        return json_race_data['races'][extension]['venue']

    def get_start_time(self, json_race_data, extension=None):
        race_time = parser.isoparse(json_race_data['races'][extension]['startTime']).astimezone(
            timezone('Europe/London'))
        return race_time.strftime("%A %d %B, %H:%M")


class BetVictor(Bookmaker):

    def __init__(self, today):
        super().__init__(today)
        self.name = 'BetVictor'
        self.all_race_url = "https://www.betvictor.com/api/sportsbook/sports/364/tree"
        self.all_race_query_string = [{"date": "today", "c": "en-gb"}]
        self.headers = {
            "cookie": "locale=en-gb; device_id=b090694c-63c4-4356-908f-70373446200a; _gcl_au=1.1.1195941356.1653511307; _mibhv=anon-1653511306989-6568333975_8834; _rdt_uuid=1653511307540.3565f9d7-1115-4210-bc23-b038f45b2a85; QuantumMetricUserID=a2f31f7232193b23f30a5f3704b364d8; OptanonAlertBoxClosed=2022-05-25T20:41:49.378Z; fp_token_7c6a6574-f011-4c9a-abdd-9894a102ccef=aVCqXg4KAKNm9zPBJN13e/yFxMy1ipjd3kVEqu3uxCo=; ever_logged_in=true; price_format_id=3; _gac_UA-27425583-4=1.1656246471.CjwKCAjwh-CVBhB8EiwAjFEPGX0jsbrdfDd7-pBqaOgWM2TaeiPdQI1NiQy4PfHda1Yt4B3pN6h7PxoCkZsQAvD_BwE; _gcl_aw=GCL.1656246472.CjwKCAjwh-CVBhB8EiwAjFEPGX0jsbrdfDd7-pBqaOgWM2TaeiPdQI1NiQy4PfHda1Yt4B3pN6h7PxoCkZsQAvD_BwE; login=Success; currency_prefix=^%^C2^%^A3; currency_iso_code=GBP; product_id=1; _vcmobi=ab47c5bbe8e3128713cf2504a51499eb; _gid=GA1.2.1707439751.1658765437; QuantumMetricSessionID=4ed3c8c1ff2d80fce77fc659cb52ff8a; _gat_UA-27425583-4=1; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Jul+25+2022+17^%^3A13^%^3A55+GMT^%^2B0100+(British+Summer+Time)&version=6.33.0&isIABGlobal=false&hosts=&consentId=5dffbc56-b0b6-45b5-b7fe-13b4b0669441&interactionCount=1&landingPath=NotLandingPage&groups=C0001^%^3A1^%^2CC0002^%^3A1^%^2CC0003^%^3A1^%^2CC0004^%^3A1&geolocation=GB^%^3BENG&AwaitingReconsent=false; _ga=GA1.1.1697580880.1653511307; _uetsid=51e0a0d00c3411ed85b7494ca1c3b691; _uetvid=185eb670dc6b11eca2db611bed58d70c; _ga_B1JTVFFX3P=GS1.1.1658765436.47.1.1658765638.24",
            "authority": "www.betvictor.com",
            "accept": "application/json",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "if-none-match": "W/^\^7a3b820884d8b3569bc232c64119c84a^^",
            "referer": "https://www.betvictor.com/en-gb/sports",
            "sec-ch-ua": "^\^.Not/A",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "^\^Windows^^",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "x-csrf-token": "8JcQ89xucZXpjg9B/IGIulXHiEoEWZeoNYZ5MPUuCoE="
        }

    def get_race_urls(self):
        self.races = [race['id'] for location in self.all_race_json_data for child in location for race in
                      child['children'] if race['eventInformation'][-16:] == 'Extra Place Race']

    def get_indiv_race_data(self, new_or_update: str):
        with requests.Session() as session:
            query_string = {"c": "en-gb"}
            for extension in self.races:
                url = f'https://www.betvictor.com/api/sportsbook/sports/364/events/{extension}/markets'
                json_data = WebBrowsing.UrlOpener(session).open_url(url, query_string, self.headers)
                if self.check_if_race_started(json_data, extension):
                    title = self.get_race_title(json_data, extension)
                    self.get_indiv_horse_data(json_data, title, extension) if new_or_update == 'new' else \
                        self.update_data(json_data, title, extension)

    def get_indiv_horse_data(self, json_race_data, race_title, extension):
        for market in json_race_data:
            if market['description'] == 'Outright':
                for horse in market['outcomes']:
                    if not horse['withdrawn']:
                        name = format_horse_name(horse['description'])
                        number = horse['raceCardNumber']
                        odds = round(horse['price'], 2) if horse['price'] > 0 else '-'
                        self.add_horse(race_title, name, odds, number, json_race_data, extension)

    def update_data(self, json_race_data, race_title, extension):
        for market in json_race_data:
            if market['description'] == 'Outright':
                for horse in market['outcomes']:
                    if not horse['withdrawn']:
                        name = format_horse_name(horse['description'])
                        odds = round(horse['price'], 2) if horse['price'] > 0 else '-'
                        self.update_horse_odds(race_title, name, odds)

    def get_race_location(self, json_race_data, extension):
        location = [child['description'] for location in self.all_race_json_data for child in location for race in child['children'] if race['id'] == extension][0]
        return self.remove_brackets(location).strip()

    def get_start_time(self, json_race_data, extension):
        for location in self.all_race_json_data:
            for child in location:
                for race in child['children']:
                    if race['id'] == extension:
                        start_time = race['description']
                        now = datetime.now()
                        return f'{now.strftime("%A %d %B")}, {start_time}'

    def remove_brackets(self, string):
        return re.sub("[\(\[].*?[\)\]]", "", string)


class Parimatch(BetVictor):

    def __init__(self, today):
        super().__init__(today)
        self.name = 'Parimatch'
        self.all_race_url = "https://www.parimatch.co.uk/api/sportsbook/sports/364/tree"
        self.all_race_query_string = [{"date": "today", "c": "en-gb"}]
        self.headers = {
    "cookie": "_vcmobi=bf494ccc12d53292ae505be41e206fef; locale=en-gb; price_format_id=2; device_id=a53d6aab-ef05-4541-ab96-f0480e2a85ea; OptanonAlertBoxClosed=2022-07-28T10:11:39.124Z; _gcl_au=1.1.239613667.1659003099; _gid=GA1.3.502365994.1659003099; _rdt_uuid=1659003099587.7bd35c18-fc8b-46e6-a5cd-95df5bdb5b4f; btagid=91481283; btag=a_49894b_11238c_; affid=24974; lc.storage=^{^}; product_id=1; _gcl_aw=GCL.1659003102.Cj0KCQjw54iXBhCXARIsADWpsG8JNVYi8vLaVjK1hRL_YUfPf2aQzK-UwwMhSc1WaEb81m2kyBHw_KoaAgXwEALw_wcB; _ga=GA1.3.1837780437.1659003099; _gac_UA-170459280-2=1.1659003102.Cj0KCQjw54iXBhCXARIsADWpsG8JNVYi8vLaVjK1hRL_YUfPf2aQzK-UwwMhSc1WaEb81m2kyBHw_KoaAgXwEALw_wcB; _uetsid=abbd75f00e5d11edb035c91c4c4225cd; _uetvid=abbde0500e5d11edaf095fd90c2926f7; cto_bundle=RwNn2l85Rkp3S0k5YzMyYzNLMGhQanAyTnJ3YklOSnphMVJxWEFXRVoyVm5LS0clMkIyekg4S05CbmRBdVdvM2w5UlFDc0t1UWljSTBqUmwlMkYxbmlHM3hvQWd3JTJCSXMlMkZjYW5JZEZmYkljOTRyM1N1bXhRUTJDZTZGZEpjZXk2VUpSQ2clMkZqS2RnMjdwODc4dXVEWUslMkJoWlo4M2hQOHclM0QlM0Q; QuantumMetricUserID=a2f31f7232193b23f30a5f3704b364d8; QuantumMetricSessionID=ef160dd15459a4129fa7ce7f20d54dcf; _ga_Q87HD4NJR7=GS1.1.1659003099.1.1.1659003275.0; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Jul+28+2022+11^%^3A14^%^3A35+GMT^%^2B0100+(British+Summer+Time)&version=6.35.0&isIABGlobal=false&hosts=&consentId=8e8f0fd0-1c08-4eb2-9247-8ef9453f4d42&interactionCount=1&landingPath=NotLandingPage&groups=C0003^%^3A1^%^2CC0002^%^3A1^%^2CC0001^%^3A1^%^2CC0004^%^3A1&geolocation=GB^%^3BENG&AwaitingReconsent=false",
    "authority": "www.parimatch.co.uk",
    "accept": "application/json",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "if-none-match": "W/^\^c81bb9e5dcdb5e5f7b309622c32818fb^^",
    "referer": "https://www.parimatch.co.uk/en-gb/sports/364",
    "sec-ch-ua": "^\^.Not/A",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "^\^Windows^^",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "x-csrf-token": "WefJNg+pyDIuNVJ42bRHnV6w4WaDgO8LGpw7pmKUNgQ="
}

    def get_indiv_race_data(self, new_or_update: str):
        with requests.Session() as session:
            query_string = {"c": "en-gb"}
            for extension in self.races:
                url = f'https://www.parimatch.co.uk/api/sportsbook/sports/364/events/{extension}/markets'
                json_data = WebBrowsing.UrlOpener(session).open_url(url, query_string, self.headers)
                if self.check_if_race_started(json_data, extension):
                    title = self.get_race_title(json_data, extension)
                    self.get_indiv_horse_data(json_data, title, extension) if new_or_update == 'new' else \
                        self.update_data(json_data, title, extension)


class LiveScoreBet(Bookmaker):

    def __init__(self, today):
        super().__init__(today)
        self.name = 'LiveScore Bet'
        self.all_race_url = 'https://gateway-uk.livescorebet.com/sportsbook/gateway/v1/view/horses/meetings'
        self.all_race_query_string = [{"lang": "en-gb"}]
        self.headers = {}

    def get_race_urls(self):
        for country in self.all_race_json_data[0]['meetingsToday'][0]['childs']:
            if country['name'] in ['United Kingdom', 'Ireland']:
                for event in country['childs']:
                    name = event['name']
                    for race in event['events']:
                        if race.get('extraPlaces'):
                            extension = race['id']
                            start_time = race['raceHour']
                            self.format_url_extension(name, start_time, extension)

    def format_url_extension(self, name, start_time, extension):
        self.races.append(f'{name}-{start_time.replace(":", "-")}/sev/{extension}')

    def get_indiv_race_data(self, new_or_update: str):
        with requests.Session() as session:
            for extension in self.races:
                query_string = {"eventid": {extension[-14:]}, "lang": "en-gb"}
                url = 'https://gateway-uk.livescorebet.com/sportsbook/gateway/v1/view/horses/event'
                json_data = WebBrowsing.UrlOpener(session).open_url(url, query_string, self.headers)
                if self.check_if_race_started(json_data, extension):
                    title = self.get_race_title(json_data, extension)
                    self.get_indiv_horse_data(json_data, title, extension) if new_or_update == 'new' else \
                        self.update_data(json_data, title, extension)

    def get_indiv_horse_data(self, json_race_data, race_title, extension=None):
        for event in json_race_data['currentEvent']:
            for market in event['markets']:
                if market['name'] == 'Racecard':
                    for horse in market['selections']:
                        if horse['kind'] == 'REGULAR' and not horse['suspended']:
                            odds = round(horse['odds'], 2)
                            name = format_horse_name(horse['name'])
                            for participant in event['participants']:
                                if participant['name'] == name:
                                    number = participant['jerseyNumber']
                                    self.add_horse(race_title, name, odds, number, json_race_data)
                                    continue

    def update_data(self, json_race_data, race_title, extension=None):
        for event in json_race_data['currentEvent']:
            for market in event['markets']:
                if market['name'] == 'Racecard':
                    for horse in market['selections']:
                        if horse['kind'] == 'REGULAR' and not horse['suspended']:
                            odds = round(horse['odds'], 2)
                            name = format_horse_name(horse['name'])
                            self.update_horse_odds(race_title, name, odds)

    def get_race_location(self, json_race_data, extension=None):
        return json_race_data['currentEvent'][0]['categories'][0]['name']

    def get_start_time(self, json_race_data, extension=None):
        start_time = f"{json_race_data['currentEvent'][0]['startTime'][:10]}, {json_race_data['currentEvent'][0]['raceHour']}"
        start_time = time.strptime(start_time, '%Y-%m-%d, %H:%M')
        return time.strftime('%A %d %B, %H:%M', start_time)


class VirginBet(LiveScoreBet):

    def __init__(self, today):
        super().__init__(today)
        self.name = 'Virgin Bet'
        self.all_race_url = "https://gateway.virginbet.com/sportsbook/gateway/v1/view/horses/racinghome"
        self.all_race_query_string = [{}]
        self.headers = {
    "authority": "gateway.virginbet.com",
    "accept": "*/*",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "client-app-version": "2.16.2447",
    "client-id": "web",
    "client-language": "en",
    "client-os-version": "default",
    "content-type": "application/json",
    "origin": "https://www.virginbet.com",
    "referer": "https://www.virginbet.com/",
    "request-id": "c4afd623-18fd-4e5b-8410-579cbe23ab8e",
    "sec-ch-ua": "^\^.Not/A",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "^\^Windows^^",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

    def get_indiv_race_data(self, new_or_update: str):
        with requests.Session() as session:
            for extension in self.races:
                query_string = {"eventid": {extension[-14:]}, "lang": "en-gb"}
                url = "https://gateway.virginbet.com/sportsbook/gateway/v1/view/horses/event"
                json_data = WebBrowsing.UrlOpener(session).open_url(url, query_string, self.headers)
                if self.check_if_race_started(json_data, extension):
                    title = self.get_race_title(json_data, extension)
                    self.get_indiv_horse_data(json_data, title, extension) if new_or_update == 'new' else \
                        self.update_data(json_data, title, extension)


class ThirtyTwoRed(Bookmaker):

    def __init__(self, today):
        super().__init__(today)
        self.name = '32Red'
        self.all_race_url = "https://eu-offering.kambicdn.org/offering/v2018/32red/meeting/horse_racing.json"
        self.all_race_query_string = [{"lang":"en_GB","market":"GB","client_id":"2","channel_id":"1","ncid":"1658856099490"}]
        self.headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Origin": "https://www.32red.com",
    "Referer": "https://www.32red.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "sec-ch-ua": "^\^.Not/A",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "^\^Windows^^"
}

    def get_race_urls(self):
        self.races = [race['id'] for meeting in self.all_race_json_data[0] if
                      meeting['context']['region']['name'] == 'UK & Ireland' for race in (meeting['events']) if
                      'ENHANCED_PLACE_TERMS' in race['tags']]

    def get_indiv_race_data(self, new_or_update: str):
        with requests.Session() as session:
            query_string = {"lang":"en_GB","market":"GB","client_id":"2","channel_id":"1","ncid":"1658858446198","includeParticipants":"true"}
            for extension in self.races:
                url = f'https://eu-offering.kambicdn.org/offering/v2018/32red/betoffer/event/{extension}.json'
                json_data = WebBrowsing.UrlOpener(session).open_url(url, query_string, self.headers)
                if self.check_if_race_started(json_data, extension):
                    title = self.get_race_title(json_data, extension)
                    self.get_indiv_horse_data(json_data, title, extension) if new_or_update == 'new' else \
                        self.update_data(json_data, title, extension)

    def get_indiv_horse_data(self, json_race_data, race_title, extension=None):
        for horse in json_race_data['betOffers'][0]['outcomes']:
            for runner in json_race_data['events'][0]['participants']:
                if horse['participantId'] == runner['participantId']:
                    if not runner['scratched']:
                        name = format_horse_name(horse['participant'])
                        number = horse['startNr']
                        odds = round(horse['odds'] / 1000, 2)
                        self.add_horse(race_title, name, odds, number, json_race_data, extension)

    def update_data(self, json_race_data, race_title, extension=None):
        for horse in json_race_data['betOffers'][0]['outcomes']:
            for runner in json_race_data['events'][0]['participants']:
                if horse['participantId'] == runner['participantId']:
                    if not runner['scratched']:
                        name = format_horse_name(horse['participant'])
                        odds = round(horse['odds'] / 1000, 2)
                        self.update_horse_odds(race_title, name, odds)

    def get_race_location(self, json_race_data, extension=None):
        return json_race_data['events'][0]['name']

    def get_start_time(self, json_race_data, extension=None):
        race_time = parser.isoparse(json_race_data['events'][0]['start']).astimezone(timezone('Europe/London'))
        return race_time.strftime("%A %d %B, %H:%M")


class Grosvenor(ThirtyTwoRed):

    def __init__(self, today):
        super().__init__(today)
        self.name = 'Grosvenor'
        self.all_race_url = 'https://eu-offering.kambicdn.org/offering/v2018/gruk/meeting/horse_racing'
        self.all_race_query_string = [{"lang":"en_GB","market":"GB"}]
        self.headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Origin": "https://www.grosvenorcasinos.com",
    "Referer": "https://www.grosvenorcasinos.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "sec-ch-ua": "^\^.Not/A",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "^\^Windows^^"
}

    def get_indiv_race_data(self, new_or_update: str):
        with requests.Session() as session:
            query_string = {"lang":"en_GB","market":"GB","client_id":"2","channel_id":"1","ncid":"1658858446198","includeParticipants":"true"}
            for extension in self.races:
                url = f'https://eu-offering.kambicdn.org/offering/v2018/gruk/betoffer/event/{extension}.json'
                json_data = WebBrowsing.UrlOpener(session).open_url(url, query_string, self.headers)
                if self.check_if_race_started(json_data, extension):
                    title = self.get_race_title(json_data, extension)
                    self.get_indiv_horse_data(json_data, title, extension) if new_or_update == 'new' else \
                        self.update_data(json_data, title, extension)


class Casumo(ThirtyTwoRed):

    def __init__(self, today):
        super().__init__(today)
        self.name = 'Casumo'
        self.all_race_url = 'https://eu-offering.kambicdn.org/offering/v2018/cauk/meeting/horse_racing.json'
        self.all_race_query_string = [{"lang":"en_GB","market":"GB","client_id":"2","channel_id":"1","ncid":"1658935543647"}]
        self.headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Origin": "https://www.casumo.com",
    "Referer": "https://www.casumo.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "sec-ch-ua": "^\^.Not/A",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "^\^Windows^^"
}

    def get_indiv_race_data(self, new_or_update: str):
        with requests.Session() as session:
            query_string = {"lang":"en_GB","market":"GB","client_id":"2","channel_id":"1","ncid":"1658858446198","includeParticipants":"true"}
            for extension in self.races:
                url = f'https://eu-offering.kambicdn.org/offering/v2018/cauk/betoffer/event/{extension}.json'
                json_data = WebBrowsing.UrlOpener(session).open_url(url, query_string, self.headers)
                if self.check_if_race_started(json_data, extension):
                    title = self.get_race_title(json_data, extension)
                    self.get_indiv_horse_data(json_data, title, extension) if new_or_update == 'new' else \
                        self.update_data(json_data, title, extension)


class LeoVegas(ThirtyTwoRed):

    def __init__(self, today):
        super().__init__(today)
        self.name = 'LeoVegas'
        self.all_race_url = 'https://eu-offering.kambicdn.org/offering/v2018/leoal/meeting/horse_racing.json'
        self.all_race_query_string = [{"lang":"en_GB","market":"GB","client_id":"2","channel_id":"1","ncid":"1658940431092"}]
        self.headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Origin": "https://www.leovegas.com",
    "Referer": "https://www.leovegas.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "sec-ch-ua": "^\^.Not/A",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "^\^Windows^^"
}

    def get_indiv_race_data(self, new_or_update: str):
        with requests.Session() as session:
            query_string = {"lang":"en_GB","market":"GB","client_id":"2","channel_id":"1","ncid":"1658858446198","includeParticipants":"true"}
            for extension in self.races:
                url = f'https://eu-offering.kambicdn.org/offering/v2018/leoal/betoffer/event/{extension}.json'
                json_data = WebBrowsing.UrlOpener(session).open_url(url, query_string, self.headers)
                if self.check_if_race_started(json_data, extension):
                    title = self.get_race_title(json_data, extension)
                    self.get_indiv_horse_data(json_data, title, extension) if new_or_update == 'new' else \
                        self.update_data(json_data, title, extension)


class MrGreen(ThirtyTwoRed):
    def __init__(self, today):
        super().__init__(today)
        self.name = 'Mr Green'
        self.all_race_url = "https://eu-offering.kambicdn.org/offering/v2018/mguk/meeting/horse_racing.json"
        self.all_race_query_string = [{"lang":"en_GB","market":"GB","client_id":"2","channel_id":"1","ncid":"1659003727782"}]
        self.headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Origin": "https://sport.mrgreen.com",
    "Referer": "https://sport.mrgreen.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "sec-ch-ua": "^\^.Not/A",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "^\^Windows^^"
}

    def get_indiv_race_data(self, new_or_update: str):
        with requests.Session() as session:
            query_string = {"lang":"en_GB","market":"GB","client_id":"2","channel_id":"1","ncid":"1658858446198","includeParticipants":"true"}
            for extension in self.races:
                url = f'https://eu-offering.kambicdn.org/offering/v2018/mguk/betoffer/event/{extension}.json'
                json_data = WebBrowsing.UrlOpener(session).open_url(url, query_string, self.headers)
                if self.check_if_race_started(json_data, extension):
                    title = self.get_race_title(json_data, extension)
                    self.get_indiv_horse_data(json_data, title, extension) if new_or_update == 'new' else \
                        self.update_data(json_data, title, extension)


class PokerStars(Bookmaker):
    def __init__(self, today):
        super().__init__(today)
        self.name = 'PokerStars'
        self.all_race_url = "https://sports.pokerstars.uk/sportsbook/v1/api/getSportTree"
        self.all_race_query_string = [
            {"sport":"HORSE_RACING","includeOutrights":"false","includeEvents":"true","includeCoupons":"true",
             "channelId":"6","locale":"en-gb","siteId":"32768"}]
        self.headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Cookie": "tsgCEedgeauth01=ip=51.19.216.32~exp=1659005897~acl=^%^2f*~id=MTIxNzk0MzQ4NQ^%^3d^%^3d~hmac=970fed295ba0626fb56b6740829b88ac6034903184ff607cb8bc73478c09063d; signalid=568562452226267; OptanonAlertBoxClosed=2022-07-12T15:16:34.189Z; pstrk.gid1=907123290-1657638991; _gcl_au=1.1.1851801803.1657638994; _scid=4585db6f-4c16-430d-8dc7-890ce5cfdb09; WIID=nvT1OGMNk5GXfX5vAHTEtmTJBoq5p72dgHUdDrGmo9H4nlhFoIKSyFQHj02JqjZ8YeigMu49lJbcjuRV3jLgVuMlyvRSoWV5; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Jul+28+2022+11^%^3A53^%^3A16+GMT^%^2B0100+(British+Summer+Time)&version=6.34.0&isIABGlobal=false&hosts=&genVendors=&consentId=XHJSJO&interactionCount=1&landingPath=NotLandingPage&groups=C0001^%^3A1^%^2CC0002^%^3A1^%^2CC0003^%^3A1^%^2CC0004^%^3A1&geolocation=GB^%^3BENG&AwaitingReconsent=false; _ga_QRHPGRCN1Q=GS1.1.1659005596.1.0.1659005596.0; LANG=en; XIID=635876271443192105; _ga=GA1.2.907123290-1657638991; _gid=GA1.2.126397550.1659005598; _gat=1; tsgCEedgeauth01=ip=51.19.216.32~exp=1659005897~acl=^%^2f*~id=NzM1MTkxNDY2~hmac=7f18693478ff2b789978638b17bdb33f728c400d501570bcb3b674a22fc6fbd3",
    "Origin": "https://www.pokerstars.uk",
    "Referer": "https://www.pokerstars.uk/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "sec-ch-ua": "^\^.Not/A",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "^\^Windows^^"
}

    def get_race_urls(self):
        for location in self.all_race_json_data[0]['categories']:
            if location['parent']['name'] == 'UK and Ireland':
                if location['competition'][0]['name'][-6:] == time.strftime("%d %b", time.localtime()):
                    for race in location['competition'][0]['event']:
                        for places in race['markets'][0]['attributes']['attrib']:
                            title = self.get_race_title(self.all_race_json_data, race['id'])
                            if self.today.get_race(title):
                                if places['key'] == 'numPlaces' and int(places['value']) > self.today.get_race(title).get_places():
                                    self.races.append(race['id'])

    def get_indiv_race_data(self, new_or_update: str):
        with requests.session() as session:
            for query_string in self.all_race_query_string:
                json_data = WebBrowsing.UrlOpener(session).open_url(self.all_race_url, query_string, self.headers)
                for race_id in self.races:
                    if self.check_if_race_started(json_data, race_id):
                        title = self.get_race_title(self.all_race_json_data, race_id)
                        self.get_indiv_horse_data(json_data, title, race_id) if new_or_update == 'new' else self.update_data(
                            json_data, title, race_id)

    def get_indiv_horse_data(self, json_race_data, race_title, extension=None):
        for location in self.all_race_json_data[0]['categories']:
            if location['parent']['name'] == 'UK and Ireland':
                if location['competition'][0]['name'][-6:] == time.strftime("%d %b", time.localtime()):
                    for race in location['competition'][0]['event']:
                        if race['id'] == extension:
                            for horse in race['markets'][0]['selection']:
                                if not horse['suspended']:
                                    name = format_horse_name(horse['name'])
                                    odds = round(float(horse['odds']['dec']), 2)
                                    number = horse['pos']['row']
                                    self.add_horse(race_title, name, odds, number, json_race_data, extension)


    def update_data(self, json_race_data, race_title, extension=None):
        for location in self.all_race_json_data[0]['categories']:
            if location['parent']['name'] == 'UK and Ireland':
                if location['competition'][0]['name'][-6:] == time.strftime("%d %b", time.localtime()):
                    for race in location['competition'][0]['event']:
                        if race['id'] == extension:
                            for horse in race['markets'][0]['selection']:
                                if not horse['suspended']:
                                    name = format_horse_name(horse['name'])
                                    odds = round(float(horse['odds']['dec']), 2)
                                    self.update_horse_odds(race_title, name, odds)

    def get_race_location(self, json_race_data, extension=None):
        for location in self.all_race_json_data[0]['categories']:
            if location['parent']['name'] == 'UK and Ireland':
                if location['competition'][0]['name'][-6:] == time.strftime("%d %b", time.localtime()):
                    for race in location['competition'][0]['event']:
                        if race['id'] == extension:
                            return race['categoryName']

    def get_start_time(self, json_race_data, extension=None):
        for location in self.all_race_json_data[0]['categories']:
            if location['parent']['name'] == 'UK and Ireland':
                if location['competition'][0]['name'][-6:] == time.strftime("%d %b", time.localtime()):
                    for race in location['competition'][0]['event']:
                        if race['id'] == extension:
                            return f'{datetime.now().strftime("%A %d %B")}, {race["name"][:5]}'

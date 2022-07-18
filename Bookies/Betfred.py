import requests
import json
import pandas as pd
from main import *

racesForToday = "https://www.betfred.com/services/SportsBook/navigationlist"
racesForTodayQuerystring = {"region":"440","language":"uk","type":"bonavigationlist","id":"254374.2","dataflags":"12","datasize":"8","cachebust":"1658160592143"}

headers = {
    "cookie": "visid_incap_2254385=ARD5TOf1RwK55Av/63oP/pQTjmIAAAAAQUIPAAAAAABnulSVh/H/pDSAYlgbp/7c; _gcl_au=1.1.1299117066.1653478296; __adal_ca=so^%^3Ddirect^%^26me^%^3Dnone^%^26ca^%^3Ddirect^%^26co^%^3D^%^28not^%^2520set^%^29^%^26ke^%^3D^%^28not^%^2520set^%^29; _tgci=0997f865-aaf3-5213-92b0-6520d39a7ea6; _tgpc=77aaac86-472c-52cb-998f-9e04ae2dde93; cd_user_id=180fafc8bf5f09-0cc5c73a3aa09a-26021851-1fa400-180fafc8bf6ea8; _hjSessionUser_688760=eyJpZCI6ImQwNmNlOWY0LTMwNzYtNTFjNi05ZDI0LTc3NjJlYzUzNDRhMyIsImNyZWF0ZWQiOjE2NTM0NzgyOTY3NDYsImV4aXN0aW5nIjp0cnVlfQ==; IA_AffiliateTracking=AffiliateID=10006&BTAG=a_107470b_c_Betfred-e-590045377658d_323778697; IA_AffiliateTracking_BTAG=a_107470b_c_Betfred-e-590045377658d_323778697; IA_AffiliateTracking_AffID=10006; BF_AffiliateTracking=AffiliateID=10006&trackingSystem=RV&trackingString=a_107470b_c_Betfred-e-590045377658d_323778697; BF_AffiliateTracking_BTAG=a_107470b_c_Betfred-e-590045377658d_323778697; BF_AffiliateTracking_ClickData=^{^\^click_id^^:323778697,^\^click_date^^:^\^2022-07-13",
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

all_races = []

response = requests.request("GET", racesForToday, headers=headers, params=racesForTodayQuerystring)
response.raise_for_status()
races = json.loads(response.text)

for race in races['Bonavigationnode']['marketgroups']:
    all_races.append(race['idfwmarketgroup'])

url = "https://www.betfred.com/services/SportsBook/marketgroup"

with requests.Session() as s:
    s.headers.update(headers)
    for extension in all_races:
        querystring = {"language": "uk", "type": "marketgroup", "idfwmarketgroup": extension, "dataflags": "12",
                       "datasize": "8", "cachebust": "1658160890508"}

        response = s.get(url, params=querystring)
        response.raise_for_status()
        data = json.loads(response.text)
        prices = []

        for horse in data['Marketgroup']['markets'][0]['selections']:
            if horse['is1stfavourite'] != 'true' and horse['is2ndfavourite'] != 'true' and horse['idfobolifestate'] != 'NR':
                prices = add_names_and_prices(prices, horse['name'], horse['competitornumber'],
                                              convert_to_decimal(horse['currentpriceup'], (horse['currentpricedown'])))
        df = pd.DataFrame(data=prices, columns=['Name', 'Number', 'Betfred']).sort_values(by=['Betfred'])
        print(df)



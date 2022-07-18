import requests
import json
import pandas as pd
from main import *

url = "https://www.betfred.com/services/SportsBook/event"

event_id = '23255712.2'

querystring = {"language":"uk","type":"event","eventid":event_id,"dataflags":"14","datasize":"8","cachebust":"1658156041303"}

headers = {
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
    "referer": "https://www.betfred.com/sports/event/23255712.2",
    "sec-ch-ua": "^\^.Not/A",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "^\^Windows^^",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 "
                  "Safari/537.36",
    "x-betfred": "Betfred Website (Desktop)",
    "x-instana-l": "1,correlationType=web;correlationId=80372f46d1e80381",
    "x-instana-s": "80372f46d1e80381",
    "x-instana-t": "80372f46d1e80381"
}

response = requests.request("GET", url, headers=headers, params=querystring)
response.raise_for_status()
data = json.loads(response.text)

prices = []

for horse in data['Event']['markets'][0]['selections']:
    try:
        if horse['competitornumber']:
            prices = add_names_and_prices(prices, horse['name'], horse['competitornumber'],
                                          convert_to_decimal(horse['currentpriceup'], (horse['currentpricedown'])))

    except:
        pass

df = pd.DataFrame(data=prices, columns=['Name', 'Number', 'Betfred']).sort_values(by=['Betfred'])
print(df)
import requests
import json

def convert_to_decimal(num: float, den: float):
    return round(num/den+1, 2)

all_races_url = "https://sports.williamhill.com/data/rmp01/api/desktop/horse-racing/en-gb/meetings/extra-places/tomorrow"

headers = {
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
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 "
                  "Safari/537.36 "
}

payload = ""
response = requests.request("GET", all_races_url, data=payload, headers=headers)
response.raise_for_status()

#with open('EPdataWH.json') as f:
    #races = json.load(f)

races = json.loads(response.text)
all_races = []
jsonPosition = races['data']['regionCompetitions'][0]['competitions']
print(jsonPosition)
for race in jsonPosition:
    for x in race['events']:
        print(x['id'])



with open('WHdata.json') as f:
    data = json.load(f)

#url = "https://sports.williamhill.com/data/rmp01/api/desktop/horse-racing/en-gb/racecard/OB_EV24632314/1710-newton-abbot"

payload = ""
#data = requests.request("GET", url, data=payload, headers=headers)
#data.raise_for_status()

prices = []

runners = data['data']['raceCardData']['event']['numberOfRunners']
for runner in data['data']['raceCardData']['selections']:
    if runners > 0:
        runner = data['data']['raceCardData']['selections'][runner]
        prices.append(convert_to_decimal(runner['priceNum'], runner['priceDen']))
        runners -= 1
    else:
        break

print(prices)



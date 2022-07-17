import requests
import json

def convert_to_decimal(num: float, den: float):
    return round(num/den+1, 2)

all_races_url = "https://sports.williamhill.com/data/rmp01/api/desktop/horse-racing/en-gb/meetings/extra-places/tomorrow"

payload = ""
#response = requests.request("GET", all_races_url, data=payload)
#response.raise_for_status()

with open('EPdataWH.json') as f:
    races = json.load(f)

#races = json.loads(response.text)
all_races = []
jsonPosition = races['data']['regionCompetitions'][0]['competitions']
print(jsonPosition)
for race in jsonPosition:
    for x in race['events']:
        print(x['id'])



#with open('WHdata.json') as f:
    #data = json.load(f)

url = "https://sports.williamhill.com/data/rmp01/api/desktop/horse-racing/en-gb/racecard/OB_EV24632314/1710-newton-abbot"

payload = ""
data = requests.request("GET", url, data=payload)
data.raise_for_status()

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



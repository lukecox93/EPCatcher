import html5lib as html5lib
import requests
from bs4 import BeautifulSoup

URL = 'https://m.skybet.com/horse-racing/curragh/event/29895027'

payload = ""

headers = {
    'cookie': "sbgCFcustrandno01=87.14; sbgCFSplashPage=^%^7B^%^22showSplash^%^22^%^3Anull^%^7D; rememberMeCookie=whurling; config=^%^7B^%^22app^%^22^%^3A^%^22web^%^22^%^2C^%^22version^%^22^%^3A-1^%^2C^%^22regStatus^%^22^%^3A^%^22FULL^%^22^%^2C^%^22loyaltyStatus^%^22^%^3A^%^22^%^22^%^2C^%^22customerGroup^%^22^%^3Anull^%^2C^%^22showCookieNotice^%^22^%^3Afalse^%^2C^%^22showBalance^%^22^%^3Atrue^%^2C^%^22hideHeaderPromo^%^22^%^3A^%^221640952000^%^22^%^7D; AMCVS_EDAB367D5AB0E5190A495EDF^%^40AdobeOrg=1; s_cc=true; ak_bmsc=D8D65DE149F185D933637A9ACE08BB16~000000000000000000000000000000~YAAQBEwQAv8oqQqCAQAAyew/DBBy3O/j7K8Zo4lkYGnKuwN7sbQbkMYgS4ZsGrcWBFBnSYiOW7tcmmXtxtQvuJRcY3J1j7XlhjPt+7tofei+RJgPcIV2uwS2RFjX9TnlTUMbrXDnzco1yptdoBtcS6+5hbuf6OcvSXDx+99PRTLInocd8I/DmZxMhPaQ5acnw/rMjzqMFopFZj1gMaPEJ0QInAliTrTqKIUQQMYvOU+z01Dj/xxjVae5Pdq/tlAUZDAlDARcweTWSkHdhpb1584XEExVH7IPPiFMYOAi0ff57Dgx0nZBqLyjdJmQ1Ejvvv59eJr/sGHTlbr305n7P2uqR6sbor+ZB7JYImFHWt4jWoTMqdwareSiVzjq+tBHA/3z7RlvwK/sXc9jmts4NujyhjZky2jWuOjhyb9JctcPM+HNSDoGRtqB73xr/oMABAwvir8PbX8HR8iNeYVShnPpZL/T7YW9IxPknGnwoCGnKSn60G3IaZlc; AMCV_EDAB367D5AB0E5190A495EDF^%^40AdobeOrg=-1303530583^%^7CMCIDTS^%^7C19191^%^7CMCMID^%^7C21656774213091643953461767672353472639^%^7CMCAAMLH-1658667982^%^7C6^%^7CMCAAMB-1658667982^%^7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y^%^7CMCOPTOUT-1658070382s^%^7CNONE^%^7CMCAID^%^7CNONE^%^7CvVersion^%^7C3.3.0; gamingCEdevice1_2=^%^7B^%^22df^%^22^%^3A^%^22other^%^22^%^2C^%^22of^%^22^%^3A^%^22unknown^%^22^%^2C^%^22ov^%^22^%^3A-1^%^2C^%^22dm^%^22^%^3A^%^22tablet^%^22^%^2C^%^22bn^%^22^%^3A^%^22Chrome^%^22^%^2C^%^22bv^%^22^%^3A103^%^2C^%^22s^%^22^%^3A^%^7B^%^22w^%^22^%^3A750^%^2C^%^22h^%^22^%^3A500^%^2C^%^22r^%^22^%^3A2^%^7D^%^7D; akacd_skybet_m=1658064352~rv=11~id=2e02aff3bcecb13cec2d22b9e556b95a; SSOSESSID=qch0utcitjceemm3i02800u113; TINYSESSID=4ii46cjn4ajvgnmjofhoebc3o2; sbgCEedgeauth01=ip=51.19.216.32~exp=1658064353~acl=^%^2f*~id=MTIxODEzNDgyMw^%^3d^%^3d~hmac=8244130a0ca62ed7af34c17e230f50e02da2b888ca20687a093584cb4dc940b6; __SBA_POLLTIME=1658064088716^|loggedOut^|true; s_sq=^%^5B^%^5BB^%^5D^%^5D; sbgCAprevPN01=^%^2Fmbet^%^2Fhorse-racing^%^2Fcurragh^%^2Fpre-live^%^2F29895026; bm_sv=59E4F82A629FAC90E824F0B929060456~YAAQxjndWNIZ8/2BAQAA7tZSDBBWDTBVYZ+thoPGGABRX3dj23yYZ626yy7lrlFBjndJDrn7Nmj6h9IfWIW2uabFQHFFYbtUevoTeYbMd7y1QImMO3pRsaCNAVJ7HY9zptHGIyNwK4zElOXmrzgQBkI2W/Ze1xeUh+zX/wU/rAuMK98pwG//ns92eB5/OR1dxqQrXi9ie/127FAM0ah2M652phSL+KzRibae1vS7t0PMcp2kf6W8dVN7/e3zhJrdQw==~1",
    'authority': "m.skybet.com",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    'accept-language': "en-GB,en-US;q=0.9,en;q=0.8",
    'cache-control': "max-age=0",
    'referer': "https://m.skybet.com/horse-racing/redcar/event/29894958",
    'sec-ch-ua': "^\^.Not/A",
    'sec-ch-ua-mobile': "?0",
    'sec-ch-ua-platform': "^\^Windows^^",
    'sec-fetch-dest': "document",
    'sec-fetch-mode': "navigate",
    'sec-fetch-site': "same-origin",
    'sec-fetch-user': "?1",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }

response = requests.get(URL, data=payload, headers=headers)
response.raise_for_status()
soup = BeautifulSoup(response.content)
prices = soup.find_all('span', 'js-oc-price')
runners = soup.find_all('span', '_1elyepi')
print(prices)
#for horse in range(runners):
    #print(prices[horse])
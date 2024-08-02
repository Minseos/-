import requests
import time
import pandas as pd
import sqlalchemy
import dbio

from naver_api_info import client_id, client_secret
from dotenv import load_dotenv
from datetime import date
from sqlalchemy import create_engine
from datetime import datetime

client_id = client_id # 네이버 api에 접속 가능한 id 
client_secret = client_secret # 네이버 api에 접속 가능한 pw 

url = f"https://openapi.naver.com/v1/search/news.json"
payload = {'query' : '핀테크', 'display': 100, 'start' : 1, 'sort' : 'date'}
headers = {'X-Naver-Client-Id' : client_id, 'X-Naver-Client-Secret' : client_secret}
r = requests.get(url, params = payload, headers = headers)

if(r.status_code == 200):
    data = r.json()
    print(type(data))
    print(data)
else:
    print("Error Cde:", r.status_code)
    
today = date.today()

formatted_date = today.strftime('%d %b %Y')
print(formatted_date)

def text_clean(x):
    x = x.replace('&quot;', '').replace('<b>','').replace('</b>', '')
    return x

result = {}
for item in data['items']:
    if formatted_date in item['pubDate']:
        for key in item.keys():
            result.setdefault(key, []).append(text_clean(item[key]))
    else:
        break

df = pd.DataFrame(result)
dbio.news_to_db('fintech_news', str(today), df)
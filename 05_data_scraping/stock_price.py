import os
import pandas as pd
from datetime import date
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pymysql
import time
import requests
from bs4 import BeautifulSoup as bs

pymysql.install_as_MySQLdb()
load_dotenv(dotenv_path = '.env_db')

def str2int(x):
    x = int(x.replace(",",""))
    return x

def db_connect():
    engine = create_engine("mysql+pymysql://root:1234@127.0.0.1:3306/korea_stock_info")
    conn = engine.connect()
    return conn


# DB에 접속해서 저장하는 함수
def stock_info_to_db(idx, code, df):
    today = str(date.today()).replace("-","_")
    conn = db_connect()    
    df.to_sql(f"{today[:7]}_stock_price_info", con=conn, if_exists='append', index=False)
    conn.close()
    
    return print(f"{today}, {idx}, {code}, {'저장완료':<30s}", end="\r")


def stock_info_scraping():
    # mysql에서 테이블 불러오기
    conn = db_connect()
    data = pd.read_sql(f'2024_07_30_stock_company_info2', con=conn)
    conn.close()
    print(data)

    errors = {}
    for idx, (company, code) in enumerate(zip(data['회사명'], data['종목코드'])):
        stock_price_detail = {}#한바퀴 돌때마다 딕셔너리가 만들어지고
        url = f"https://finance.naver.com/item/main.naver?code={code}" 
        try: #혹시라도 에러나더라도 코드 계속 실행될 수 있도록 try except
            r = requests.get(url)
            print(r.status_code, f"{idx+1}/{len(data['종목코드'])} 수집중                    ", end="\r")
            soup = bs(r.text, 'lxml')
            # 가격
            price = int((soup.select_one(".today").text).strip("\n").split("\n")[1].replace(",", ""))
            # 변동금액
            price_chage = int((soup.select_one(".today").text).strip("\n").split("\n")[9].replace(",", ""))
            # 변화율
            rate_of_chage = float(((soup.select_one(".today").text).strip("\n").split("\n")[13]+(soup.select_one(".today").text).strip("\n").split("\n")[15]).replace("%",""))
            stock_price_detail.setdefault('수집일', []).append(str(date.today()))
            stock_price_detail.setdefault('회사명', []).append(company)
            stock_price_detail.setdefault('종목코드', []).append(code)
            stock_price_detail.setdefault('현재가', []).append(price)
            stock_price_detail.setdefault('변동금액', []).append(price_chage)
            stock_price_detail.setdefault('변화율', []).append(rate_of_chage)
            table = soup.select_one(".no_info")
            for tr in table.select("tr"):
                for td in tr.select('td'):
                    stock_price_detail.setdefault(td.select_one('span').text, []).append(str2int(td.select_one("span.blind").text))
            df = pd.DataFrame(stock_price_detail) #반복문 끝나는 부분에서 데이터 프레임으로 만들어지고
            stock_info_to_db(idx, code, df) #데베에 저장하는코드를 통해 넣어주고
            time.sleep(5)
        except Exception as e:
            print(e)
            print(r.status_code, f"{idx+1}/{len(data['종목코드'])} 수집중 에러", end="\r")
            errors.setdefault("에러", []).append(code)  # 에러난 코드들 모음
    return print(f"{str(date.today())} 주식 수집 완료")
            
    stock_price_detail

if __name__ == "__main__":
    stock_info_scraping()
   
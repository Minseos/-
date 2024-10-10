import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import time
from datetime import date
import os
from sqlalchemy import create_engine, text
import pymysql

# 오늘 날짜 설정
today = date.today()
today = str(today)

# MySQL 접속 정보 설정
dbtype = "pymysql"
user = "root"
password = "1234"
host = "127.0.0.1:3306"
database = "korea_stock"  # 사용할 데이터베이스 이름


# 데이터 수집 부분 (기존 코드 사용)
page = 1
page_size = 100
final_result_df = pd.DataFrame()
while True:
    url = "https://kind.krx.co.kr/corpgeneral/corpList.do"
    payload = dict(method='searchCorpList', pageIndex=page, currentPageSize=page_size, orderMode=3, orderStat='D', searchType=13, fiscalYearEnd='all', location='all')
    r = requests.get(url, params=payload)
    print(r.status_code, end="\r")
    soup = bs(r.text, 'lxml')
    total_items = int(soup.select_one(".info.type-00 > em").text.replace(",", ""))
    total_pages = total_items // page_size + 1
    print(f"{page}/{total_pages} 수집중", end="\r")
    keys = soup.select_one("table.list.type-00.tmt30")['summary'].split(", ")  
    result = {}
    for tr in soup.select('tr'):
        for idx, (key, td) in enumerate(zip(keys, tr.select('td'))):
            if idx == 0:
                kinds = [img['alt'].strip() for img in td.select('img')]   # 1번째 증권 종류, 회사이름
                kind = ", ".join(kinds)
                code = td.select_one('a')['onclick'].split("'")[1]+"0" # 종목코드 추출
                result.setdefault('증권종류', []).append(kind) # 증권종류 저장
                result.setdefault(key, []).append(td.text)   # 회사이름 저장
                result.setdefault('종목코드', []).append(code)
            elif idx == 6:
                home_link = td.select_one('a')['href'] if td.string == None else ""  # 6번째 링크 찾기
                result.setdefault(key, []).append(home_link)
            else:
                result.setdefault(key, []).append(td.text)
    result_df = pd.DataFrame(result)
    final_result_df = pd.concat([final_result_df, result_df])
        
    if page < total_pages:
        page += 1
        time.sleep(5)
    else:
        break

# 데이터 확인
print(final_result_df)

# CSV로 저장
final_result_df.to_csv(f"상장기업정보_{today}기준.csv", encoding='utf-8', index=False)

# 이미 저장된 CSV 파일 불러오기
final_result_df = pd.read_csv(f"./상장기업정보_{today}기준.csv")

# MySQL 연결 설정
pymysql.install_as_MySQLdb()

# MySQL 서버에 연결 (데이터베이스를 지정하지 않고 접속)
engine = create_engine(f"mysql+{dbtype}://{user}:{password}@{host}")

# MySQL 연결 열기 및 데이터베이스 생성
with engine.connect() as conn:
    # 데이터베이스가 존재하지 않으면 생성
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {database};"))
    print(f"'{database}' 데이터베이스가 성공적으로 생성되었거나 이미 존재합니다.")

# 데이터베이스와 연결을 다시 시도
engine = create_engine(f"mysql+{dbtype}://{user}:{password}@{host}/{database}")
conn = engine.connect()

# 연결 성공 여부 확인
print("Connected to the database.")

# DataFrame을 MySQL 테이블로 저장
table_name = f"company_info"

# MySQL로 데이터 저장
final_result_df.to_sql(name=table_name, con=conn, if_exists='replace', index=False)

# 연결 닫기
conn.close()

print(f"데이터가 MySQL의 '{table_name}' 테이블에 성공적으로 저장되었습니다.")

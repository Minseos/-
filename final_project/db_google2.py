import os
import pandas as pd
import pymysql
from dbenv import id, pw, host, database  # MySQL 연결 정보 가져오기

# MySQL 연결 정보
db_config = {
    "host": host.split(":")[0],
    "port": int(host.split(":")[1]) if ":" in host else 3306,
    "user": id,
    "password": pw,
    "database": database
}

# CSV 파일 경로 설정
# csv_dir = r'C:\study\fintech\final_project\data\리뷰추출\구글최종'
csv_dir = r'C:\fintech_service\final_project\data\리뷰추출\구글최종'

# 데이터베이스 테이블 명
table_name = 'reviews'

# stores 테이블에서 store_name과 store_id를 매핑
def get_store_id_mapping():
    connection = pymysql.connect(**db_config)
    store_mapping = {}
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT store_id, store_name FROM stores")
            result = cursor.fetchall()
            for row in result:
                store_mapping[row[1]] = row[0]
    finally:
        connection.close()
    return store_mapping

# 날짜 형식 변환
def convert_date(date_str):
    try:
        return pd.to_datetime(date_str).strftime('%Y-%m-%d')
    except Exception as e:
        print(f"날짜 변환 오류: {e} (원본 값: {date_str})")
        return None

# CSV 파일들을 데이터베이스에 삽입하는 함수
def insert_kakao_reviews():
    store_mapping = get_store_id_mapping()

    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]

        for file in csv_files:
            store_name = file.replace('.csv', '').strip()
            if store_name.startswith('~$'):  # 잘못된 파일 이름 건너뛰기
                print(f"잘못된 파일 이름 '{store_name}' 건너뜁니다.")
                continue

            store_id = store_mapping.get(store_name)
            if not store_id:
                print(f"store_name '{store_name}'에 해당하는 store_id를 찾을 수 없습니다. 건너뜁니다.")
                continue

            file_path = os.path.join(csv_dir, file)
            data = pd.read_csv(file_path)
            data = data.where(pd.notnull(data), None)

            insert_query = f"""
            INSERT INTO {table_name} (
                store_id, platform, review_date, review_text, final_sentiment,
                taste, service, quantity, sentiment, sentiment2
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            rows_to_insert = [
                (
                    store_id,
                    "구글",
                    convert_date(row['Date']),
                    row['Review'],
                    row['Final_Sentiment'],
                    row['맛'],
                    row['서비스'],
                    row['양'],
                    row['sentiment'],
                    row['Sentiment2']
                )
                for _, row in data.iterrows()
            ]
            cursor.executemany(insert_query, rows_to_insert)
            connection.commit()

        print("모든 구글 리뷰 데이터가 데이터베이스에 삽입되었습니다.")

    except Exception as e:
        print(f"오류 발생: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

# 실행
insert_kakao_reviews()

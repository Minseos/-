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
# csv_dir = r'C:\study\fintech\final_project\data\리뷰추출\업종정보\병합결과'
csv_dir = r'C:\fintech_service\final_project\data\리뷰추출\업종정보\병합결과'

# 데이터베이스 테이블 명
table_name = 'stores'

# CSV 파일들을 데이터베이스에 삽입하는 함수
def insert_csv_to_db():
    try:
        # DB 연결
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        # 파일 목록 가져오기
        csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]

        for file in csv_files:
            # CSV 파일 읽기
            file_path = os.path.join(csv_dir, file)
            data = pd.read_csv(file_path)

            # NaN 값을 None으로 변환 (MySQL의 NULL과 호환되도록)
            data = data.where(pd.notnull(data), None)

            # SQL INSERT 쿼리 작성
            insert_query = f"""
            INSERT INTO {table_name} (
                store_name, category, address, phone_number, business_hours,
                price_range, naver_rating, kakao_rating, google_rating
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # 데이터 삽입 (배치 처리)
            rows_to_insert = [
                (
                    str(row.get('가게이름')) if pd.notnull(row.get('가게이름')) else None,  # 문자열로 변환
                    str(row.get('카테고리')) if pd.notnull(row.get('카테고리')) else None,
                    str(row.get('주소')) if pd.notnull(row.get('주소')) else None,
                    str(row.get('전화번호')) if pd.notnull(row.get('전화번호')) else None,
                    str(row.get('영업시간')) if pd.notnull(row.get('영업시간')) else None,
                    str(row.get('가격대')) if pd.notnull(row.get('가격대')) else None,
                    float(row.get('네이버 별점')) if pd.notnull(row.get('네이버 별점')) else None,
                    float(row.get('카카오 별점')) if pd.notnull(row.get('카카오 별점')) else None,
                    float(row.get('구글 별점')) if pd.notnull(row.get('구글 별점')) else None
                )
                for _, row in data.iterrows()
            ]
            cursor.executemany(insert_query, rows_to_insert)
            connection.commit()

        print("모든 CSV 파일의 데이터가 데이터베이스에 삽입되었습니다.")

    except Exception as e:
        print(f"오류 발생: {e}")

    finally:
        # 연결 닫기
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

# 함수 실행
insert_csv_to_db()

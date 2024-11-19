import os
import pymysql
import pandas as pd
from dbenv import id, pw, host, database  # dbenv.py에서 MySQL 연결 정보 가져오기
import re

# MySQL 연결 정보
db_config = {
    "host": host.split(":")[0],  # 호스트 주소 추출
    "port": int(host.split(":")[1]) if ":" in host else 3306,  # 포트 번호 추출
    "user": id,
    "password": pw,
    "database": database
}

# 데이터 폴더 경로
data_folder = r"C:\fintech_service\final_project\data\리뷰추출"

# 테이블 이름 생성 함수
def generate_table_name(filename):
    # 파일명에서 "_reviews" 제거, 공백과 특수문자를 "_"로 변환
    table_name = os.path.splitext(filename)[0].replace("_reviews", "").strip()
    table_name = re.sub(r"[^\w]", "_", table_name)  # 알파벳, 숫자, 밑줄만 허용
    return table_name.lower()  # 소문자로 변환

# MySQL 연결 및 CSV 데이터 삽입
def insert_all_csv_to_separate_tables(folder_path):
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            # 폴더 내 모든 CSV 파일 탐색
            for filename in os.listdir(folder_path):
                if filename.endswith(".csv"):  # CSV 파일만 처리
                    file_path = os.path.join(folder_path, filename)

                    # 테이블 이름 생성
                    table_name = generate_table_name(filename)
                    print(f"테이블 생성 및 데이터 삽입 시작: {table_name}")

                    # 테이블 자동 생성
                    cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS `{table_name}` (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            date VARCHAR(20),
                            review TEXT
                        );
                    """)

                    # CSV 파일 로드
                    data = pd.read_csv(file_path)

                    # NaN 값을 포함한 행 제거
                    data.dropna(subset=["Date", "Review"], inplace=True)

                    # 데이터 삽입
                    for _, row in data.iterrows():
                        sql = f"INSERT INTO `{table_name}` (date, review) VALUES (%s, %s)"
                        cursor.execute(sql, (row["Date"], row["Review"]))

                    print(f"{filename} 데이터를 {table_name} 테이블에 성공적으로 삽입했습니다!")

        # 변경 사항 저장
        connection.commit()
        print("모든 CSV 데이터를 MySQL에 성공적으로 삽입했습니다!")

    except Exception as e:
        print(f"에러 발생: {e}")

    finally:
        connection.close()

# 실행
if __name__ == "__main__":
    insert_all_csv_to_separate_tables(data_folder)

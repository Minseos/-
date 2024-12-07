import pymysql
from firebase_admin import credentials, initialize_app, storage
from dbenv import id, pw, host, database  # MySQL 연결 정보 가져오기

# Firebase 초기화
cred = credentials.Certificate("C:/study/fintech/final_project/final-project-8f802-firebase-adminsdk-dxoaf-794617e2ee.json")
initialize_app(cred, {'storageBucket': 'final-project-8f802.firebasestorage.app'})  # 올바른 버킷 이름 사용

# MySQL 연결 정보
db_config = {
    "host": host.split(":")[0],
    "port": int(host.split(":")[1]) if ":" in host else 3306,
    "user": id,
    "password": pw,
    "database": database
}

# Firebase 폴더 경로
firebase_folders = {
    "menu_photo": "menu",
    "wordcloud": "1_WordCloud",
    "negative_ratio": "2_NegativeReview_Ratio",
    "distribution": "3_Distribution",
    "keyword": "4_Keyword",
    "raderchart": "5_RadarChart"
}

# 처리할 store_id 리스트
target_store_ids = [10, 15, 19, 43]

# Firebase에서 파일 URL 가져오기
def get_file_url(folder, store_id, is_distribution=False):
    bucket = storage.bucket()

    if is_distribution:
        # Distribution 파일은 하나만 고정 사용
        blob = bucket.blob(f"{folder}/weighted_rating_vs_price.png")
        if blob.exists():
            return blob.generate_signed_url(version="v4", expiration=3600)
    else:
        # 파일 검색 (store_id가 포함된 파일 이름)
        blobs = list(bucket.list_blobs(prefix=folder))
        for blob in blobs:
            if str(store_id) in blob.name:
                return blob.generate_signed_url(version="v4", expiration=3600)

    return None

# MySQL 연결 및 Firebase 데이터 업데이트
def update_analysis_table():
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            for store_id in target_store_ids:
                print(f"\n처리 중인 Store ID: {store_id}")

                # 각 컬럼별 데이터 처리
                update_data = {}
                for column, folder in firebase_folders.items():
                    if column == "distribution":
                        file_url = get_file_url(folder, store_id, is_distribution=True)
                    else:
                        file_url = get_file_url(folder, store_id)

                    if file_url:
                        update_data[column] = file_url
                        print(f"{column} - URL: {file_url}")
                    else:
                        print(f"{column} - Firebase에서 파일을 찾을 수 없습니다: {store_id}")

                # analysis 테이블에 데이터 업데이트
                cursor.execute(f"""
                    INSERT INTO analysis (store_id, menu_photo, wordcloud, negative_ratio, distribution, keyword, raderchart)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE 
                        menu_photo = VALUES(menu_photo),
                        wordcloud = VALUES(wordcloud),
                        negative_ratio = VALUES(negative_ratio),
                        distribution = VALUES(distribution),
                        keyword = VALUES(keyword),
                        raderchart = VALUES(raderchart)
                """, (
                    store_id,
                    update_data.get("menu_photo"),
                    update_data.get("wordcloud"),
                    update_data.get("negative_ratio"),
                    update_data.get("distribution"),
                    update_data.get("keyword"),
                    update_data.get("raderchart")
                ))

                print(f"Store ID {store_id} 데이터 업데이트 완료")

            # 변경사항 커밋
            connection.commit()
            print("\n모든 데이터 처리 완료")
    except Exception as e:
        print(f"에러 발생: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    # 실행
    print("\n--- 분석 테이블 업데이트 시작 ---")
    update_analysis_table()

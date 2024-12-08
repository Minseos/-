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
    "distribution": "3_Distribution/weighted_rating_vs_price.png",  # 단일 파일 처리
    "keyword": "4_Keyword",
    "raderchart": "5_RadarChart"
}

# 처리할 store_id 리스트
target_store_ids = [10, 15, 19, 43]

# Firebase에서 파일 경로 가져오기
def get_file_path(folder, store_id):
    bucket = storage.bucket()

    if folder.endswith(".png"):  # distribution 전용 처리
        blob = bucket.blob(folder)
        if blob.exists():
            return f"gs://{bucket.name}/{blob.name}"
    else:
        blobs = list(bucket.list_blobs(prefix=folder))
        for blob in blobs:
            if f"/{store_id}_" in blob.name or blob.name.endswith(f"/{store_id}.png") or blob.name.endswith(f"/{store_id}.jpg"):
                return f"gs://{bucket.name}/{blob.name}"

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
                    file_path = get_file_path(folder, store_id)
                    if file_path:
                        update_data[column] = file_path
                        print(f"{column} - Path: {file_path}")
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
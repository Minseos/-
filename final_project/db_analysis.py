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

# 워드클라우드 파일 경로 (Firebase 폴더 경로)
wordcloud_folder = "1_WordCloud"

# 처리할 store_id 리스트
target_store_ids = [10, 15, 19, 43]

# Firebase에서 파일 목록 확인
def list_files():
    bucket = storage.bucket()
    blobs = bucket.list_blobs(prefix=wordcloud_folder)  # 특정 폴더 내 파일만 검색
    print("\nFirebase Storage 파일 목록:")
    for blob in blobs:
        print(f"파일 이름: {blob.name}")  # 각 파일 이름 출력

# Firebase에서 특정 파일 검색 및 디버깅
def debug_blob_search(store_id):
    filename = f"{wordcloud_folder}/{store_id}_wordcloud.png"
    print(f"검색하려는 파일 경로: {filename}")
    
    bucket = storage.bucket()

    blob = bucket.blob(filename)
    
    if blob.exists():
        print(f"파일 찾음: {filename}")
        return True
    else:
        print(f"파일을 찾을 수 없음: {filename}")
        return False

# MySQL 연결 및 Firebase 데이터 업데이트
def update_analysis_table():
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            for store_id in target_store_ids:
                print(f"\n처리 중인 Store ID: {store_id}")

                # Firebase에서 파일 검색
                filename = f"{wordcloud_folder}/{store_id}_wordcloud.png"
                if debug_blob_search(store_id):  # 파일 존재 여부 확인
                    # Firebase에서 다운로드 URL 생성
                    bucket = storage.bucket()
                    blob = bucket.blob(filename)
                    download_url = blob.generate_signed_url(version="v4", expiration=3600)
                    print(f"Firebase URL: {download_url}")

                    # analysis 테이블에 데이터 업데이트
                    cursor.execute("""
                        INSERT INTO analysis (store_id, wordcloud)
                        VALUES (%s, %s)
                        ON DUPLICATE KEY UPDATE wordcloud = %s
                    """, (store_id, download_url, download_url))
                    print(f"analysis 테이블에 {store_id}의 워드클라우드 URL 업데이트 완료")
                else:
                    print(f"Store ID {store_id}에 대한 파일을 Firebase에서 찾을 수 없습니다.")

            # 변경사항 커밋
            connection.commit()
            print("\n모든 데이터 처리 완료")
    except Exception as e:
        print(f"에러 발생: {e}")
    finally:
        connection.close()

def debug_firebase_bucket():
    try:
        bucket = storage.bucket()
        print(f"Firebase Storage 연결 성공! 버킷 이름: {bucket.name}")
    except Exception as e:
        print(f"Firebase Storage 연결 실패: {e}")

if __name__ == "__main__":
    debug_firebase_bucket()

    # 실행
    print("\n--- Firebase 파일 목록 확인 ---")
    list_files()  # Firebase Storage 파일 목록 출력
    print("\n--- 분석 테이블 업데이트 시작 ---")
    update_analysis_table()  # MySQL 데이터 업데이트

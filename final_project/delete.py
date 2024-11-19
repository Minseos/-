import pymysql
from dbenv import id, pw, host, database  # dbenv.py에서 MySQL 연결 정보 가져오기

# MySQL 연결 정보
db_config = {
    "host": host.split(":")[0],
    "port": int(host.split(":")[1]) if ":" in host else 3306,
    "user": id,
    "password": pw,
    "database": database
}

# 삭제할 테이블 목록
tables_to_delete = [
    "our948", "s카페", "가정식집밥_세로방", "고가네철판불백", "고래똥", "고품격커피공장_뱅뱅사거리점",
    "곰바로곰탕", "곰작골나주곰탕_역삼초교점", "교토일식", "궁민김밥_본점", "깡돈", "낙여삼",
    "남강매점", "남순남순대국_본점", "노브랜드버거_뱅뱅사거리점", "다돈식당", "다슬음_강남점", "더벤티_뱅뱅사거리점",
    "돼지벅스_강남점", "두두", "두메_도곡점", "뚜레쥬르_뱅뱅사거리점", "라망드쉐프", "리첸",
    "만복회해산물_뱅뱅사거리점", "맥켄치킨", "명동할머니국수_뱅뱅사거리점", "무화잠", "문화시민_서울",
    "뱅뱅막국수", "버드나무집_서초동본점", "봉구스밥버거_역삼삼일점", "봉평착한메밀_본점", "봉피양_양재점",
    "북경반점", "브라운돈까스_뱅뱅사거리점", "비채", "사람사는고깃집김일도_뱅뱅점", "사천루",
    "소뭉집_본점", "스타벅스_서초태우빌딩점", "시원한대구탕", "아티제_강남유니온센터점", "아티제_뱅뱅사거리점",
    "양재족발_참족", "에슬로우_뱅뱅사거리점", "에이림커피", "영이네", "예당", "오늘은_어떤_닭",
    "오로스트커피", "오하나_도곡점", "왕산골", "원할매이모네닭한마리", "월참치", "이천쌀밥",
    "잇풀", "장수촌풍천장어", "전주피순대", "조순금닭도리탕", "중화카츠_덮밥_역삼본점",
    "지우네", "짜짜루", "짜짜루_추천순", "청담배짱이", "카린지린가네스낵바_뱅뱅사거리점",
    "카페블랑131", "칸꼬시", "커피박스", "큐뮬러스", "통돼지두루치기김치찌개전문점",
    "파라노이드_강남뱅뱅_카페", "파리바게뜨_뱅뱅사거리점", "판문점부대찌개_역삼점",
    "해머스미스커피_뱅뱅사거리점", "회춘식당"
]

def drop_tables(tables):
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")  # 외래 키 제약 비활성화
            for table in tables:
                print(f"Deleting table: {table}")
                cursor.execute(f"DROP TABLE IF EXISTS `{table}`;")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")  # 외래 키 제약 재활성화

        connection.commit()
        print("모든 테이블을 성공적으로 삭제했습니다!")

    except Exception as e:
        print(f"에러 발생: {e}")

    finally:
        connection.close()

# 실행
if __name__ == "__main__":
    drop_tables(tables_to_delete)

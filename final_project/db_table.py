import pymysql
import re
from dbenv import id, pw, host, database  # MySQL 연결 정보 가져오기

# MySQL 연결 정보
db_config = {
    "host": host.split(":")[0],
    "port": int(host.split(":")[1]) if ":" in host else 3306,
    "user": id,
    "password": pw,
    "database": database
}

# 가게 리스트
store_list = [
    "스노우폭스_뱅뱅점", "맥도날드_서초뱅뱅점", "큐뮬러스", "유니마카롱", "짜짜루",
    "아티제_강남유니온센터점", "어가람", "드시옹", "웰니스_쌀빵", "파리바게뜨_뱅뱅사거리점",
    "파라노이드_강남뱅뱅_카페", "아티제_뱅뱅사거리점", "만복회해산물_뱅뱅사거리점", "해머스미스커피_뱅뱅사거리점",
    "월참치", "쿡쿡쿡_뱅뱅사거리점", "파스타엔포크_강남역삼점", "고가네철판불백", "곰작골나주곰탕_역삼초교점",
    "사람사는고깃집김일도_뱅뱅점", "잇풀키토김밥_샌드위치_샐러드_강남점", "엄마손맛집밥세로방",
    "고불초쌈밥_2호점", "우심터", "난타5000", "봉구스밥버거_역삼삼일점", "세로방", "커피콩스토리",
    "더에이치", "9CAFE", "소뭉집_본점", "리첸", "지우네", "중화카츠", "교토일식", "회춘식당",
    "노브랜드버거_뱅뱅사거리점", "라망드쉐프", "서초골", "에슬로우커피_뱅뱅사거리점", "전주피순대",
    "오로스트커피", "다슬음", "조순금닭도리탕", "궁민김밥", "더벤티_뱅뱅사거리점", "돼지벅스",
    "시원한대구탕", "판문점부대찌개_역삼점", "청담배짱이", "통돼지_두루치기김치찌개", "봉평착한메밀",
    "칸꼬시", "곰바로곰탕", "문화시민", "오늘은_어떤닭", "카페블랑131", "버드나무집_서초본점",
    "파스쿠찌_뱅뱅사거리점", "남강매점", "스타벅스_서초태우빌딩점", "맥켄치킨", "봉피양_양재점",
    "깡돈", "북경반점", "무화잠_강남점", "아워948", "참족", "예당", "다돈식당", "낙여삼",
    "명동할머니국수_뱅뱅사거리점", "이천쌀밥", "또봉이통닭_도곡점", "카린지린가네스낵바_뱅뱅사거리점",
    "왕산골", "서초남순남순대국_본점", "브라운돈까스_뱅뱅사거리점", "고품격커피공장_뱅뱅사거리점",
    "두두돼지불백", "사천루", "장수촌풍천장어", "뱅뱅막국수_역삼본점", "커피박스", "뚜레쥬르_뱅뱅사거리점",
    "멜론", "오아시스", "에이림커피", "카페S", "원할매이모네닭한마리",
    "영이네추억의떡볶이", "비채", "한강수", "고래똥", "두메_도곡점", "썸", "샵5827_에스프레소", "메종보탄",
    "오하나_도곡점"
]

# 테이블 이름 생성 함수
def generate_table_name(store_name):
    return re.sub(r"[^\w]", "_", store_name.strip()).lower()

# MySQL 연결 및 테이블 생성
def create_tables():
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            for store_name in store_list:
                table_name = generate_table_name(store_name)

                # 테이블 생성 SQL
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS `{table_name}` (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        platform VARCHAR(50),   -- 플랫폼 (네이버, 카카오, 구글 등)
                        date VARCHAR(20),       -- 리뷰 작성 날짜
                        review TEXT             -- 리뷰 내용
                    );
                """)
                print(f"테이블 생성 완료: {table_name}")

            # 변경 사항 저장
            connection.commit()
            print("모든 테이블이 성공적으로 생성되었습니다!")

    except Exception as e:
        print(f"에러 발생: {e}")
    finally:
        connection.close()

# 실행
if __name__ == "__main__":
    create_tables()

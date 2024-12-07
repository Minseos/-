from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS
from dbenv import id, pw, host, database
import os

app = Flask(
    __name__, 
    template_folder=os.path.join('C:/fintech_service/final_project', 'templates')
)
CORS(app)

# MySQL 연결 정보
db_config = {
    "host": host.split(":")[0],
    "port": int(host.split(":")[1]) if ":" in host else 3306,
    "user": id,
    "password": pw,
    "database": database
}

# 카테고리 매핑 함수
def map_category(category):
    category_map = {
        "한식": ['한식', '곰탕,설렁탕', '돼지고기구이', '낙지요리', '백반,가정식', '육류,고기요리', '순대,순댓국', '찌개,전골', '정육식당', '장어,먹장어요리', '족발,보쌈', '한식뷔페', '닭요리', '국수'],
        "중식": ['중식당'],
        "일식": ['일식당', '생선회', '초밥,롤', '돈가스'],
        "양식": ['이탈리아음식', '햄버거'],
        "분식": ['분식', '종합분식', '김밥'],
        "카페/디저트": ['카페', '카페,디저트', '베이커리'],
        "치킨": ['치킨,닭강정'],
        "해물": ['게요리', '매운탕,해물탕', '해물,생선요리'],
        "요리주점": ['요리주점', '바(BAR)', '맥주,호프', '포장마차'],
        "다이어트": ['샌드위치']
    }
    for main_category, sub_categories in category_map.items():
        if category in sub_categories:
            return main_category
    return "기타"

# 1. `/markers` 엔드포인트: 모든 가게 데이터를 반환
@app.route('/markers', methods=['GET'])
def get_markers():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT s.store_id, s.store_name AS name, s.address, s.category, a.menu_photo
            FROM stores s
            LEFT JOIN analysis a ON s.store_id = a.store_id
        """
        cursor.execute(query)
        results = cursor.fetchall()

        for result in results:
            result['main_category'] = map_category(result['category'])

        return jsonify(results)
    except Exception as e:
        print(f"Error in /markers: {str(e)}")
        return jsonify({"error": "데이터를 불러오는 중 문제가 발생했습니다."}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



# 2. `/reviews/<store_id>` 엔드포인트: 특정 가게의 상세 리뷰 데이터를 반환 - 상세 정보
@app.route('/reviews/<int:store_id>', methods=['GET'])
def get_reviews(store_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT DATE_FORMAT(review_date, '%Y-%m') AS review_date,
                   review_text,
                   platform,
                   naver_rating,
                   kakao_rating,
                   google_rating,
                   stores.store_name,
                   stores.address,
                   stores.phone_number,
                   stores.business_hours,
                   stores.price_range
            FROM reviews 
            JOIN stores ON stores.store_id = reviews.store_id
            WHERE reviews.store_id = %s
            ORDER BY review_date DESC
        """
        cursor.execute(query, (store_id,))
        reviews = cursor.fetchall()

        if not reviews:
            return jsonify({"message": "리뷰가 없습니다."}), 404

        response = {
            "store_name": reviews[0]['store_name'].replace('_', ' '),  # 여기에서 _를 공백으로 변경
            "address": reviews[0]['address'],
            "phone_number": reviews[0]['phone_number'] or "-",
            "business_hours": reviews[0]['business_hours'] or "-",
            "price_range": reviews[0]['price_range'] or "-",
            "reviews": reviews
        }
        return jsonify(response)
    except Exception as e:
        print(f"Error in /reviews/<store_id>: {str(e)}")
        return jsonify({"error": "서버에서 문제가 발생했습니다."}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# 3. `/search_reviews` 엔드포인트: 키워드로 리뷰 검색 - 마커 부분
@app.route('/search_reviews', methods=['GET'])
def search_reviews():
    keyword = request.args.get('keyword', '').strip()

    if not keyword:
        return jsonify({"search_results": []})

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT stores.store_id, stores.store_name AS name, stores.address, stores.category,
                   COUNT(reviews.review_id) AS keyword_count
            FROM reviews
            JOIN stores ON stores.store_id = reviews.store_id
            WHERE reviews.review_text LIKE %s
            GROUP BY stores.store_id, stores.store_name, stores.address, stores.category
        """
        cursor.execute(query, (f"%{keyword}%",))
        results = cursor.fetchall()

        for result in results:
            result['main_category'] = map_category(result['category'])

        return jsonify({"search_results": results})
    except Exception as e:
        print(f"Error in /search_reviews: {str(e)}")
        return jsonify({"error": "검색 중 문제가 발생했습니다."}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
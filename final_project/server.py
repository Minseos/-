from flask import Flask, jsonify, request, render_template
import mysql.connector
from flask_cors import CORS
from dbenv import id, pw, host, database  # MySQL 연결 정보 가져오기

app = Flask(__name__)
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

@app.route('/markers', methods=['GET'])
def get_markers():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT store_id, store_name AS name, address, category FROM stores"
        cursor.execute(query)
        results = cursor.fetchall()

        for result in results:
            result['main_category'] = map_category(result['category'])

        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/reviews/<int:store_id>', methods=['GET'])
def get_reviews(store_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT review_date, review_text, final_sentiment 
            FROM reviews 
            WHERE store_id = %s
            ORDER BY review_date DESC
        """
        cursor.execute(query, (store_id,))
        reviews = cursor.fetchall()

        if not reviews:
            return jsonify({"message": "리뷰가 없습니다."}), 404

        return jsonify(reviews)
    except mysql.connector.Error as e:
        return jsonify({"error": f"MySQL Error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/reviews.html')
def render_reviews_page():
    return render_template('reviews.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)

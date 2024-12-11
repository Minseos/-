from flask import Flask, jsonify, request, send_from_directory, render_template
import mysql.connector
from flask_cors import CORS
from dotenv import load_dotenv
import os
import urllib.parse

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# 기본 이미지 URL
DEFAULT_MENU_PHOTO = "https://via.placeholder.com/150"

load_dotenv(dotenv_path = '.env')

# MySQL 연결 정보
db_config = {
    "host": os.getenv("host", "localhost").split(":")[0],
    "port": int(os.getenv("host", "localhost:3306").split(":")[1]) if ":" in os.getenv("host", "localhost:3306") else 3306,
    "user": os.getenv("id", "root"),
    "password": os.getenv("pw", ""),
    "database": os.getenv("database", "test")
}



#루트 경로에서 kakao.html 렌더링
@app.route('/')
def home():
    return render_template('kakao.html')

# gs:// URL을 HTTP URL로 변환하는 함수
def convert_gs_to_http(gs_url):
    if gs_url.startswith("gs://"):
        bucket_name = "final-project-8f802.firebasestorage.app"  # 정확한 버킷 이름
        path = gs_url.replace(f"gs://{bucket_name}/", "")  # `gs://` 경로 제거
        encoded_path = urllib.parse.quote(path, safe="")  # URL 인코딩
        return f"https://firebasestorage.googleapis.com/v0/b/{bucket_name}/o/{encoded_path}?alt=media"
    return gs_url



@app.route('/markers', methods=['GET'])
def get_markers():
    # conn = None
    # cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT s.store_id, s.store_name AS name, s.address, 
                CASE 
                    WHEN s.store_id IN (10, 15, 19, 43) THEN '고기/구이'
                    ELSE s.category
                END AS category,
                COALESCE(a.menu_photo, %s) AS menu_photo
            FROM stores s
            LEFT JOIN analysis a ON s.store_id = a.store_id
        """
        cursor.execute(query, (DEFAULT_MENU_PHOTO,))
        results = cursor.fetchall()

        for result in results:
            result['menu_photo'] = convert_gs_to_http(result['menu_photo'])

        return jsonify(results)
    except mysql.connector.Error as e:
        print(f"Error in /markers: {e}")
        return jsonify({"error": "MySQL에서 문제가 발생했습니다."}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# reviews.html 파일 렌더링을 위한 라우트 추가
@app.route('/reviews.html')
def reviews_page():
    store_id = request.args.get('storeId')
    if not store_id:
        return jsonify({"error": "storeId가 제공되지 않았습니다."}), 400
    return render_template('reviews.html', store_id=store_id)


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
                stores.price_range,
                COALESCE(analysis.menu_photo, %s) AS menu_photo
            FROM reviews 
            JOIN stores ON stores.store_id = reviews.store_id
            LEFT JOIN analysis ON stores.store_id = analysis.store_id
            WHERE reviews.store_id = %s
            ORDER BY review_date DESC
        """
        cursor.execute(query, (DEFAULT_MENU_PHOTO, store_id))
        reviews = cursor.fetchall()

        if not reviews:
            return jsonify({"message": "리뷰가 없습니다."}), 404

        response = {
            "store_name": reviews[0]['store_name'].replace('_', ' '),
            "address": reviews[0]['address'],
            "phone_number": reviews[0]['phone_number'] or "-",
            "business_hours": reviews[0]['business_hours'] or "-",
            "price_range": reviews[0]['price_range'] or "-",
            "menu_photo": convert_gs_to_http(reviews[0]['menu_photo']),
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
                   COUNT(reviews.review_id) AS keyword_count,
                   COALESCE(analysis.menu_photo, %s) AS menu_photo
            FROM reviews
            JOIN stores ON stores.store_id = reviews.store_id
            LEFT JOIN analysis ON stores.store_id = analysis.store_id
            WHERE reviews.review_text LIKE %s
            GROUP BY stores.store_id, stores.store_name, stores.address, stores.category, analysis.menu_photo
        """
        cursor.execute(query, (DEFAULT_MENU_PHOTO, f"%{keyword}%"))
        results = cursor.fetchall()

        for result in results:
            result['menu_photo'] = convert_gs_to_http(result['menu_photo'])

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
    app.run(host='0.0.0.0', port=5000, debug=True)


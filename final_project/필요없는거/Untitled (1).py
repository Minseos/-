#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# WebDriver 초기화
driver = webdriver.Chrome()
driver.get("https://www.google.com/maps")

# 검색어 입력 및 검색
try:
    search_box = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="searchboxinput"]'))
    )
    search_box.send_keys("뱅뱅막국수")
    search_box.send_keys(Keys.ENTER)
except Exception as e:
    print(f"검색창을 찾을 수 없습니다: {e}")
    driver.quit()
    exit()

# 페이지 로드 대기
time.sleep(5)

# 리뷰 페이지 열기
try:
    review_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(@aria-label, "리뷰 더보기")]'))
    )
    review_button.click()
    time.sleep(5)  # 리뷰 페이지가 완전히 로드되도록 추가 대기
except Exception as e:
    print(f"리뷰 페이지를 열 수 없습니다: {e}")
    driver.quit()
    exit()

# 리뷰 크롤링 데이터프레임 초기화
reviews_list = []

# 스크롤 다운하여 모든 리뷰 로드
def scroll_down():
    scrollable_div = None
    # 스크롤 가능한 리뷰 섹션이 로드될 때까지 대기
    for _ in range(5):  # 시도 횟수 조정 가능
        try:
            scrollable_div = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]'))
            )
            break  # 요소가 로드되면 루프 종료
        except:
            time.sleep(2)  # 요소가 로드되지 않으면 잠시 대기 후 재시도

    # 리뷰 섹션이 로드되지 않았을 경우 함수 종료
    if scrollable_div is None:
        print("스크롤 가능한 리뷰 섹션을 찾을 수 없습니다.")
        return

    # 스크롤을 끝까지 반복 수행
    last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
    for _ in range(30):  # 필요한 만큼 스크롤 반복
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
        time.sleep(2)
        
        new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
        if new_height == last_height:  # 더 이상 새로운 내용이 없을 때 종료
            break
        last_height = new_height

scroll_down()

# 리뷰 데이터 수집
reviews = driver.find_elements(By.CSS_SELECTOR, '.jftiEf.fontBodyMedium')

for review in reviews:
    try:
        # 리뷰 작성자 ID
        reviewer_id = review.find_element(By.CSS_SELECTOR, '.d4r55').text
        # 리뷰 작성 날짜
        date = review.find_element(By.CSS_SELECTOR, '.rsqaWe').text
        # 리뷰 내용
        review_text = review.find_element(By.CSS_SELECTOR, '.wiI7pd').text
    except:
        continue

    # 리스트에 리뷰 추가
    reviews_list.append({
        "ID": reviewer_id,
        "Date": date,
        "Review": review_text
    })

# 리스트를 데이터프레임으로 변환
reviews_df = pd.DataFrame(reviews_list)

# 수집된 리뷰 데이터 출력
print(reviews_df)

# 엑셀 파일로 저장
reviews_df.to_excel('bangbang_makguksu_reviews.xlsx', index=False)

# 드라이버 종료
driver.quit()


# In[ ]:





# In[ ]:


import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# WebDriver 초기화
driver = webdriver.Chrome()
driver.get("https://www.google.com/maps")

# 검색어 입력 및 검색
try:
    search_box = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="searchboxinput"]'))
    )
    search_box.send_keys("뱅뱅막국수")
    search_box.send_keys(Keys.ENTER)
except Exception as e:
    print(f"검색창을 찾을 수 없습니다: {e}")
    driver.quit()
    exit()

# 페이지 로드 대기
time.sleep(5)

# "리뷰 더보기" 버튼 클릭
try:
    review_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="ChZDSUhNMG9nS0VJQ0FnSUNYaGUyYkZBEAE"]/span'))
    )
    review_button.click()
    time.sleep(5)  # 리뷰 페이지가 완전히 로드되도록 추가 대기
except Exception as e:
    print(f"리뷰 페이지를 열 수 없습니다: {e}")
    driver.quit()
    exit()

# 리뷰 크롤링 데이터프레임 초기화
reviews_list = []

# 스크롤 다운하여 모든 리뷰 로드
def scroll_down():
    try:
        scrollable_div = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]'))
        )
        
        last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
        for _ in range(50):  # 필요한 만큼 스크롤 반복
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
            time.sleep(2)
            
            new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
            if new_height == last_height:  # 더 이상 새로운 내용이 없을 때 종료
                break
            last_height = new_height
    except Exception as e:
        print("스크롤 가능한 리뷰 섹션을 찾을 수 없습니다.")
        print(f"오류: {e}")
        driver.quit()
        exit()

scroll_down()

# 리뷰 데이터 수집
reviews = driver.find_elements(By.CSS_SELECTOR, '.jftiEf.fontBodyMedium')

for review in reviews:
    try:
        # 리뷰 작성자 ID
        reviewer_id = review.find_element(By.CSS_SELECTOR, '.d4r55').text
        # 리뷰 작성 날짜
        date = review.find_element(By.CSS_SELECTOR, '.rsqaWe').text
        # 리뷰 내용
        review_text = review.find_element(By.CSS_SELECTOR, '.wiI7pd').text
    except Exception as e:
        print(f"리뷰 수집 중 오류: {e}")
        continue

    # 리스트에 리뷰 추가
    reviews_list.append({
        "ID": reviewer_id,
        "Date": date,
        "Review": review_text
    })

# 리스트를 데이터프레임으로 변환
reviews_df = pd.DataFrame(reviews_list)

# 수집된 리뷰 데이터 출력
print(reviews_df)

# 엑셀 파일로 저장
reviews_df.to_excel('bangbang_makguksu_reviews.xlsx', index=False)

# 드라이버 종료
driver.quit()


import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from time import sleep
import base64  
import os
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

# 웹페이지 제목
st.title("📊 최적의 투자 분석을 통한 배당주 투자 예측 웹페이지")

# 1. 월 투자 금액 입력
st.subheader("1. 월 투자 금액 입력")
investment_krw = st.number_input("한 달 투자 금액을 입력하세요 (만원 단위)", min_value=1, value=100) * 10000
st.write(f"매달 투자 금액: {investment_krw:,} 원")

# 2. 투자 기간 입력
st.subheader("2. 투자 기간 입력")
investment_years = st.slider("투자 기간을 선택하세요 (년)", min_value=1, max_value=30, value=10)

# 프로그레스바
progress = st.progress(0)
for percent_complete in range(0, 100, 20):
    sleep(0.1)
    progress.progress(percent_complete + 20)

# 3. 추천 종목 미국 주식 (티커 입력)
st.subheader("3. 추천 종목 입력")
tickers_input = st.text_input("추천할 종목의 티커를 입력하세요 (예: AAPL, MSFT, KO)", "AAPL, MSFT, KO")
tickers = [ticker.strip() for ticker in tickers_input.split(',')]

# 주식 데이터를 가져오는 함수
# 기존의 st.cache를 st.cache_data로 변경
@st.cache_data
def load_stock_data(tickers):
    data = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info
        dividend_yield = info.get('dividendYield', 0)
        if dividend_yield > 0:  # 배당금이 없는 주식 제외
            data.append({
                'Ticker': ticker,
                'Company': info.get('shortName', ''),
                'Price': info.get('previousClose', 0),
                'Dividend Yield (%)': dividend_yield * 100,
                'Dividend Rate (USD)': info.get('dividendRate', 0)
            })
    return pd.DataFrame(data)


# 데이터 불러오기
stock_df = load_stock_data(tickers)

# 4. 미래 배당금 예측 (10년, 20년)
years = [10, 20]
for year in years:
    stock_df[f'{year}년 예상 배당금 (USD)'] = stock_df['Dividend Rate (USD)'] * investment_krw / stock_df['Price'] * year

# 4.1 배당금 예측 시각화
st.subheader("4. 미래 배당금 예측")
fig = px.bar(stock_df, x='Company', y=[f'{years[0]}년 예상 배당금 (USD)', f'{years[1]}년 예상 배당금 (USD)'],
             title="10년 및 20년 예상 배당금",
             labels={'value': '배당금 (USD)', 'Company': '종목 이름'})
st.plotly_chart(fig)

# 5. 누적 배당금 및 다중 지표 분석
st.subheader("5. 누적 배당금 분석")
fig2 = px.line(stock_df, x='Company', y=[f'{years[0]}년 예상 배당금 (USD)', f'{years[1]}년 예상 배당금 (USD)'],
              title="누적 배당금 분석",
              labels={'value': '배당금 (USD)', 'Company': '종목 이름'})
st.plotly_chart(fig2)

# 결과 요약
st.write(f"한 달 {investment_krw / 10000} 만원을 {investment_years}년 동안 투자할 경우, 상위 3개 배당주에서 "
         f"최대 수익을 낼 수 있는 종목은 다음과 같습니다. 10년과 20년 후 예상 배당금을 확인하세요!")

 
# 원금과 누적 배당금 계산 함수 
def calculate_total_investment_and_dividends(investment_krw, investment_years, stock_df):
    # 필요한 열이 생성되었는지 확인하고, 없으면 생성
    target_column = f'{investment_years}년 예상 배당금 (USD)'
    if target_column not in stock_df.columns:
        stock_df[target_column] = stock_df['Dividend Rate (USD)'] * investment_krw / stock_df['Price'] * investment_years

    # 원금과 배당금 계산 열 추가
    stock_df[f'{investment_years}년 후 원금 + 배당금 (USD)'] = (
        (investment_krw * 12 * investment_years / stock_df['Price']) * stock_df['Price']
        + stock_df[target_column]
    )

    # 총 수령 금액 계산
    total_value = stock_df[f'{investment_years}년 후 원금 + 배당금 (USD)'].sum()
    return total_value

# 5. 원금과 배당금 합계 계산
total_investment_and_dividends = calculate_total_investment_and_dividends(investment_krw, investment_years, stock_df)

# 결과 출력
st.subheader("💰 원금 + 배당금 확인")

# 원금 + 배당금 계산 결과 출력
st.write(f"**{investment_years}년 후 예상 총 수령 금액**: {total_investment_and_dividends:,.2f} USD")
st.write(f"**한화 환산 금액 (1,300 KRW/USD 환율 가정)**: {total_investment_and_dividends * 1300:,.0f} 원")

# 6. 배당 수익률 상위 10개 기업 추천
st.subheader("6. 배당 수익률 상위 10개 기업 추천")
sp500_tickers = ["AAPL", "MSFT", "NVDA", "INTC", "KO", "PEP", "JNJ", "PG", "XOM", "IBM", "T", "VZ", "MMM", "MO", "CVX"]

def get_yahoo_finance_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        dividend_yield = stock.info.get('dividendYield')
        if dividend_yield is not None:
            return dividend_yield * 100  # 백분율로 변환
        else:
            return 0.0
    except Exception as e:
        st.error(f"{ticker}의 데이터를 가져오는 도중 오류가 발생했습니다: {e}")
        return 0.0

top_10_dividend_data = {"Ticker": [], "Dividend Yield (%)": [], "Recommendation Reason": []}

for ticker in sp500_tickers:
    yield_value = get_yahoo_finance_data(ticker)
    if yield_value > 0:
        top_10_dividend_data["Ticker"].append(ticker)
        top_10_dividend_data["Dividend Yield (%)"].append(yield_value)

        # 각 종목에 대한 추천 이유 설명 추가
        if yield_value > 4.0:
            reason = f"{ticker}은(는) 높은 배당 수익률({yield_value:.2f}%)을 자랑하며, 장기 투자 시 수익 창출 잠재력이 높습니다."
        elif 2.0 < yield_value <= 4.0:
            reason = f"{ticker}은(는) 안정적인 배당 수익률({yield_value:.2f}%)을 제공하며, 꾸준한 현금 흐름을 기대할 수 있습니다."
        else:
            reason = f"{ticker}은(는) 비교적 낮은 배당 수익률({yield_value:.2f}%)을 제공하지만, 성장 잠재력이 높은 기업입니다."

        top_10_dividend_data["Recommendation Reason"].append(reason)

# 상위 10개 기업 추출
top_10_dividends_df = pd.DataFrame(top_10_dividend_data).sort_values(by="Dividend Yield (%)", ascending=False).head(10)

# 데이터프레임 출력 및 그래프 생성
st.write("### 📊 배당 수익률 상위 10개 기업 데이터")
st.write(top_10_dividends_df)

# 배당 수익률 시각화
fig_top10 = px.bar(top_10_dividends_df, x='Ticker', y='Dividend Yield (%)', text='Dividend Yield (%)',
                   labels={'Ticker': '주식 종목 코드', 'Dividend Yield (%)': '배당 수익률 (%)'},
                   color='Dividend Yield (%)', title='Top 10 배당 수익률 기업')
fig_top10.update_traces(texttemplate='%{text:.2f}', textposition='outside')
st.plotly_chart(fig_top10)



# 재무제표와 뉴스 추가
# 뉴스 카드 형식으로 출력하는 HTML 스타일 정의
def render_news_card(title, publisher, link, image_url):
    return f"""
    <div style="display: flex; align-items: center; background-color: #f9f9f9; border-radius: 10px; padding: 15px; margin: 10px 0; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
        <div style="flex: 1;">
            <img src="{image_url}" style="width: 120px; height: 80px; border-radius: 5px; margin-right: 15px;" />
        </div>
        <div style="flex: 4;">
            <h3 style="margin: 0; color: #0073e6;">{title}</h3>
            <p style="margin: 5px 0; font-size: 14px; color: #333;">출처: {publisher}</p>
            <a href="{link}" target="_blank" style="text-decoration: none;">
                <button style="background-color: #0073e6; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer; font-size: 14px;">기사 읽기 🔗</button>
            </a>
        </div>
    </div>
    """

# 기본 이미지를 대체하여 뉴스 제목의 첫 글자를 이미지로 생성하는 함수
def generate_initial_image(text):
    img = Image.new('RGB', (120, 80), color=(200, 200, 200))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((40, 25), text[0], font=font, fill=(50, 50, 50))
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{img_str}"

# Streamlit 레이아웃 및 UI 요소 설정
st.subheader("비고 : 티커별 재무제표 및 최신 뉴스")
ticker = st.text_input("재무제표와 뉴스를 확인할 종목 티커를 입력하세요:", "AAPL").upper()

if ticker:
    try:
        # Yahoo Finance에서 주식 데이터 및 재무제표 가져오기
        stock = yf.Ticker(ticker)

        # 대차대조표 (Balance Sheet)
        st.write("### 대차대조표")
        balance_sheet = stock.balance_sheet
        st.dataframe(balance_sheet)

        # 손익계산서 (Income Statement)
        st.write("### 손익계산서")
        income_statement = stock.financials
        st.dataframe(income_statement)

        # 현금흐름표 (Cash Flow Statement)
        st.write("### 현금흐름표")
        cash_flow = stock.cashflow
        st.dataframe(cash_flow)

        # 최신 뉴스 (카드 형식)
        st.write("### 📢 최신 뉴스")
        news = stock.news

        # 뉴스 데이터가 없을 경우 예외 처리
        if not news:
            st.write(f"{ticker}의 최신 뉴스를 가져올 수 없습니다.")
        else:
            # 각 뉴스 항목에 대해 카드 형식으로 표시
            for article in news[:5]:
                title = article['title']
                publisher = article['publisher']
                link = article['link']
                
                # 이미지가 없는 경우 기본 이미지 생성
                try:
                    # 뉴스의 이미지가 있는 경우 가져오기
                    image_url = article.get("thumbnail", {}).get("resolutions", [{}])[0].get("url", None)
                    if not image_url:
                        image_url = generate_initial_image(title)  # 이미지가 없으면 첫 글자를 이미지로 대체
                except:
                    image_url = generate_initial_image(title)

                # 뉴스 카드 렌더링
                st.markdown(render_news_card(title, publisher, link, image_url), unsafe_allow_html=True)

    except Exception as e:
        st.write(f"재무제표 및 뉴스 데이터를 가져오는 중 오류가 발생했습니다: {e}")
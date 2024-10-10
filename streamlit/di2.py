import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# 웹페이지 제목
st.title("최적의 투자 분석을 통한 배당주 투자 예측 웹페이지")

# 1. 월 투자 금액 입력
st.subheader("월 투자 금액 입력")
investment_krw = st.number_input("한 달 투자 금액을 입력하세요 (만원 단위)", min_value=1, value=100) * 10000
st.write(f"매달 투자 금액: {investment_krw:,} 원")

# 2. 투자 기간 입력
st.subheader("투자 기간 입력")
investment_years = st.slider("투자 기간을 선택하세요 (년)", min_value=1, max_value=30, value=10)

# 3. 추천 종목 미국 주식 (티커 입력)
st.subheader("추천 종목 입력")
tickers_input = st.text_input("추천할 종목의 티커를 입력하세요 (예: AAPL, MSFT, KO)", "AAPL, MSFT, KO")
tickers = [ticker.strip() for ticker in tickers_input.split(',')]

# 주식 데이터를 가져오는 함수
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
with st.spinner('배당주 데이터를 불러오고 있습니다...'):
    stock_df = load_stock_data(tickers)

# 4. 미래 배당금 예측 (10년, 20년)
years = [10, 20]
for year in years:
    stock_df[f'{year}년 예상 배당금 (USD)'] = stock_df['Dividend Rate (USD)'] * investment_krw / stock_df['Price'] * year

# 4.1 배당금 예측 시각화
st.subheader("미래 배당금 예측")
fig = px.bar(stock_df, x='Company', y=[f'{years[0]}년 예상 배당금 (USD)', f'{years[1]}년 예상 배당금 (USD)'],
             title="10년 및 20년 예상 배당금",
             labels={'value': '배당금 (USD)', 'Company': '종목 이름'})
st.plotly_chart(fig)

# 5. 누적 배당금 및 다중 지표 분석
st.subheader("누적 배당금 분석")
fig2 = px.line(stock_df, x='Company', y=[f'{years[0]}년 예상 배당금 (USD)', f'{years[1]}년 예상 배당금 (USD)'],
              title="누적 배당금 분석",
              labels={'value': '배당금 (USD)', 'Company': '종목 이름'})
st.plotly_chart(fig2)

# 결과 요약
st.write(f"한 달 {investment_krw / 10000} 만원을 {investment_years}년 동안 투자할 경우, 상위 3개 배당주에서 "
         f"최대 수익을 낼 수 있는 종목은 다음과 같습니다. 10년과 20년 후 예상 배당금을 확인하세요!")

# 6. 배당 수익률 상위 10개 기업 추천
st.subheader("배당 수익률 상위 10개 기업 추천")
sp500_tickers = ["AAPL", "MSFT", "NVDA", "INTC", "KO", "PEP", "JNJ", "PG", "XOM", "IBM", "T", "VZ", "MMM", "MO", "CVX"]

@st.cache_data
def get_dividend_yield(tickers):
    data = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        dividend_yield = stock.info.get('dividendYield')
        if dividend_yield:
            data.append({'Ticker': ticker, 'Dividend Yield (%)': dividend_yield * 100})
    return pd.DataFrame(data).sort_values(by='Dividend Yield (%)', ascending=False).head(10)

top_10_dividends_df = get_dividend_yield(sp500_tickers)

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
st.subheader("티커별 재무제표 및 최신 뉴스")
ticker = st.text_input("재무제표와 뉴스를 확인할 종목 티커를 입력하세요:", "AAPL").upper()
if ticker:
    try:
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

        # 최신 뉴스
        st.write("### 최신 뉴스")
        news = stock.news
        for article in news[:5]:
            st.write(f"**{article['title']}**")
            st.write(f"출처: {article['publisher']}")
            st.write(f"[기사 읽기]({article['link']})")
            st.write("---")
    except Exception as e:
        st.write(f"재무제표 및 뉴스 데이터를 가져오는 중 오류가 발생했습니다: {e}")


# CSV 저장 버튼
if st.button("CSV로 저장"):
    # CSV 파일을 utf-8-sig 인코딩으로 저장하여 Excel에서 읽을 때 문제가 없도록 함
    csv_stock_df = stock_df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
    st.download_button(
        label="미래 배당금 예측 CSV 다운로드",
        data=csv_stock_df,
        file_name='future_dividend_estimate.csv',
        mime='text/csv',
    )



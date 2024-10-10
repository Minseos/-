import streamlit as st  # Streamlit을 사용한 웹 대시보드를 만들기 위한 라이브러리
import pandas as pd  # 데이터 처리용 라이브러리
import os  # 파일 경로 탐색을 위한 라이브러리
import glob  # 여러 파일을 쉽게 불러오기 위한 라이브러리

# Model 클래스 임포트 시도
try:
    from model import Model
except ImportError as e:
    st.write(f"Model import error: {e}")

# 제목을 표시
st.write("# 📈 Nasdaq Stock Market Dashboard")

# 최신 데이터 날짜를 불러와 표시
data_folder = "./data"
csv_files = glob.glob(f"{data_folder}/*.csv")

if csv_files:
    latest_day = "-".join(os.path.basename(csv_files[0]).split("_")[1:]).split(".")[0]
else:
    latest_day = "unknown"

st.write(f"""
- **Period: first_day - {latest_day}**
""")

# 구분선
st.write("---")

# 데이터 로드를 위한 메시지 출력
st.write(f"### Data load")

# 여러 개의 CSV 파일을 읽어와서 병합
if csv_files:
    try:
        # 모든 CSV 파일 읽어서 하나의 DataFrame으로 병합
        data_list = [pd.read_csv(file) for file in csv_files]
        data = pd.concat(data_list, ignore_index=True)

        # ticker 컬럼을 대문자로 변환하여 통일
        if 'ticker' in data.columns:
            data['ticker'] = data['ticker'].str.upper()
        else:
            data['ticker'] = os.path.basename(csv_files[0]).split("_")[0].upper()  # 파일명에서 티커를 추출하여 대문자로 설정

        # 데이터 출력(디버그용)
        st.write("Data loaded successfully.")
        st.dataframe(data.head())  # 데이터 확인을 위해 상위 5개 행 출력
    except Exception as e:
        st.write(f"Error loading CSV files: {e}")
        data = pd.DataFrame()  # 빈 데이터프레임으로 초기화
else:
    st.write("No CSV files found in the './data' directory.")
    data = pd.DataFrame()  # 빈 데이터프레임으로 초기화

# 사용자로부터 ticker를 입력받음 (기본값은 'NVDA')
st.session_state["ticker"] = st.text_input("ticker input", "NVDA").upper()

# 사용자가 ticker를 입력한 경우 실행
if st.session_state["ticker"] and not data.empty:
    # 사용자가 입력한 ticker에 해당하는 데이터 필터링
    chart_data = data.loc[data['ticker'] == st.session_state["ticker"]]

    # 필터링된 데이터 출력 (디버그용)
    st.write("Filtered Data:")
    st.dataframe(chart_data)

    if chart_data.empty:
        st.write("No data available for the selected ticker.")
    else:
        # 구분선
        st.write("---")

        # 지표 (Indicator) 섹션 표시
        st.write("### Indicator")

        # 사용될 보조 지표들 정의
        indi_cols = ["SMA_20", "SMA_200", "RSI_14", "MACD", "MACD_signal"]

        # 지표 컬럼이 데이터에 모두 존재하는지 확인
        missing_cols = [col for col in indi_cols if col not in chart_data.columns]
        if missing_cols:
            st.write(f"Missing columns in data: {missing_cols}")
        else:
            # 5개의 열로 지표를 표시할 공간 생성
            cols = st.columns(5)

            # 마지막 2개의 row에서 각 지표의 현재 값과 전 값의 차이를 계산
            if len(chart_data) < 2:
                st.write("Not enough data to calculate indicators.")
            else:
                last_two_rows = chart_data.tail(2)

                for i, col in enumerate(indi_cols):
                    with cols[i]:
                        # 지표 이름과 현재 값, 변화량을 계산 및 표시
                        name = col
                        current_value = round(last_two_rows.iloc[-1][col], 4)  # 현재 값
                        previous_value = round(last_two_rows.iloc[-2][col], 4)  # 이전 값
                        change_value = round(current_value - previous_value, 4)  # 변화량
                        cols[i].metric(
                            label=name,
                            value=current_value,
                            delta=change_value
                        )

        # 구분선
        st.write("---")

        # 차트 (Chart) 섹션 표시
        st.write("### Chart")

        # 차트 시각화를 위한 필터링 (최근 126일 데이터)
        chart_columns = ["High", "Low", "SMA_20", "SMA_100"]
        missing_chart_cols = [col for col in chart_columns if col not in chart_data.columns]
        if missing_chart_cols:
            st.write(f"Missing columns for charting: {missing_chart_cols}")
        elif len(chart_data) < 126:
            st.write("차트를 그리기 위한 데이터가 충분하지 않습니다. 최소 126일 이상의 데이터가 필요합니다.")
        else:
            st.line_chart(chart_data[chart_columns].iloc[-126:])

        # 구분선
        st.write("---")

        # 인사이트 (Insight) 섹션 표시
        st.write("### Insight")

        # 모델을 사용하여 인사이트를 도출 (지표 분석)
        with st.spinner("Thinking... plz wait"):
            try:
                if 'Model' in globals():
                    insight = Model(chart_data).get_insight()  # 모델을 사용하여 인사이트 도출
                    st.write(insight)  # 인사이트 출력
                else:
                    st.write("Model is not defined. Please check the model import.")
            except Exception as e:
                st.write(f"Error generating insight: {e}")

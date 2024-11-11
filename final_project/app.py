
import streamlit as st
import pandas as pd
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from konlpy.tag import Mecab

# 기본 설정
st.title("리뷰 데이터 분석")
st.write("이 애플리케이션은 리뷰 데이터를 분석하여 단어 빈도와 주제를 시각화합니다.")

# 데이터 업로드
uploaded_file = st.file_uploader("CSV 파일 업로드", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # 리뷰 데이터 전처리
    st.subheader("데이터 전처리")
    st.write("불용어 제거 및 형태소 분석을 통해 명사만 추출합니다.")
    
    # Mecab 설정 및 명사 추출 함수
    mecab = Mecab()
    def extract_nouns(text):
        if isinstance(text, str):
            return ' '.join(mecab.nouns(text))
        return text
    
    # 리뷰 데이터 전처리 적용
    df['Nouns_Review'] = df['Review'].apply(extract_nouns)
    st.write("전처리된 데이터:")
    st.dataframe(df[['Review', 'Nouns_Review']].head())

    # 단어 빈도 분석
    st.subheader("단어 빈도 분석")
    all_nouns = ' '.join(df['Nouns_Review'].dropna()).split()
    word_counts = Counter(all_nouns)
    top_20_words = word_counts.most_common(20)
    st.write("상위 20개의 자주 언급된 단어:")
    st.write(top_20_words)

    # 워드 클라우드 생성
    st.subheader("워드 클라우드")
    text_for_wordcloud = ' '.join(df['Nouns_Review'].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color='white', font_path='/usr/share/fonts/truetype/nanum/NanumGothic.ttf').generate(text_for_wordcloud)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

    # LDA 주제 모델링
    st.subheader("주제 모델링 (LDA)")
    vectorizer = CountVectorizer(max_df=0.9, min_df=2)
    X = vectorizer.fit_transform(df['Nouns_Review'].dropna())

    lda_model = LatentDirichletAllocation(n_components=5, random_state=42)
    lda_model.fit(X)

    feature_names = vectorizer.get_feature_names_out()
    num_top_words = 10

    topics = []
    for topic_idx, topic in enumerate(lda_model.components_):
        top_words = [feature_names[i] for i in topic.argsort()[:-num_top_words - 1:-1]]
        topics.append((f"Topic {topic_idx + 1}", top_words))
    
    for topic_name, words in topics:
        st.write(f"{topic_name}: {', '.join(words)}")

    # 토픽별 막대 그래프
    st.subheader("토픽별 주요 단어 빈도 막대 그래프")
    for topic_idx, topic in enumerate(lda_model.components_):
        top_words = [feature_names[i] for i in topic.argsort()[:-num_top_words - 1:-1]]
        top_word_counts = topic[topic.argsort()[:-num_top_words - 1:-1]]

        plt.figure(figsize=(10, 5))
        plt.barh(top_words, top_word_counts)
        plt.gca().invert_yaxis()
        plt.title(f"Topic {topic_idx + 1}")
        plt.xlabel("Word Frequency")
        st.pyplot(plt)


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# 1. 한글 폰트 설정
@st.cache_resource
def setup_font():
    font_path = "NanumGothic.ttf"
    if os.path.exists(font_path):
        font_prop = fm.FontProperties(fname=font_path)
        plt.rc('font', family=font_prop.get_name())
        plt.rcParams['axes.unicode_minus'] = False
        return font_prop
    return None

font_prop = setup_font()

# 2. 데이터 불러오기
@st.cache_data
def load_data():
    file_path = "K-stat 무역통계 - 한국무역협회.csv"
    df = pd.read_csv(file_path, encoding="cp949")

    # 연도 정리 ("2025년" → 2025)
    df["년"] = df["년"].str.replace("년", "").astype(int)

    # 숫자 컬럼 쉼표 제거 후 숫자형 변환
    num_cols = [
        "수출금액", "수출중량", "수입금액", "수입중량", "수지"
    ]
    for col in num_cols:
        df[col] = df[col].str.replace(",", "").astype(float)

    return df

df = load_data()

# -------------------------------
# 3. 페이지 기본 설정
# -------------------------------
st.set_page_config(
    page_title="Italy–Korea Trade Dashboard",
    page_icon="🇮🇹",
    layout="wide"
)

# -------------------------------
# 4. 커스텀 CSS (이탈리아 테마)
# -------------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 40px;
        font-weight: 800;
        color: #FFFFFF;
    }
    .sub-title {
        font-size: 20px;
        color: #F1F1F1;
        margin-bottom: 30px;
    }
    .metric-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #F8F9FA;
        border-left: 6px solid #008C45;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <div class="main-title">
        💱
        <span style="color:#006400;">이탈</span>
        <span style="color:#800000;">리아</span>
        –
        <span style="color:#000080;">한</span>
        <span style="color:#800000;">국</span>
        무역통계 대시보드
        📊
    </div>
    """,
    unsafe_allow_html=True
)


# -------------------------------
# 5. 메인 타이틀
# -------------------------------
st.markdown(
    '<div class="sub-title">K-stat 기반 연도별 수출입·무역수지 추이 분석</div>',
    unsafe_allow_html=True
)


# 사이드바
st.sidebar.header("필터 설정")

if st.sidebar.checkbox("데이터 원본 보기"):
    st.subheader("Raw Data")
    st.dataframe(df)

# 분석 대상 선택
st.subheader("📈 연도별 무역 지표 추이")

metric = st.selectbox(
    "분석할 지표를 선택하세요",
    ["수출금액", "수입금액", "수지", "수출중량", "수입중량"]
)

# -------------------------------
# 8. 시각화 (증가/감소 색상 분기)
# -------------------------------
fig, ax = plt.subplots(figsize=(10, 5))

# 배경색 설정 (이탈리아 레드)


years = df["년"].values
values = df[metric].values

for i in range(len(values) - 1):
    if values[i + 1] >= values[i]:
        color = "#CD212A"  # 감소 → Red 
    else:
        color = "#008C45"  # 증가 → Green

    ax.plot(
        years[i:i+2],
        values[i:i+2],
        color=color,
        linewidth=3,
        marker="o"
    )

ax.set_title(
    f"연도별 {metric} 추이 (Korea–Italy)",
    fontproperties=font_prop,
    fontsize=16,
    color="black",
    pad=15
)

ax.set_xlabel("연도", fontproperties=font_prop)
ax.set_ylabel(metric, fontproperties=font_prop)

ax.grid(True, linestyle="--", alpha=0.4)

st.pyplot(fig)
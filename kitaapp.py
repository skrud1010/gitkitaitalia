import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# 1. Font setup (Handles Korean breakages in matplotlib)
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

# 2. Load Data
@st.cache_data
def load_data():
    file_path = "K-stat 무역통계 - 한국무역협회.csv"
    df = pd.read_csv(file_path, encoding="cp949")

    # Clean Year ("2025년" → 2025)
    df["년"] = df["년"].str.replace("년", "").astype(int)

    # Remove commas and convert to float
    num_cols = [
        "수출금액", "수출중량", "수입금액", "수입중량", "수지"
    ]
    for col in num_cols:
        df[col] = df[col].astype(str).str.replace(",", "").astype(float)
        
    # Translate columns to English
    df.rename(columns={
        "년": "Year",
        "수출금액": "Export Value",
        "수입금액": "Import Value",
        "수지": "Trade Balance",
        "수출중량": "Export Weight",
        "수입중량": "Import Weight"
    }, inplace=True)

    return df

df = load_data()

# -------------------------------
# 3. Page Config
# -------------------------------
st.set_page_config(
    page_title="Italy–Korea Trade Dashboard",
    page_icon="🇮🇹",
    layout="wide"
)

# -------------------------------
# 4. Custom CSS (Adaptive Theme Colors)
# -------------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 40px;
        font-weight: 800;
        color: var(--text-color); /* Automatically adapts to Light/Dark Mode */
    }
    .sub-title {
        font-size: 20px;
        color: var(--text-color); /* Automatically adapts to Light/Dark Mode */
        opacity: 0.85;
        margin-bottom: 30px;
    }
    .metric-box {
        padding: 15px;
        border-radius: 10px;
        background-color: var(--background-color);
        border-left: 6px solid #008C45;
        color: var(--text-color);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Italy/Korea 국가명 색상도 양쪽 모드에서 모두 잘 보이는 톤으로 미세 조정
st.markdown(
    """
    <div class="main-title">
        <span style="color:#009246;">Italy</span>
        –
        <span style="color:#0A549E;">Korea</span>
        Trade Statistics Dashboard
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# 5. Main Title & Subtitle
# -------------------------------
st.markdown(
    '<div class="sub-title">K-stat Based Annual Export/Import & Trade Balance Trend Analysis</div>',
    unsafe_allow_html=True
)

# Sidebar
st.sidebar.header("Filter Settings")

if st.sidebar.checkbox("View Raw Data"):
    st.subheader("Raw Data")
    st.dataframe(df)

# Analysis Target Selection
st.subheader("Annual Trade Indicator Trends")

metric = st.selectbox(
    "Select an indicator to analyze",
    ["Export Value", "Import Value", "Trade Balance", "Export Weight", "Import Weight"]
)

# -------------------------------
# 6. Visualization 
# -------------------------------
# 기존 크기 (11.5, 5)에서 40% 줄인 비율 (6.9, 3)로 수정
fig, ax = plt.subplots(figsize=(6.9, 3))

years = df["Year"].values
values = df[metric].values

for i in range(len(values) - 1):
    if values[i + 1] >= values[i]:
        color = "#CD212A"  # Increase
    else:
        color = "#008C45"  # Decrease

    ax.plot(
        years[i:i+2],
        values[i:i+2],
        color=color,
        linewidth=3.5,
        marker="o",
        markersize=6
    )

# 라이트/다크 모드 자동 글자색 대응
ax.set_title(
    f"Annual {metric} Trend (Korea–Italy)",
    fontproperties=font_prop if font_prop else None,
    fontsize=15,
    pad=15
)

ax.set_xlabel("Year", fontproperties=font_prop if font_prop else None, fontsize=11)
ax.set_ylabel(metric, fontproperties=font_prop if font_prop else None, fontsize=11)

ax.grid(True, linestyle="--", alpha=0.3)

# 화면을 1:3:1 비율로 3개의 칸으로 나눕니다. (좌측여백, 중앙그래프, 우측여백)
col1, col2, col3 = st.columns([1, 3, 1])

# 가운데 칸(col2)에만 그래프를 그려서 가운데 정렬 효과를 냅니다.
with col2:
    st.pyplot(fig, use_container_width=False)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# 1. Font setup
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
# 4. Custom CSS 
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
        color: #FFFFFF;
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
        <span style="color:#006400;">Italy</span>
        –
        <span style="color:#000080;">Korea</span>
        Trade Statistics Dashboard
        📊
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# 5. Main Title
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
st.subheader("📈 Annual Trade Indicator Trends")

metric = st.selectbox(
    "Select an indicator to analyze",
    ["Export Value", "Import Value", "Trade Balance", "Export Weight", "Import Weight"]
)

# -------------------------------
# 8. Visualization 
# -------------------------------
# 그래프 크기 50% 축소 (기존 10, 5 -> 5, 2.5)
fig, ax = plt.subplots(figsize=(5, 2.5))

years = df["Year"].values
values = df[metric].values

for i in range(len(values) - 1):
    if values[i + 1] >= values[i]:
        color = "#CD212A"  
    else:
        color = "#008C45"  

    ax.plot(
        years[i:i+2],
        values[i:i+2],
        color=color,
        linewidth=3,
        marker="o"
    )

# 그래프 텍스트 및 축 색상 변경 (다크 모드 호환)
ax.set_title(
    f"Annual {metric} Trend (Korea–Italy)",
    fontproperties=font_prop if font_prop else None,
    fontsize=12,
    color="white",
    pad=15
)

ax.set_xlabel("Year", fontproperties=font_prop if font_prop else None, color="white")
ax.set_ylabel(metric, fontproperties=font_prop if font_prop else None, color="white")

ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

# 그래프 배경 투명화
fig.patch.set_alpha(0.0)
ax.patch.set_alpha(0.0)

ax.grid(True, linestyle="--", alpha=0.4, color="gray")

# 화면 가운데 정렬을 위한 컬럼 분할
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.pyplot(fig)

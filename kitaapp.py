import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform
import matplotlib.font_manager as fm
import os

# =============================
# 1. 한글 폰트 설정 (기존과 동일)
# =============================
def set_korean_font():
    font_file = "NanumGothic.ttf"
    if os.path.exists(font_file):
        font_prop = fm.FontProperties(fname=font_file)
        plt.rc('font', family=font_prop.get_name())
    else:
        if platform.system() == 'Darwin':
            plt.rc('font', family='AppleGothic')
        elif platform.system() == 'Windows':
            plt.rc('font', family='Malgun Gothic')
    plt.rcParams['axes.unicode_minus'] = False

set_korean_font()

# 앱 설정
st.set_page_config(page_title="한-이탈리아 무역 분석", layout="wide")
st.title("🇮🇹 한-이탈리아 수출입 무역 통계 분석기 🇰🇷")

# =============================
# 2. 데이터 로드 및 전처리
# =============================
file_path = "K-stat 무역통계 - 한국무역협회.xls - sheet1.csv"

@st.cache_data
def load_trade_data(path):
    try:
        # 데이터 특성에 따라 skiprows 조정 (상단 제목 행 제외)
        # 콤마(thousands) 처리 및 인코딩 자동 시도
        df = pd.read_csv(path, encoding='utf-8-sig', thousands=',', skiprows=3)
        
        # 컬럼명 정리 (공백 제거)
        df.columns = df.columns.str.strip()
        
        # '기간'이나 '연도' 컬럼이 있다면 숫자형으로 변환
        if '기간' in df.columns:
            df['기간'] = df['기간'].astype(str)
            
        return df
    except Exception as e:
        st.error(f"데이터 로드 중 오류 발생: {e}")
        return None

df = load_trade_data(file_path)

if df is not None:
    # 데이터 요약 정보
    st.sidebar.header("📊 데이터 필터")
    
    # 분석할 지표 선택 (수출액, 수입액, 무역수지 등)
    target_cols = [col for col in df.columns if '액' in col or '지' in col or '률' in col]
    
    # 메인 대시보드
    tab1, tab2 = st.tabs(["📈 시각화 분석", "📄 원본 데이터"])

    with tab1:
        st.subheader("연도별 무역 추이")
        
        if '기간' in df.columns and len(target_cols) > 0:
            selected_metric = st.selectbox("분석할 지표를 선택하세요:", target_cols)
            
            # 추세선 그래프
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.lineplot(data=df, x='기간', y=selected_metric, marker='o', color='#008C45', ax=ax)
            sns.barplot(data=df, x='기간', y=selected_metric, alpha=0.3, color='#CD212A', ax=ax)
            
            plt.title(f"연도별 {selected_metric} 변화", fontsize=18)
            plt.xticks(rotation=45)
            plt.grid(True, linestyle='--', alpha=0.6)
            
            st.pyplot(fig)
            
            # 지표 설명 (무역수지 계산 등)
            col1, col2, col3 = st.columns(3)
            latest = df.iloc[-1]
            col1.metric("최근 수출액", f"{latest.get('수출액', 0):,}")
            col2.metric("최근 수입액", f"{latest.get('수입액', 0):,}")
            col3.metric("최근 무역수지", f"{latest.get('무역수지', 0):,}")
        else:
            st.warning("데이터 형식이 분석에 적합하지 않습니다. 컬럼명을 확인해 주세요.")

    with tab2:
        st.subheader("데이터 상세 보기")
        st.dataframe(df, use_container_width=True)
        
        # CSV 다운로드 버튼
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="데이터 다운로드 (CSV)",
            data=csv,
            file_name='italy_korea_trade.csv',
            mime='text/csv',
        )

else:
    st.info("파일을 찾을 수 없습니다. 경로를 확인하거나 파일을 업로드해 주세요.")
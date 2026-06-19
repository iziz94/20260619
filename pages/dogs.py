import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="서울의 가장 이상했던 날들",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울의 가장 이상했던 날들")
st.caption("1907 ~ 2026 서울 기온 데이터 분석")

# -----------------------------
# 데이터 로드
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("ta_20260619190504.csv")

    # 컬럼 강제 정리
    df.columns = ["date", "station", "avg_temp", "min_temp", "max_temp"]

    # 날짜 변환
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # 숫자 변환 (중요: 문자열 에러 방지)
    df["avg_temp"] = pd.to_numeric(df["avg_temp"], errors="coerce")
    df["min_temp"] = pd.to_numeric(df["min_temp"], errors="coerce")
    df["max_temp"] = pd.to_numeric(df["max_temp"], errors="coerce")

    # 파생 변수
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["temp_range"] = df["max_temp"] - df["min_temp"]

    # 결측 제거
    df = df.dropna()

    return df


df = load_data()

# -----------------------------
# 기록 찾기
# -----------------------------
hottest_day = df.loc[df["max_temp"].idxmax()]
coldest_day = df.loc[df["min_temp"].idxmin()]
largest_gap = df.loc[df["temp_range"].idxmax()]

st.header("🏆 서울 기온 역사 기록")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🔥 역대 최고기온", f"{hottest_day['max_temp']:.1f}°C")
    st.write(hottest_day["date"].date())

with col2:
    st.metric("🥶 역대 최저기온", f"{coldest_day['min_temp']:.1f}°C")
    st.write(coldest_day["date"].date())

with col3:
    st.metric("🌤 최대 일교차", f"{largest_gap['temp_range']:.1f}°C")
    st.write(largest_gap["date"].date())

# -----------------------------
# 연평균 분석
# -----------------------------
st.header("📈 연평균 기온 변화")

annual = df.groupby("year", as_index=False)["avg_temp"].mean()

fig = px.line(
    annual,
    x="year",
    y="avg_temp",
    markers=True,
    title="서울 연평균 기온 변화"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# 가장 이상한 해 (Z-score)
# -----------------------------
st.header("🚨 가장 이상했던 해")

mean_temp = annual["avg_temp"].mean()
std_temp = annual["avg_temp"].std()

annual["zscore"] = (annual["avg_temp"] - mean_temp) / std_temp

warm_outlier = annual.loc[annual["zscore"].idxmax()]
cold_outlier = annual.loc[annual["zscore"].idxmin()]

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔥 가장 따뜻했던 해")
    st.metric(str(int(warm_outlier["year"])), f"{warm_outlier['avg_temp']:.2f}°C")

with col2:
    st.subheader("🥶 가장 추웠던 해")
    st.metric(str(int(cold_outlier["year"])), f"{cold_outlier['avg_temp']:.2f}°C")

# -----------------------------
# 월별 극값
# -----------------------------
st.header("📅 월별 극단 기록")

monthly_hot = df.loc[df.groupby("month")["max_temp"].idxmax()].sort_values("month")
monthly_cold = df.loc[df.groupby("month")["min_temp"].idxmin()].sort_values("month")

st.subheader("🔥 월별 최고기온 기록")
st.dataframe(monthly_hot[["month", "date", "max_temp"]], use_container_width=True)

st.subheader("❄️ 월별 최저기온 기록")
st.dataframe(monthly_cold[["month", "date", "min_temp"]], use_container_width=True)

# -----------------------------
# 날짜 탐험
# -----------------------------
st.header("🔍 특정 날짜 탐험")

selected_date = st.date_input("날짜 선택")

month = selected_date.month
day = selected_date.day

same_day = df[(df["month"] == month) & (df["day"] == day)]

if not same_day.empty:

    hottest = same_day.loc[same_day["max_temp"].idxmax()]
    coldest = same_day.loc[same_day["min_temp"].idxmin()]

    col1, col2 = st.columns(2)

    with col1:
        st.success(
            f"🔥 가장 더운 {month}/{day}\n"
            f"{hottest['date'].date()} / {hottest['max_temp']:.1f}°C"
        )

    with col2:
        st.info(
            f"🥶 가장 추운 {month}/{day}\n"
            f"{coldest['date'].date()} / {coldest['min_temp']:.1f}°C"
        )

    fig2 = px.line(
        same_day.sort_values("year"),
        x="year",
        y="avg_temp",
        title=f"{month}/{day} 기온 변화"
    )

    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# 데이터 개요
# -----------------------------
st.header("📊 데이터 개요")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("총 데이터 수", f"{len(df):,}")

with col2:
    st.metric("시작 연도", int(df["year"].min()))

with col3:
    st.metric("종료 연도", int(df["year"].max()))

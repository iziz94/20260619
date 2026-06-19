import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Global Top10 Stocks Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("🌍 Global Market Cap Top10 Dashboard")

# --------------------------------
# 기업 정보
# --------------------------------

COMPANIES = {
    "NVIDIA": "NVDA",
    "Microsoft": "MSFT",
    "Apple": "AAPL",
    "Alphabet": "GOOGL",
    "Amazon": "AMZN",
    "Meta": "META",
    "Broadcom": "AVGO",
    "TSMC": "TSM",
    "Tesla": "TSLA",
    "Saudi Aramco": "2222.SR",
}

# --------------------------------
# Sidebar
# --------------------------------

st.sidebar.header("⚙️ Settings")

period = st.sidebar.selectbox(
    "기간 선택",
    ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
    index=3
)

show_ai_only = st.sidebar.checkbox(
    "AI 관련 기업만 보기",
    value=False
)

AI_COMPANIES = [
    "NVIDIA",
    "Microsoft",
    "Alphabet",
    "Amazon",
    "Meta",
    "Broadcom",
    "TSMC"
]

# --------------------------------
# 데이터 로딩
# --------------------------------

@st.cache_data(ttl=3600)
def load_price_data(period):

    tickers = list(COMPANIES.values())

    df = yf.download(
        tickers,
        period=period,
        auto_adjust=True,
        progress=False
    )["Close"]

    return df


@st.cache_data(ttl=3600)
def get_market_caps():

    data = []

    for company, ticker in COMPANIES.items():

        try:
            info = yf.Ticker(ticker).info

            market_cap = info.get("marketCap", np.nan)

            data.append(
                [company, ticker, market_cap]
            )

        except:
            pass

    return pd.DataFrame(
        data,
        columns=["Company", "Ticker", "MarketCap"]
    )


prices = load_price_data(period)

if show_ai_only:

    ai_tickers = [
        COMPANIES[c]
        for c in AI_COMPANIES
    ]

    prices = prices[ai_tickers]

# --------------------------------
# 수익률 계산
# --------------------------------

normalized = (
    prices
    .div(prices.iloc[0])
    .mul(100)
)

returns = (
    prices.iloc[-1]
    / prices.iloc[0]
    - 1
) * 100

returns = returns.sort_values(
    ascending=False
)

# --------------------------------
# 상단 KPI
# --------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "종목 수",
    len(prices.columns)
)

col2.metric(
    "최고 수익률",
    f"{returns.max():.1f}%"
)

col3.metric(
    "평균 수익률",
    f"{returns.mean():.1f}%"
)

st.divider()

# --------------------------------
# 1. 성과 비교
# --------------------------------

st.subheader("📈 Normalized Performance")

fig = px.line(
    normalized,
    x=normalized.index,
    y=normalized.columns,
)

fig.update_layout(
    height=600,
    hovermode="x unified",
    template="plotly_white",
    yaxis_title="Base 100"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------
# 2. 수익률 랭킹
# --------------------------------

left, right = st.columns([1, 2])

with left:

    st.subheader("🏆 Return Ranking")

    ranking_df = pd.DataFrame({
        "Ticker": returns.index,
        "Return (%)": returns.values.round(2)
    })

    st.dataframe(
        ranking_df,
        use_container_width=True
    )

with right:

    fig_bar = px.bar(
        ranking_df,
        x="Return (%)",
        y="Ticker",
        orientation="h",
        color="Return (%)",
    )

    fig_bar.update_layout(
        height=500,
        template="plotly_white"
    )

    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )

# --------------------------------
# 3. 시가총액 Treemap
# --------------------------------

st.subheader("🌎 Market Cap Treemap")

market_caps = get_market_caps()

fig_tree = px.treemap(
    market_caps,
    path=["Company"],
    values="MarketCap",
    color="MarketCap",
)

fig_tree.update_layout(
    height=700
)

st.plotly_chart(
    fig_tree,
    use_container_width=True
)

# --------------------------------
# 4. 상관관계 분석
# --------------------------------

st.subheader("🔗 Correlation Heatmap")

daily_returns = prices.pct_change().dropna()

corr = daily_returns.corr()

heatmap = go.Figure(
    data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale="RdBu",
        zmin=-1,
        zmax=1,
        text=np.round(corr.values, 2),
        texttemplate="%{text}"
    )
)

heatmap.update_layout(
    height=700
)

st.plotly_chart(
    heatmap,
    use_container_width=True
)

# --------------------------------
# 5. 리스크 분석
# --------------------------------

st.subheader("⚠️ Risk Metrics")

annual_volatility = (
    daily_returns.std()
    * np.sqrt(252)
    * 100
)

rolling_max = prices.cummax()

drawdown = (
    prices / rolling_max
    - 1
)

mdd = (
    drawdown.min()
    * 100
)

risk_df = pd.DataFrame({
    "Volatility (%)":
        annual_volatility.round(2),
    "Max Drawdown (%)":
        mdd.round(2),
    "Return (%)":
        returns.round(2)
})

risk_df = risk_df.sort_values(
    "Return (%)",
    ascending=False
)

st.dataframe(
    risk_df,
    use_container_width=True
)

# --------------------------------
# 다운로드
# --------------------------------

csv = risk_df.to_csv().encode("utf-8")

st.download_button(
    "📥 결과 다운로드",
    csv,
    "global_top10_analysis.csv",
    "text/csv"
)

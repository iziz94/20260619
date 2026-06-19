import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Global Market Cap Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("🌍 Global Market Cap Top10 Dashboard")
st.caption("Weekly Performance / Market Cap / Risk Analytics")

# =====================================================
# CONFIG
# =====================================================

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

BENCHMARKS = {
    "S&P500": "^GSPC",
    "NASDAQ100": "^NDX",
}

AI_COMPANIES = [
    "NVIDIA",
    "Microsoft",
    "Alphabet",
    "Amazon",
    "Meta",
    "Broadcom",
    "TSMC",
]

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("⚙️ Settings")

period = st.sidebar.selectbox(
    "기간 선택",
    ["6mo", "1y", "2y", "5y"],
    index=1
)

show_ai_only = st.sidebar.checkbox(
    "AI 관련 기업만 보기",
    value=False
)

# =====================================================
# DATA
# =====================================================

@st.cache_data(ttl=3600)
def load_prices(period):

    tickers = list(COMPANIES.values())
    tickers.extend(BENCHMARKS.values())

    prices = yf.download(
        tickers,
        period=period,
        auto_adjust=True,
        progress=False
    )["Close"]

    # 휴장일 보정
    prices = prices.ffill().bfill()

    # 주봉 변환
    prices = (
        prices
        .resample("W-FRI")
        .last()
    )

    return prices


@st.cache_data(ttl=3600)
def get_market_caps():

    data = []

    for company, ticker in COMPANIES.items():

        try:
            info = yf.Ticker(ticker).info

            data.append({
                "Company": company,
                "Ticker": ticker,
                "MarketCap": info.get("marketCap", np.nan)
            })

        except:
            pass

    return pd.DataFrame(data)


prices = load_prices(period)

# =====================================================
# FILTER
# =====================================================

stock_tickers = list(COMPANIES.values())

if show_ai_only:

    stock_tickers = [
        COMPANIES[x]
        for x in AI_COMPANIES
    ]

display_cols = stock_tickers + list(BENCHMARKS.values())

prices_display = prices[display_cols]

# =====================================================
# NORMALIZED PERFORMANCE
# =====================================================

normalized = (
    prices_display
    .div(prices_display.iloc[0])
    * 100
)

returns = (
    prices_display.iloc[-1]
    / prices_display.iloc[0]
    - 1
) * 100

returns = returns.sort_values(
    ascending=False
)

# =====================================================
# KPI
# =====================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Assets",
    len(display_cols)
)

c2.metric(
    "Best Return",
    f"{returns.max():.1f}%"
)

c3.metric(
    "Average Return",
    f"{returns.mean():.1f}%"
)

c4.metric(
    "Worst Return",
    f"{returns.min():.1f}%"
)

st.divider()

# =====================================================
# PERFORMANCE CHART
# =====================================================

st.subheader("📈 Weekly Normalized Performance")

fig = go.Figure()

for col in normalized.columns:

    fig.add_trace(
        go.Scatter(
            x=normalized.index,
            y=normalized[col],
            mode="lines",
            name=col,
            connectgaps=True
        )
    )

fig.update_layout(
    height=650,
    template="plotly_white",
    hovermode="x unified",
    yaxis_title="Base = 100",
    legend=dict(
        orientation="h",
        y=1.02,
        x=1,
        xanchor="right"
    )
)

fig.update_traces(
    line=dict(width=3)
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# RETURN RANKING
# =====================================================

st.subheader("🏆 Performance Ranking")

ranking_df = pd.DataFrame({
    "Ticker": returns.index,
    "Return (%)": returns.values.round(2)
})

left, right = st.columns([1, 2])

with left:

    st.dataframe(
        ranking_df,
        use_container_width=True
    )

with right:

    fig_rank = px.bar(
        ranking_df,
        x="Return (%)",
        y="Ticker",
        orientation="h",
        color="Return (%)"
    )

    fig_rank.update_layout(
        height=500,
        template="plotly_white"
    )

    st.plotly_chart(
        fig_rank,
        use_container_width=True
    )

# =====================================================
# MARKET CAP TREEMAP
# =====================================================

st.subheader("🌎 Market Capitalization")

market_caps = get_market_caps()

fig_tree = px.treemap(
    market_caps,
    path=["Company"],
    values="MarketCap",
    color="MarketCap"
)

fig_tree.update_layout(
    height=700
)

st.plotly_chart(
    fig_tree,
    use_container_width=True
)

# =====================================================
# CORRELATION
# =====================================================

st.subheader("🔗 Correlation Matrix")

daily_returns = prices_display.pct_change().dropna()

corr = daily_returns.corr()

heatmap = go.Figure(
    data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        text=np.round(corr.values, 2),
        texttemplate="%{text}",
        colorscale="RdBu",
        zmin=-1,
        zmax=1
    )
)

heatmap.update_layout(
    height=700
)

st.plotly_chart(
    heatmap,
    use_container_width=True
)

# =====================================================
# RISK ANALYSIS
# =====================================================

st.subheader("⚠️ Risk Metrics")

volatility = (
    daily_returns.std()
    * np.sqrt(52)
    * 100
)

rolling_max = prices_display.cummax()

drawdown = (
    prices_display / rolling_max
    - 1
)

mdd = drawdown.min() * 100

risk_df = pd.DataFrame({
    "Return (%)": returns.round(2),
    "Volatility (%)": volatility.round(2),
    "Max Drawdown (%)": mdd.round(2)
})

risk_df = risk_df.sort_values(
    "Return (%)",
    ascending=False
)

st.dataframe(
    risk_df,
    use_container_width=True
)

# =====================================================
# DOWNLOAD
# =====================================================

csv = risk_df.to_csv().encode("utf-8")

st.download_button(
    "📥 Download CSV",
    data=csv,
    file_name="global_top10_dashboard.csv",
    mime="text/csv"
)

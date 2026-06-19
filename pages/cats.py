import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

st.set_page_config(
    page_title="Global Market Cap Top 10 Dashboard",
    layout="wide"
)

st.title("🌍 Global Market Cap Top 10 Stocks")
st.caption("최근 1년 수익률 비교")

# Top10 시총 기업
stocks = {
    "NVIDIA": "NVDA",
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Alphabet": "GOOGL",
    "Amazon": "AMZN",
    "Broadcom": "AVGO",
    "TSMC": "TSM",
    "Saudi Aramco": "2222.SR",
    "Tesla": "TSLA",
    "Meta": "META"
}

@st.cache_data(ttl=3600)
def load_data():
    tickers = list(stocks.values())

    df = yf.download(
        tickers,
        period="1y",
        auto_adjust=True,
        progress=False
    )["Close"]

    return df

prices = load_data()

# 정규화 (첫날 = 100)
normalized = prices.div(prices.iloc[0]).mul(100)

fig = px.line(
    normalized,
    x=normalized.index,
    y=normalized.columns,
    title="Top 10 Global Companies - 1 Year Performance (Base=100)"
)

fig.update_layout(
    height=700,
    template="plotly_white",
    hovermode="x unified",
    legend_title="Ticker",
    xaxis_title="Date",
    yaxis_title="Normalized Return"
)

st.plotly_chart(fig, use_container_width=True)

# 현재 수익률
returns = (
    (prices.iloc[-1] / prices.iloc[0] - 1)
    .sort_values(ascending=False)
    * 100
)

st.subheader("📈 1년 수익률")

st.dataframe(
    pd.DataFrame({
        "Ticker": returns.index,
        "Return (%)": returns.values.round(2)
    }),
    use_container_width=True
)

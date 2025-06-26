import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="📊 NitroBot Pro Dashboard", layout="wide")
st.title("🚀 NitroBot Pro Dashboard — Market + Bot Trades")

# Initialize exchange
exchange = ccxt.binance()

# Sidebar settings
symbol = st.sidebar.selectbox("Select Pair", ["BTC/USDT", "ETH/USDT", "SOL/USDT"])
timeframe = st.sidebar.selectbox("Timeframe", ["1m", "5m", "15m", "1h", "4h"])
limit = st.sidebar.slider("Candles to Load", min_value=50, max_value=500, value=100)

# Fetch OHLCV data
def fetch_ohlcv(symbol, timeframe, limit):
    try:
        data = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(data, columns=["Time", "Open", "High", "Low", "Close", "Volume"])
        df["Time"] = pd.to_datetime(df["Time"], unit="ms")
        df.set_index("Time", inplace=True)
        df["EMA_9"] = df["Close"].ewm(span=9).mean()
        df["EMA_21"] = df["Close"].ewm(span=21).mean()
        df["RSI"] = compute_rsi(df["Close"], 14)
        return df
    except Exception as e:
        st.error(f"Error fetching market data: {e}")
        return pd.DataFrame()

# Compute RSI
def compute_rsi(series, period):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# Load market data
df = fetch_ohlcv(symbol, timeframe, limit)

if not df.empty:
    st.subheader(f"📉 {symbol} Candlestick + EMA/RSI ({timeframe})")

    # Plot candlestick chart
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["Open"], high=df["High"],
        low=df["Low"], close=df["Close"],
        name="Candles"
    ))
    fig.add_trace(go.Scatter(x=df.index, y=df["EMA_9"], line=dict(color='orange', width=1), name="EMA 9"))
    fig.add_trace(go.Scatter(x=df.index, y=df["EMA_21"], line=dict(color='blue', width=1), name="EMA 21"))

    fig.update_layout(
        height=500,
        xaxis_rangeslider_visible=False,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

    # RSI Plot
    st.subheader("📊 RSI Indicator")
    st.line_chart(df["RSI"])

# Show trade history if available
try:
    trade_df = pd.read_csv("trade_history.csv", parse_dates=["timestamp"])
    st.subheader("📋 NitroBot Trade History")
    st.dataframe(trade_df.tail(10))

    st.subheader("📈 Cumulative Profit")
    trade_df["profit_cumsum"] = trade_df["profit"].cumsum()
    st.line_chart(trade_df.set_index("timestamp")[["profit_cumsum"]])
except FileNotFoundError:
    st.info("No trade history available — waiting for NitroBot trades.")

st.caption("📱 Mobile-optimized layout enabled. Use sidebar for settings.")

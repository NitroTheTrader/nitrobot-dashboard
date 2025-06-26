import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="NitroBot Pro Dashboard", layout="wide")

st.title("🚀 NitroBot Pro Dashboard — Market + Bot Trades")

# Function to fetch market data from CoinGecko
@st.cache_data(ttl=900)
def get_market_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "1",
        "interval": "minute"
    }
    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

try:
    df = get_market_data()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['price'], mode='lines', name='BTC/USD'))
    fig.update_layout(title="Bitcoin Market Price (from CoinGecko)", xaxis_title="Time", yaxis_title="Price (USD)", height=400)
    st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.error(f"Error fetching market data: {e}")

st.subheader("📈 NitroBot Trades (Demo)")

# Example Trade Data
trades = [
    {"time": "2025-06-25 17:00", "type": "BUY", "pair": "BTC/USDT", "price": 61000, "amount": 0.01, "profit": "+$12"},
    {"time": "2025-06-25 16:45", "type": "SELL", "pair": "BTC/USDT", "price": 61200, "amount": 0.01, "profit": "+$18"},
]

trade_df = pd.DataFrame(trades)
st.dataframe(trade_df)

st.sidebar.title("📊 Settings")
st.sidebar.write("Customize your bot alerts, timeframe, etc.")


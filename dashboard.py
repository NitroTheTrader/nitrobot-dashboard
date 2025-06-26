import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests

st.set_page_config(page_title="📊 NitroBot Pro Dashboard", layout="wide")

# Load trade data
try:
    df = pd.read_csv("trade_log.csv")
except:
    st.error("No trade history found.")

# Get real-time BTC price from CoinGecko
def get_price():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
        return r.json()["bitcoin"]["usd"]
    except:
        return None

# Layout
st.title("🚀 NitroBot Pro Dashboard — Market + Bot Trades")
price = get_price()
if price:
    st.metric("📈 BTC/USDT Price", f"${price:,}")
else:
    st.error("Error fetching market price")

if 'df' in locals():
    st.subheader("📉 NitroBot Trades")
    st.dataframe(df[::-1], use_container_width=True)

    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df['time'],
        open=df['price'],
        high=df['price'] + 50,
        low=df['price'] - 50,
        close=df['price']
    ))
    st.plotly_chart(fig, use_container_width=True)

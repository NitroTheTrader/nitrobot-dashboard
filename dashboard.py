import streamlit as st
import subprocess
import os
import pandas as pd
import requests

st.set_page_config(page_title="NitroBot Dashboard", layout="wide")

if "bot_running" not in st.session_state:
    st.session_state.bot_running = False

st.title("🧠 NitroBot AI Trading Dashboard")
st.markdown("---")

# 🔁 Live Price from CoinMarketCap (more stable if you use an API key)
def fetch_price():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        response = requests.get(url, timeout=5)
        data = response.json()
        return float(data["price"])
    except Exception as e:
        print("❌ Price fetch error:", e)
        return None

price = fetch_price()
if price:
    st.metric("BTC/USDT", f"${price:,.2f}")
else:
    st.metric("BTC/USDT", "Unavailable")

st.markdown("### 📈 Profit Tracker")

# Profit Tracker
if os.path.exists("trade_log.csv"):
    df = pd.read_csv("trade_log.csv")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df.dropna(inplace=True)
    df["value"] = df["price"] * df["amount"]
    realized_profit = df["value"].diff().fillna(0).sum()
else:
    df = pd.DataFrame(columns=["type", "price", "amount"])
    realized_profit = 0.00

st.metric("Realized Profit", f"${realized_profit:,.2f}")
st.dataframe(df, use_container_width=True)

st.markdown("### 🤖 Bot Control")

# Bot control
col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 Start NitroBot"):
        if not st.session_state.bot_running:
            st.session_state.process = subprocess.Popen(["python3", "nitrobot.py"])
            st.session_state.bot_running = True
            st.success("NitroBot started!")

with col2:
    if st.button("🛑 Stop NitroBot"):
        if st.session_state.bot_running:
            st.session_state.process.terminate()
            st.session_state.bot_running = False
            st.warning("NitroBot stopped!")

st.write("Bot status:", "🟢 Running" if st.session_state.bot_running else "🔴 Stopped")

import streamlit as st
import subprocess
import os
import pandas as pd
import time
import requests

# Set up page
st.set_page_config(page_title="NitroBot Dashboard", layout="wide")

# Session state setup
if "bot_running" not in st.session_state:
    st.session_state.bot_running = False

# Sidebar controls
mode = st.sidebar.selectbox("Mode", ["Demo", "Real"])
st.sidebar.write("Trading Mode:", mode)

st.title("📊 NitroBot Dashboard")
st.subheader("💰 Live Price Tracker")


# ✅ Working BTC/USDT price fetcher
def fetch_price():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(
            "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            return float(data["price"])
        else:
            print("⚠️ Binance API error:", response.status_code, response.text)
            return None
    except Exception as e:
        print("❌ Exception fetching price:", e)
        return None


# Display price safely
price = fetch_price()
if price is not None:
    st.metric("BTC/USDT Price", f"${price:,.2f}")
else:
    st.metric("BTC/USDT Price", "Fetching price...")


# 📈 Profit Tracker
st.subheader("📈 Profit Tracker")

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

st.metric("Realized PnL", f"${realized_profit:,.2f}")
st.dataframe(df)


# 🕹️ Bot Controls
st.subheader("🕹️ Bot Control")

if st.button("🚀 Start NitroBot"):
    if not st.session_state.bot_running:
        st.session_state.process = subprocess.Popen(["python3", "nitrobot.py"])
        st.session_state.bot_running = True
        st.success("NitroBot started!")

if st.button("🛑 Stop NitroBot"):
    if st.session_state.bot_running:
        st.session_state.process.terminate()
        st.session_state.bot_running = False
        st.warning("NitroBot stopped!")

st.write("Bot status:", "🟢 Running" if st.session_state.bot_running else "🔴 Stopped")

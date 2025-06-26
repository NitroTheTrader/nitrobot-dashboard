import streamlit as st
import time
import csv
import os
import requests

# Set Streamlit page settings
st.set_page_config(page_title="NitroBot Dashboard", layout="wide")
st.title("🚀 NitroBot Dashboard")

# --- Fetch Live BTC Price from CoinGecko ---
def fetch_price(symbol="bitcoin"):
    try:
        response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd")
        data = response.json()
        return data[symbol]['usd']
    except Exception as e:
        print("Error fetching price:", e)
        return "Fetching price..."

# --- Trade Log File ---
TRADE_LOG_FILE = "trade_log.csv"

# --- Load Trade Log ---
def load_trade_log():
    trades = []
    if os.path.exists(TRADE_LOG_FILE):
        with open(TRADE_LOG_FILE, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                trades.append(row)
    return trades

# --- Calculate Realized Profit ---
def calculate_realized_profit(trades):
    try:
        profit = 0.0
        for trade in trades:
            if trade["type"] == "BUY":
                profit -= float(trade["price"]) * float(trade["amount"])
            elif trade["type"] == "SELL":
                profit += float(trade["price"]) * float(trade["amount"])
        return round(profit, 2)
    except:
        return 0.0

# --- Sidebar Controls ---
st.sidebar.header("⚙️ NitroBot Control Panel")
if "bot_running" not in st.session_state:
    st.session_state.bot_running = False

# Start/Stop Button
if st.sidebar.button("▶️ Start Bot"):
    st.session_state.bot_running = True
if st.sidebar.button("⏹️ Stop Bot"):
    st.session_state.bot_running = False

# Demo/Real Mode Toggle
mode = st.sidebar.radio("Mode:", ["Demo", "Real"])
st.sidebar.write(f"🔁 Current Mode: **{mode}**")
st.sidebar.write("---")

# --- Main Dashboard ---
price = fetch_price()
st.metric("💰 BTC/USDT Price", f"${price:,.2f}" if isinstance(price, float) else price)

# Load trades and calculate PnL
trades = load_trade_log()
realized_profit = calculate_realized_profit(trades)
st.metric("📈 Realized PnL", f"${realized_profit:,.2f}")

# Show trade history
st.subheader("📋 Trade History")
if trades:
    st.dataframe(trades)
else:
    st.write("No trade history found yet.")

# Auto-refresh every 15 seconds
st.caption("⏱️ Auto-refreshing every 15 seconds...")
time.sleep(15)
st.experimental_rerun()

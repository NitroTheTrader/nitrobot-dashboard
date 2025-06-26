import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="📊 NitroBot Pro Dashboard", layout="wide")

# Sidebar toggle for Demo or Real
account_type = st.sidebar.radio("Select Account Mode", ["Demo", "Real"])
st.sidebar.markdown(f"### Currently Viewing: {account_type} Account")

# Title
st.title("🚀 NitroBot Pro Dashboard — Live Trades & Market View")

# Get BTC price from CoinGecko
def get_price():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
        return r.json()["bitcoin"]["usd"]
    except:
        return None

btc_price = get_price()
if btc_price:
    st.metric("📈 BTC/USDT Price", f"${btc_price:,}")
else:
    st.error("Error fetching BTC price")

# Load and display trade history
st.subheader("📋 NitroBot Trade History")
try:
    df = pd.read_csv("trade_log.csv")
    st.dataframe(df[::-1], use_container_width=True)

    has_valid_trades = False
    realized_profit = 0
    unrealized_profit = 0
    total_profit = 0

    if not df.empty and {'type', 'price', 'amount'}.issubset(df.columns):
        buy_count = len(df[df['type'] == 'BUY'])
        sell_count = len(df[df['type'] == 'SELL'])

        if buy_count > 0 or sell_count > 0:
            has_valid_trades = True

    if has_valid_trades:
        buys = df[df['type'] == 'BUY']
        sells = df[df['type'] == 'SELL']

        open_positions = []

        for _, row in df.iterrows():
            if row['type'] == 'BUY':
                open_positions.append(row)
            elif row['type'] == 'SELL' and open_positions:
                buy = open_positions.pop(0)
                profit = (row['price'] - buy['price']) * row['amount']
                realized_profit += profit

        for pos in open_positions:
            unrealized_profit += (btc_price - pos['price']) * pos['amount']

        total_profit = realized_profit + unrealized_profit

    # Final Profit Summary
    st.subheader("💰 NitroBot Profit Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Realized Profit", f"${realized_profit:.2f}")
    col2.metric("Unrealized Profit", f"${unrealized_profit:.2f}")
    col3.metric("📊 Total Profit", f"${total_profit:.2f}")

except FileNotFoundError:
    st.warning("⚠️ trade_log.csv not found. Add some trades to see history.")
    st.subheader("💰 NitroBot Profit Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Realized Profit", "$0.00")
    col2.metric("Unrealized Profit", "$0.00")
    col3.metric("📊 Total Profit", "$0.00")
except Exception as e:
    st.error(f"Error loading trade data: {e}")

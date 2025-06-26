import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="📊 NitroBot Pro Dashboard", layout="wide")

# Sidebar demo/real toggle
account_type = st.sidebar.radio("Select Account Mode", ["Demo", "Real"])
st.sidebar.markdown(f"### Currently Viewing: {account_type} Account")

# Title
st.title("🚀 NitroBot Pro Dashboard — Live Trades & Market View")

# Fetch BTC price from CoinGecko
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
except FileNotFoundError:
    st.warning("⚠️ trade_log.csv not found. Add some trades to see history.")
except Exception as e:
    st.error(f"Error loading trade data: {e}")

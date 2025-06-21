# streamlit_app.py
import streamlit as st
import pandas as pd
from kiteconnect import KiteConnect
import datetime

API_KEY = "tw1tc6dl9940mwtu"
ACCESS_TOKEN = "JNDkqIqo49rmGL8cauTVOJHP3N9SQgdr"
SYMBOL = "RELIANCE"
EXCHANGE = "NSE"
INTERVAL = "5minute"
SHORT_MA = 5
LONG_MA = 20

kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

st.set_page_config(page_title="Paper Trading Bot", layout="wide")
st.title("📈 Paper Trading Bot - Zerodha")

if "capital" not in st.session_state:
    st.session_state.capital = 100000
    st.session_state.position = None
    st.session_state.entry_price = 0
    st.session_state.trade_log = []

def fetch_data():
    token = kite.ltp(f"{EXCHANGE}:{SYMBOL}")[f"{EXCHANGE}:{SYMBOL}"]['instrument_token']
    to_date = datetime.datetime.now()
    from_date = to_date - datetime.timedelta(days=5)
    data = kite.historical_data(token, from_date, to_date, INTERVAL)
    return pd.DataFrame(data)

def generate_signal(df):
    df["SMA_short"] = df["close"].rolling(SHORT_MA).mean()
    df["SMA_long"] = df["close"].rolling(LONG_MA).mean()

    if df["SMA_short"].iloc[-2] < df["SMA_long"].iloc[-2] and df["SMA_short"].iloc[-1] > df["SMA_long"].iloc[-1]:
        return "BUY"
    elif df["SMA_short"].iloc[-2] > df["SMA_long"].iloc[-2] and df["SMA_short"].iloc[-1] < df["SMA_long"].iloc[-1]:
        return "SELL"
    else:
        return "HOLD"

def simulate_trade(price, signal):
    if signal == "BUY" and st.session_state.position is None:
        st.session_state.position = "LONG"
        st.session_state.entry_price = price
        st.session_state.trade_log.append(f"BUY at ₹{price:.2f}")
    elif signal == "SELL" and st.session_state.position == "LONG":
        pnl = price - st.session_state.entry_price
        st.session_state.capital += pnl
        st.session_state.trade_log.append(f"SELL at ₹{price:.2f} | P&L: ₹{pnl:.2f}")
        st.session_state.position = None

with st.spinner("Fetching market data..."):
    df = fetch_data()
    last_price = df["close"].iloc[-1]
    signal = generate_signal(df)
    simulate_trade(last_price, signal)

st.metric("💰 Virtual Capital", f"₹{st.session_state.capital:.2f}")
st.metric("📉 Last Price", f"₹{last_price:.2f}")
st.metric("📊 Signal", signal)

st.subheader("📋 Trade Log")
for log in st.session_state.trade_log[::-1]:
    st.text(log)

st.line_chart(df[["close", "SMA_short", "SMA_long"]].dropna())

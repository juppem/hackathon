import streamlit as st
import yfinance as yf
import pandas as pd

# Vlastní CSS pro úpravu vzhledu
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
        color: #003366;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #003366;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Predikce EUR/CZK – Signál pro nákup/prodej")

symbol = "EURCZK=X"
data = yf.download(symbol, period="6mo", interval="1d")

st.subheader("📊 Historický vývoj kurzu")
st.line_chart(data['Close'])

# Výpočet RSI
delta = data['Close'].diff()
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)

avg_gain = gain.rolling(window=14).mean()
avg_loss = loss.rolling(window=14).mean()
rs = avg_gain / avg_loss
rsi = 100 - (100 / (1 + rs))

data['RSI'] = rsi

st.subheader("📈 RSI indikátor")
st.line_chart(data['RSI'])

latest_rsi = data['RSI'].iloc[-1]

st.markdown(f"### 📌 Aktuální RSI: **{latest_rsi:.2f}**")

# Závěrečné doporučení ve stylu šlechtice z 18. století
if latest_rsi < 30:
    st.success("✅ RSI pod 30: Trh je přeprodaný → Signál k nákupu")
elif latest_rsi > 70:
    st.error("⚠️ RSI nad 70: Trh je překoupený → Signál k prodeji")
else:
    st.info("👑 *\"Vážení, dle mého urozeného mínění jest trh v rovnováze. Doporučuji vyčkávat na příhodnější okamžik k akci.\"*")

st.caption("Data: Yahoo Finance (denní interval, 6 měsíců)")
